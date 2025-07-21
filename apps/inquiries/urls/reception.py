from django.urls import path

from ..views import reception

urlpatterns = [
    path('reception/', reception.ReceptionListView.as_view(), name='reception-list'),
    path(
        'reception/create/',
        reception.ReceptionCreateView.as_view(),
        name='reception-create',
    ),
    path(
        'reception/<int:pk>/',
        reception.ReceptionDetailView.as_view(),
        name='reception-detail',
    ),
    path(
        'reception/<int:pk>/edit/',
        reception.ReceptionUpdateView.as_view(),
        name='reception-update',
    ),
    path(
        'reception/<int:pk>/delete/',
        reception.ReceptionDeleteView.as_view(),
        name='reception-delete',
    ),
]
