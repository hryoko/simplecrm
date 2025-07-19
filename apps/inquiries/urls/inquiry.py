from django.urls import path

from ..views import inquiry

urlpatterns = [
    path('inquiry/', inquiry.InquiryListView.as_view(), name='inquiry-list'),
]
