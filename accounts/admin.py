from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    # list_display = list(UserAdmin.list_display) + []
    pass


CustomUser = get_user_model()
admin.site.register(CustomUser, CustomUserAdmin)

"""
参考
https://office54.net/python/django/model-custom-user
https://daeudaeu.com/django-useradmin/

get_user_model は、settings.py で AUTH_USER_MODEL に指定されているモデルを取得する関数。

現時点で有効になっているUserモデル自体を呼び出してくれます。つまり、AUTH_USER_MODELにCustomUserが指定されている場合はCustomUserを、デフォルトのUserのままであればUserモデルを呼び出します。
"""
