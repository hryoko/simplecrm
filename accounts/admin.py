from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    def __init__(self, model, admin_site):
        """
        モデルの全フィールド名を自動的に list_display に設定する。
        これにより、明示的に list_display を定義しなくても、管理画面で全フィールドが一覧表示される。
        """
        super().__init__(model, admin_site)
        self.list_display = [field.name for field in model._meta.fields]

    list_display = list(UserAdmin.list_display) + []


CustomUser = get_user_model()
admin.site.register(CustomUser, CustomUserAdmin)

"""
参考
https://office54.net/python/django/model-custom-user
https://daeudaeu.com/django-useradmin/

get_user_model は、settings.py で AUTH_USER_MODEL に指定されているモデルを取得する関数。

現時点で有効になっているUserモデル自体を呼び出してくれます。
つまり、AUTH_USER_MODELにCustomUserが指定されている場合はCustomUserを、
デフォルトのUserのままであればUserモデルを呼び出します。
"""
