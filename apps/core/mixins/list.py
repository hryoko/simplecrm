# --- 一覧表示関連 ---
from .base import BaseContextMixin
from .urls import AutoNamespaceMixin


class ListViewMixin(BaseContextMixin, AutoNamespaceMixin):
    """
    一覧表示用のコンテキストを構築する汎用 Mixin。
    - ヘッダー定義の自動生成
    - 行データの整形（外部キーや関連オブジェクトにも対応）
    - detail/update/delete の各URLを自動生成
    """

    exclude_fields = ['created_at', 'updated_at']
    wanted_field_keys = None  # 順序付きで指定したい場合

    def get_table_headers(self):
        """
        一覧表示用のヘッダー定義を返す。
        - wanted_field_keys があればその順序に従う（任意フィールド指定）
        - なければ model._meta.fields から exclude_fields を除いたものを使用
        - 各項目は {'key': フィールド名, 'label': verbose_name} の形式
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
            except AttributeError:
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
        except AttributeError:
            return ''  # 存在しないキーなどを安全に無視

    def inject_headers(self, context):
        """
        context に headers を追加。
        """
        context['headers'] = self.get_table_headers()
        return context

    def inject_rows(self, context):
        """
        context に rows を追加。
        """
        queryset = self.get_queryset()
        headers = context.get('headers') or self.get_table_headers()
        context['rows'] = self.get_table_rows(queryset, headers)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.inject_headers(context)
        context = self.inject_rows(context)
        return context
