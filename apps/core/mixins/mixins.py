from django.http import Http404
from django.urls import reverse

from .url import AutoContextMixin


class AutoContextMixin:
    model = None  # Django CBV の model と連携
    namespace = None  # 例: 'customers'

    # ---- URL名生成 ----
    def get_namespace(self):
        """明示指定がなければ model から app_label を推測"""
        if self.namespace:
            return self.namespace
        elif self.model:
            return self.model._meta.app_label  # モデルからアプリ名を推測
        return None
        # return self.namespace or self.model._meta.app_label

    def namespaced_url(self, viewname, *args):
        ns = self.get_namespace()
        if ns:
            return reverse(f'{ns}:{viewname}', args=args)
        return reverse(viewname, args=args)


class BaseContextMixin(AutoContextMixin):
    # 表示やリンク用の基本設定
    page_title = ''

    # ---- オブジェクト関連 ----
    def get_object_safe(self):
        """objectが存在する場合は返す（なければNone）"""
        try:
            return self.get_object()
        except (AttributeError, Http404):
            return None

    def get_page_title(self):
        return self.page_title or ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.get_page_title()
        return context


class BaseListViewMixin:
    exclude_fields = ['created_at', 'updated_at']
    wanted_field_keys = None  # 順序付きで指定したい場合
    context_object_name = None  # 明示されていればそれを使う

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
                    "key": name,
                    "label": field.verbose_name.title(),
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
            # row = {key: getattr(obj, key) for key in keys}
            row = {key: self.get_cell_value(obj, key) for key in keys}

            # URL付加（try-exceptで柔軟に）
            try:
                row['detail_url'] = self.namespaced_url('detail', obj.pk)
                row['update_url'] = self.namespaced_url('update', obj.pk)
                row['delete_url'] = self.namespaced_url('delete', obj.pk)
            except:
                pass  # 該当URLが未定義でもスルー

            rows.append(row)

        return rows

    def get_cell_value(self, obj, key):
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
        except Exception:
            return ''  # 存在しないキーなどを安全に無視

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj_name = self.context_object_name or 'object_list'
        queryset = context.get(obj_name, [])
        headers = self.get_table_headers()
        context['headers'] = headers
        context['rows'] = self.get_table_rows(queryset, headers)
        return context


class ListContextMixin(BaseContextMixin):
    back_view = None  # listページでは不要なことが多いが必要なら指定
    page_title = '一覧'


class ListViewMixin(ListContextMixin, BaseListViewMixin):
    """一覧ビュー用のUI + データ構造をまとめた統合Mixin"""

    pass


class ObjectContextMixin(BaseContextMixin):
    # 表示やリンク用の基本設定
    object_title_field = None  # 例: 'name'（任意のフィールド名）
    back_view = 'list'
    detail_view = 'detail'
    update_view = 'update'
    delete_view = 'delete'

    # ボタンなどの表示文言
    back_label = '戻る'
    detail_label = '詳細'
    update_label = '編集'
    delete_label = '削除'

    # ---- オブジェクト関連 ----
    # def get_object_safe(self):
    #     """objectが存在する場合は返す（なければNone）"""
    #     return getattr(self, 'object', None)

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
                return f"{value} の{self.page_title}"

        return self.page_title or ''

    # ---- 各種URL取得 ----
    def get_back_url(self):
        if self.back_view:
            return self.namespaced_url(self.back_view)
        return None  # または reverse('top') などのデフォルト

    def get_detail_url(self):
        return self.namespaced_url(self.detail_view, self.get_object_safe().pk)

    def get_update_url(self):
        return self.namespaced_url(self.update_view, self.get_object_safe().pk)

    def get_delete_url(self):
        return self.namespaced_url(self.delete_view, self.get_object_safe().pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object_safe()
        context.update(
            {
                'title': self.get_context_title(),
                'back_url': self.get_back_url(),
                'detail_url': self.get_detail_url(),
                'update_url': self.get_update_url(),
                'delete_url': self.get_delete_url(),
                'created_at': getattr(obj, 'created_at', None),
                'updated_at': getattr(obj, 'updated_at', None),
                'back_label': self.back_label,
                'detail_label': self.detail_label,
                'update_label': self.update_label,
                'delete_label': self.delete_label,
            }
        )
        return context


class DetailContextMixin(ObjectContextMixin):
    page_title = '詳細'
    object_title_field = 'name'


class FormContextMixin(ObjectContextMixin):
    form_action_view = None
    submit_label = '保存label'

    # def get_form_action(self):
    #     if self.form_action_view:
    #         return self.namespaced_url(self.form_action_view, self.get_object_safe().pk)
    #     return self.request.path  # フォールバックとして自分自身にPOST

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form_action'] = self.get_form_action()
        context['submit_label'] = self.submit_label
        return context


class CreateContextMixin(BaseContextMixin):
    page_title = '新規'


class CreateContextMixin(BaseContextMixin):
    """
    CreateView 専用のコンテキストMixin。
    object がまだ存在しない前提で、安全に back_url などを提供。
    """

    back_view = 'list'
    back_label = '戻る'
    page_title = '新規'  # 自動で「新規作成」に変換される想定

    def get_back_url(self):
        if self.back_view:
            return self.namespaced_url(self.back_view)
        return self.request.META.get('HTTP_REFERER', '/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'back_url': self.get_back_url(),
                'back_label': self.back_label,
                'title': self.get_page_title(),  # ページ内タイトル
            }
        )
        return context


class UpdateContextMixin(FormContextMixin):
    back_view = 'detail'
    page_title = '更新'


class DeleteContextMixin(ObjectContextMixin):
    # back_view = 'detail'
    page_title = '削除'
