from django.urls import path

from ..views import reception

urlpatterns = [
    path('reception/', reception.ReceptionListView.as_view(), name='reception-list'),
]
