from django.http import Http404
from django.urls import NoReverseMatch, reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

# from .url import AutoNamespaceMixin


# --- 基本ユーティリティ ---


class AutoNamespaceMixin:
    # model = None  # Django CBV の model と連携
    namespace = None  # 例: 'customers'

    # ---- URL名生成 ----
    def get_namespace(self):
        """明示指定がなければ model から app_label を推測"""
        if self.namespace:
            return self.namespace
        elif self.model:
            return self.model._meta.app_label  # モデルからアプリ名を推測
        return None

    def namespaced_url(self, viewname, *args):
        ns = self.get_namespace()
        if ns:
            return reverse(f'{ns}:{viewname}', args=args)
        return reverse(viewname, args=args)


class PageTitleMixin:
    page_title = None

    def get_page_title(self):
        return self.page_title or 'ページ'

    def inject_page_title(self, context):
        context['page_title'] = self.get_page_title()
        return context


class SafeObjectMixin:
    # ---- オブジェクト関連 ----
    def get_object_safe(self):
        """objectが存在する場合は返す（なければNone）"""
        try:
            return self.get_object()
        except Http404:
            return None


class AutoPageTitleMixin(PageTitleMixin):
    page_title = None
    action_label = None

    def get_page_title(self):
        if self.page_title:
            return self.page_title
        if getattr(self, 'model', None):
            return f"{self.model._meta.verbose_name}{self.get_action_label()}"
        return super().get_page_title()

    def get_action_label(self):
        if self.action_label:
            return self.action_label

        match self:
            case ListView():
                return '一覧'
            case CreateView():
                return '新規登録'
            case DetailView():
                return '詳細'
            case UpdateView():
                return '編集'
            case DeleteView():
                return '削除'
            case _:
                return ''


class ObjectMetaContextMixin(SafeObjectMixin):
    def inject_object_meta(self, context):
        obj = self.get_object_safe()
        context['created_at'] = getattr(obj, 'created_at', None)
        context['updated_at'] = getattr(obj, 'updated_at', None)
        return context


class BaseContextMixin(AutoPageTitleMixin, ObjectMetaContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.inject_page_title(context)
        return context


class ListViewMixin(BaseContextMixin, AutoNamespaceMixin):
    exclude_fields = ['created_at', 'updated_at']
    wanted_field_keys = None  # 順序付きで指定したい場合

    def get_table_headers(self):
        """
        一覧表示用のヘッダー定義を返す。
        - wanted_field_keys があればその順序に従う
        - なければ exclude_fields を除いた全フィールドを使う
        """
        if self.wanted_field_keys:
            fields = self.wanted_field_keys
        else:
            fields = [
                f.name
                for f in self.model._meta.fields
                if f.name not in self.exclude_fields
            ]

        headers = []
        for name in fields:
            field = self.model._meta.get_field(name)
            headers.append(
                {
                    'key': name,
                    'label': str(field.verbose_name),
                }
            )

        return headers

    def get_table_rows(self, queryset, headers):
        """
        headers に基づいて各行を構築。各行は dict。
        - key: フィールド名
        - value: 安全に取得された値（外部キーなら str(obj) ）
        - detail_url / update_url / delete_url も自動追加
        """
        keys = [h['key'] for h in headers]
        rows = []

        for obj in queryset:
            row = {key: self._get_cell_value(obj, key) for key in keys}

            # URL付加（try-exceptで柔軟に）
            try:
                row['detail_url'] = self.namespaced_url('detail', obj.pk)
                row['update_url'] = self.namespaced_url('update', obj.pk)
                row['delete_url'] = self.namespaced_url('delete', obj.pk)
            except NoReverseMatch:
                pass  # 該当URLが未定義でもスルー

            rows.append(row)

        return rows

    def _get_cell_value(self, obj, key):
        """
        各セルの表示値を取得。外部キーは __str__() にフォールバック。
        上書きしてカスタム可能。
        """
        try:
            val = getattr(obj, key)
            if val is None:
                return ''
            if hasattr(val, '_meta'):  # 外部キーや related object
                return str(val)
            return val
        except (NoReverseMatch, AttributeError):
            return ''  # 存在しないキーなどを安全に無視

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        headers = self.get_table_headers()
        rows = self.get_table_rows(queryset, headers)
        context['headers'] = headers
        context['rows'] = rows
        return context


class NavigationUrlMixin:
    """ナビゲーションURL関連の拡張用 Mixin"""

    ...


# --- オブジェクト系共通 ---


class ObjectUrlMixin(SafeObjectMixin, AutoNamespaceMixin):
    """
    オブジェクトに紐づく各種URLを提供するMixin。
    """

    back_view = 'list'
    detail_view = 'detail'
    update_view = 'update'
    delete_view = 'delete'
    fallback_redirect = 'home'  # デフォルトのリダイレクト先

    # ---- 各種URL取得 ----
    def get_object_url(self, viewname):
        obj = self.get_object_safe()
        if obj and getattr(obj, 'pk', None):
            return self.namespaced_url(viewname, obj.pk)
        return None

    def get_list_url(self):
        return self.namespaced_url(self.list_view)

    def get_detail_url(self):
        return self.get_object_url(self.detail_view)

    def get_update_url(self):
        return self.get_object_url(self.update_view)

    def get_delete_url(self):
        return self.get_object_url(self.delete_view)

    def get_created_at(self):
        obj = self.get_object_safe()
        return getattr(obj, 'created_at', None) if obj else None

    def get_updated_at(self):
        obj = self.get_object_safe()
        return getattr(obj, 'updated_at', None) if obj else None

    def get_back_url(self):
        """
        back_view があれば namespaced_url でURLを返す。
        失敗したり obj が無ければ fallback_redirect にリダイレクトURLを返す。
        """
        try:
            if self.back_view:
                return self.namespaced_url(self.back_view)
        except NoReverseMatch:
            pass

        # fallback_redirect は名前（名前付きURL）かURL文字列のどちらでも対応
        if self.fallback_redirect:
            # URL文字列か名前か判別して返す簡易処理
            if self.fallback_redirect.startswith(('http://', 'https://', '/')):
                return self.fallback_redirect
            else:
                try:
                    return reverse(self.fallback_redirect)
                except NoReverseMatch:
                    pass
        return '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'back_url': self.get_back_url(),
                'detail_url': self.get_detail_url(),
                'update_url': self.get_update_url(),
                'delete_url': self.get_delete_url(),
            }
        )
        return context


