from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # path(
    #     '', RedirectView.as_view(pattern_name='core:home', permanent=False)
    # ),  # ルートURLからhomeにリダイレクトさせる
    # path('home/', views.home, name='home'),  # ホームページ
    # path('dashboard/', views.dashboard, name='dashboard'),  # ダッシュボード
]
