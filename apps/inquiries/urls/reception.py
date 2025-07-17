from django.urls import path
from inquiries.views.reception import ReceptionCreateView, ReceptionListView

urlpatterns = [
    path('', ReceptionListView.as_view(), name='reception_list'),
    path('create/', ReceptionCreateView.as_view(), name='reception_create'),
]