class ObjectContextMixin(ObjectUrlMixin, AutoPageTitleMixin):
    object_title_field = None  # 例: 'name'（任意のフィールド名）

    def get_context_title(self):
        """ページ内タイトル（例: '田中一郎 の編集'）"""
        obj = self.get_object_safe()
        field = getattr(self, 'object_title_field', None)

        if obj:
            if field and hasattr(obj, field):
                value = getattr(obj, field)
            else:
                value = str(obj)  # fallback to __str__()
            if value:
                return f"{value} の{getattr(self, 'page_title', '')}"
        return getattr(self, 'page_title', '')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object_safe()
        context.update(
            {
                'title': self.get_context_title(),
                'created_at': getattr(obj, 'created_at', None),
                'updated_at': getattr(obj, 'updated_at', None),
            }
        )
        return context


class DetailContextMixin(ObjectContextMixin): ...


class SubmitLabelMixin:
    submit_label = None

    def get_submit_label(self):
        return self.submit_label

    def inject_submit_label(self, context):
        context['submit_label'] = self.get_submit_label()
        return context


class FormActionMixin(SubmitLabelMixin, ObjectContextMixin):
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


class CreateContextMixin(FormActionMixin):
    submit_label = '新規保存'


class UpdateContextMixin(FormActionMixin):
    submit_label = '更新保存'


class DeleteContextMixin(SubmitLabelMixin, ObjectContextMixin):
    submit_label = 'はい、削除します'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.inject_submit_label(context)


"""
                PageTitleMixin
                     ↑
           ┌────────┴────────┐
           │                 │
AutoNamespaceMixin     AutoPageTitleMixin
           ↑                 ↑
           └──────┬──────────┘
                  ↓
       ObjectUrlMixin
                  ↓
       ObjectContextMixin
       ↓        ↓        ↓
DetailCtx  FormViewCtx  DeleteCtx
              ↑
   ┌──────────┴──────────┐
CreateCtx            UpdateCtx

ListViewMixin → AutoPageTitleMixin + AutoNamespaceMixin
"""
