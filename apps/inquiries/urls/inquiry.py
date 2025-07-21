from django.urls import path

from ..views import inquiry

urlpatterns = [
    path('inquiry/', inquiry.InquiryListView.as_view(), name='inquiry-list'),
    path('inquiry/create/', inquiry.InquiryCreateView.as_view(), name='inquiry-create'),
    path(
        'inquiry/<int:pk>/', inquiry.InquiryDetailView.as_view(), name='inquiry-detail'
    ),
    path(
        'inquiry/<int:pk>/edit/',
        inquiry.InquiryUpdateView.as_view(),
        name='inquiry-update',
    ),
    path(
        'inquiry/<int:pk>/delete/',
        inquiry.InquiryDeleteView.as_view(),
        name='inquiry-delete',
    ),
]
