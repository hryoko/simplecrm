from django.urls import path

from . import views

app_name = 'persons'

urlpatterns = [
    path('', views.PersonListView.as_view(), name='list'),
    path('create/', views.PersonCreateView.as_view(), name='create'),
    path('<int:pk>/', views.PersonDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.PersonUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.PersonDeleteView.as_view(), name='delete'),
]
