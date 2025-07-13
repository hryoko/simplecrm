# --- フォーム系（CRUD）ビュー関連 ---
from .base import BaseContextMixin
from .object import DetailFieldsMixin, ObjectContextMixin


class SubmitLabelMixin:
    submit_label = None

    def get_submit_label(self):
        return self.submit_label

    def inject_submit_label(self, context):
        context['submit_label'] = self.get_submit_label()
        return context


class FormActionMixin(SubmitLabelMixin, ObjectContextMixin):
    """
    フォームの送信先URL（form_action）とボタンラベル（submit_label）を context に注入する Mixin。
    Create/Update 共通。
    """

    form_action_view = None

    def get_form_action_args(self):
        obj = self.get_object_safe()
        return (getattr(obj, 'pk', None),) if obj else ()

    def get_form_action(self):
        if self.form_action_view:
            return self.namespaced_url(
                self.form_action_view, *self.get_form_action_args()
            )
        return self.request.path  # 自分自身にPOST（Createなど）

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.inject_submit_label(context)
        context['form_action'] = self.get_form_action()
        return context


class DetailViewMixin(DetailFieldsMixin): ...


class CreateViewMixin(FormActionMixin):
    submit_label = '新規保存'


class UpdateViewMixin(FormActionMixin):
    submit_label = '更新保存'


class DeleteViewMixin(SubmitLabelMixin, ObjectContextMixin):
    submit_label = 'はい、削除します'
    form_action_view = None  # 明示的に None（→ request.path）

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.inject_submit_label(context)
