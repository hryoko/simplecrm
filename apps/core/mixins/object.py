# --- 単一オブジェクト関連の Mixin（メタ情報・タイトル表示など） ---
from django.http import Http404
from django.urls import NoReverseMatch, reverse

from .base import BaseContextMixin
from .urls import AutoNamespaceMixin


class SafeObjectMixin:
    # object取得を安全に行う
    def get_object_safe(self):
        """get_object() を安全に実行し、
        存在しない場合は None を返す"""
        try:
            return self.get_object()
        except Http404:
            return None


class ObjectLabelContextMixin(SafeObjectMixin):
    """テンプレートに object の表示名（label）を context 変数として追加する Mixin。
    モデル側に get_object_label() があればそれを使い、なければ str(obj) を使う。
    """

    def get_object_label(self):
        obj = self.get_object_safe()
        # モデルに get_object_label() があればそれを使う
        if obj and hasattr(obj, 'get_object_label'):
            return obj.get_object_label()

        # それ以外は __str__() を使う（None の場合は空文字）
        return str(obj) if obj else ''

    def inject_object_label(self, context):
        context['object_label'] = self.get_object_label()
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.inject_object_label(context)


class ObjectTitleContextMixin:
    """
    オブジェクトからタイトル（例:「〇〇 の 編集」）を生成して context['title'] に注入する Mixin。
    """

    object_title_field = None  # 例: 'name'（任意のフィールド名）

    def get_context_title(self):
        """
        オブジェクトに基づいてページ内タイトルを生成。
        例: '田中一郎 の編集'
        """
        obj = self.get_object_safe()
        field = self.object_title_field

        if obj:
            if field and hasattr(obj, field):
                value = getattr(obj, field)
            else:
                value = str(obj)
            if value:
                return f"{value} の {self.get_page_title()}"
        return self.get_page_title()

    def inject_title(self, context):
        context['title'] = self.get_context_title()
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.inject_title(context)


# class ObjectMetaContextMixin(SafeObjectMixin):
#     """
#     オブジェクトのメタ情報（作成日時・更新日時）を context に注入するための Mixin。
#     """

#     def inject_object_meta(self, context):
#         """
#         context に 'created_at', 'updated_at' を追加。
#         """
#         obj = self.get_object_safe()
#         # 以下は削除検討中。テンプレートで問題なければ削除予定
#         context.update(
#             {
#                 'created_at': getattr(obj, 'created_at', None),
#                 'updated_at': getattr(obj, 'updated_at', None),
#             }
#         )
#         return context

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return self.inject_object_meta(context)


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

    def inject_object_urls(self, context):
        context.update(
            {
                'back_url': self.get_back_url(),
                'detail_url': self.get_detail_url(),
                'update_url': self.get_update_url(),
                'delete_url': self.get_delete_url(),
            }
        )
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.inject_object_urls(context)


class ObjectContextMixin(ObjectLabelContextMixin, ObjectUrlMixin, BaseContextMixin):
    """
    タイトル + 作成・更新日時を context にまとめて注入したいとき用の合成Mixin。
    """

    pass


class DetailFieldsMixin:
    """
    オブジェクトのフィールドを「ラベル + 値」の形で context['details'] に構築する Mixin。

    - 通常の詳細ビューにおいて、テンプレート側でループして表示するために便利。
    - `detail_exclude_fields` によって除外したいフィールドを指定可能。
    - `detail_field_order` によって表示順を明示的にコントロール可能。
    """

    # 除外するフィールド名（デフォルトでよくある3つ）
    detail_exclude_fields = ['id', 'created_at', 'updated_at']
    # 表示順を固定したい場合はリストで指定（Noneなら全フィールドから自動生成）
    detail_field_order = None

    def get_detail_fields(self):
        """
        表示対象のフィールド名リストを取得し、ラベルと値のペアに変換。
        context['details'] に格納される各要素は:
            {
                "label": "名前",
                "value": "田中一郎"
            }
        のような形式。
        """
        obj = self.get_object()
        model = obj.__class__

        # 表示順が明示されていればそれを使う、なければ exclude_fields に従う
        if self.detail_field_order is not None:
            field_names = self.detail_field_order
        else:
            field_names = [
                f.name
                for f in model._meta.fields
                if f.name not in self.detail_exclude_fields
            ]

        # フィールド名 → 表示ラベルと値のペアに変換
        return [
            {
                "label": model._meta.get_field(name).verbose_name.title(),
                "value": getattr(obj, name),
            }
            for name in field_names
        ]

    def inject_details(self, context):
        """
        context に 'details' キーを追加。
        テンプレートでは {{ details }} をループして表示に利用可能。
        """
        context['details'] = self.get_detail_fields()
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.inject_details(context)
