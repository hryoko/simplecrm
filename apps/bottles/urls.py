from django.urls import path
from . import views

urlpatterns = [
    path('', views.bottle_list, name='bottle_list'),
    path('create/', views.bottle_create, name='bottle_create'),
    path('<int:pk>/', views.bottle_detail, name='bottle_detail'),
    path('<int:pk>/edit/', views.bottle_update, name='bottle_update'),
    path('<int:pk>/delete/', views.bottle_delete, name='bottle_delete'),
]
