from django.urls import path

from .views import inquiry, interview, trial

app_name = 'inquiries'

urlpatterns = [
    # Inquiry
    path('inquiries/', inquiry.InquiryListView.as_view(), name='inquiry_list'),
    path(
        'inquiries/<int:pk>/',
        inquiry.InquiryDetailView.as_view(),
        name='inquiry_detail',
    ),
    path(
        'inquiries/create/',
        inquiry.InquiryCreateView.as_view(),
        name='inquiry_create',
    ),
]
