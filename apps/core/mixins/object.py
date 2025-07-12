# --- 単一オブジェクト関連の Mixin（メタ情報・タイトル表示など） ---
from .base import AutoPageTitleMixin, SafeObjectMixin
from .urls import ObjectUrlMixin


class ObjectContextMixin(ObjectUrlMixin, AutoPageTitleMixin):
    """
    単一オブジェクトの詳細表示や編集に関連するコンテキストデータを提供する Mixin。
    - タイトルの動的生成（例: 「〇〇 の編集」）
    - 作成・更新日時の表示
    """

    object_title_field = None  # 例: 'name'（任意のフィールド名）

    def get_context_title(self):
        """
        オブジェクトに基づいてページ内タイトルを生成。
        例: '田中一郎 の編集'
        """
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
        """
        context にタイトル・作成日・更新日を追加。
        """
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


class ObjectMetaContextMixin(SafeObjectMixin):
    """
    オブジェクトのメタ情報（作成日時・更新日時）を context に注入するための Mixin。
    """

    def inject_object_meta(self, context):
        """
        context に 'created_at', 'updated_at' を追加。
        """
        obj = self.get_object_safe()
        context['created_at'] = getattr(obj, 'created_at', None)
        context['updated_at'] = getattr(obj, 'updated_at', None)
        return context


class BaseContextMixin(AutoPageTitleMixin, ObjectMetaContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.inject_page_title(context)
        return context
