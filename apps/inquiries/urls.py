from django.urls import path

from .views import inquiry_views, interview_views, trial_views

app_name = 'inquiries'

urlpatterns = [
    # Inquiry
    path('inquiries/', inquiry_views.InquiryListView.as_view(), name='inquiry_list'),
    path(
        'inquiries/<int:pk>/',
        inquiry_views.InquiryDetailView.as_view(),
        name='inquiry_detail',
    ),
    path(
        'inquiries/create/',
        inquiry_views.InquiryCreateView.as_view(),
        name='inquiry_create',
    ),
    # Interview
    path(
        'interviews/',
        interview_views.InterviewListView.as_view(),
        name='interview_list',
    ),
    path(
        'interviews/<int:pk>/',
        interview_views.InterviewDetailView.as_view(),
        name='interview_detail',
    ),
    # Trial
    path('trials/', trial_views.TrialListView.as_view(), name='trial_list'),
    path(
        'trials/<int:pk>/', trial_views.TrialDetailView.as_view(), name='trial_detail'
    ),
]
