"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

admin.site.site_title = 'Django 管理サイト-title'
admin.site.site_header = 'サイト管理者-header'
admin.site.index_title = 'サイト管理-index_title'
# admin.site.unregister(Group)  # 認証と認可の非表示
# admin.site.disable_action(
#     'delete_selected'
# )  # リストのチェックボックスからの削除を無効化する

urlpatterns = [
    path(
        'admin/logout/',
        auth_views.LogoutView.as_view(next_page='/admin/login/'),
        name='admin_logout',
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(next_page='/'),
        name='logout',
    ),
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core')),
    path('accounts/', include('django.contrib.auth.urls')),  # 認証URLを一式を登録
    path('customers/', include('apps.customers.urls')),
    path('persons/', include('apps.persons.urls')),
    # path('inquiry/', include('apps.inquiries.urls')),
    # path('entry/', include('apps.entries.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
