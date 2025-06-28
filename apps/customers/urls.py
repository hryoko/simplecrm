from django.urls import path

from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.CustomerListView.as_view(), name='list'),
    path('create/', views.customer_create, name='create'),
    path('success/', views.customer_success, name='success'),
    path('<int:pk>/', views.customer_detail, name='detail'),
    path('<int:pk>/edit/', views.customer_update, name='update'),
    path('<int:pk>/delete/', views.customer_delete, name='delete'),
] + [
    # path('', views.customer_list, name='customer_list'),
    # path('create/', views.CustomerCreateView.as_view(), name='customer_create'),
    # path('<int:pk>/', views.customer_detail, name='customer_detail'),
    # path('<int:pk>/edit/', views.customer_update, name='customer_update'),
    # path('<int:pk>/delete/', views.customer_delete, name='customer_delete'),
]
