from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = 'core'

urlpatterns = [
    # path('', views.index, name='index'),  # ルートURL
    path(
        '', RedirectView.as_view(pattern_name='core:home', permanent=False)
    ),  # ルートURLからhomeにリダイレクトさせる
    path('home/', views.home, name='home'),  # ホームページ
    # path('dashboard/', views.dashboard, name='dashboard'),  # ダッシュボード
]
