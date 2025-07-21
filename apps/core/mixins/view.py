# --- フォーム系（CRUD）ビュー関連 ---
from .base import BaseContextMixin, PageTitleFromObjectMixin
from .object import DetailFieldsMixin, ObjectContextMixin


class SubmitLabelMixin:
    """
    Submitボタンのラベルをコンテキストに注入するMixin。
    サブクラスで `submit_label` を定義するか、
    `get_submit_label()` をオーバーライドしてカスタマイズ可能。
    """

    submit_label = None

    def get_submit_label(self):
        if self.submit_label is not None:
            return self.submit_label
        # デフォルト値は汎用的に「Submit」
        return 'Submit'

    def inject_submit_label(self, context):
        context['submit_label'] = self.get_submit_label()
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # submit_labelを追加
        return self.inject_submit_label(context)


class FormContextMixin(SubmitLabelMixin):
    """
    フォームの送信先URL (form_action) を context に注入する Mixin。
    Create / Update 共通想定。
    """

    form_action_view = None  # namespaced_url の第一引数に使うURLやview名等

    def get_form_action_args(self):
        obj = self.get_object_safe()
        # objがあればpkをURL引数に使う想定。なければ空タプル
        return (getattr(obj, 'pk', None),) if obj else ()

    def get_form_action(self):
        if self.form_action_view:
            return self.namespaced_url(
                self.form_action_view, *self.get_form_action_args()
            )
        # 指定がなければ現在のパスをPOST先とする（Create時など）
        return self.request.path  # 自分自身にPOST（Createなど）

    def inject_form_context(self, context):
        # form_actionを追加
        context['form_action'] = self.get_form_action()
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.inject_form_context(context)


class DetailViewMixin(ObjectContextMixin, DetailFieldsMixin): ...


class CreateViewMixin(FormContextMixin, BaseContextMixin):
    submit_label = '新規保存'
    # form_action_view = 'app:create'


class UpdateViewMixin(FormContextMixin, ObjectContextMixin):
    submit_label = '更新保存'
    # form_action_view = 'app:update'


class DeleteViewMixin(SubmitLabelMixin, ObjectContextMixin):
    submit_label = 'はい、削除します'
    form_action_view = None  # 明示的に None（→ request.path）
