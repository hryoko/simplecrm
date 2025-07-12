# --- URL関連のMixin（リダイレクト・名前付きURL補助など） ---
from django.urls import NoReverseMatch, reverse

from .base import SafeObjectMixin  # ベースMixinを使う


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


class NavigationUrlMixin:
    """ナビゲーションURL関連の拡張用 Mixin"""

    ...
