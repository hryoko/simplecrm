from django.urls import path

from . import views

app_name = 'bottles'

urlpatterns = [
    path('', views.BottleListView.as_view(), name='list'),
    path('create/', views.BottleCreateView.as_view(), name='create'),
    path('<int:pk>/', views.BottleDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.BottleUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.BottleDeleteView.as_view(), name='delete'),
]
