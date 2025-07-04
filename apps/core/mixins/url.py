# from django.urls import reverse


# class AutoContextMixin:
#     model = None  # Django CBV の model と連携
#     namespace = None  # 例: 'customers'

#     # ---- URL名生成 ----
#     def get_namespace(self):
#         """明示指定がなければ model から app_label を推測"""
#         if self.namespace:
#             return self.namespace
#         elif self.model:
#             return self.model._meta.app_label  # モデルからアプリ名を推測
#         return None
#         # return self.namespace or self.model._meta.app_label

#     def namespaced_url(self, viewname, *args):
#         ns = self.get_namespace()
#         if ns:
#             return reverse(f'{ns}:{viewname}', args=args)
#         return reverse(viewname, args=args)
