# --- 単一オブジェクト関連の Mixin（メタ情報・タイトル表示など） ---
from .base import AutoPageTitleMixin
from .urls import ObjectUrlMixin


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
