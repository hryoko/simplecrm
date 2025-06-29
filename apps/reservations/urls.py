from django.urls import path

from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.ReservationListView.as_view(), name='list'),
    path('create/', views.ReservationCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ReservationDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.ReservationUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='delete'),
]
