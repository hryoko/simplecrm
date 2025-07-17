from django.urls import path

from .views import inquiry, interview, trial

app_name = 'inquiries'
from inquiries.views.reception import ReceptionCreateView, ReceptionListView

urlpatterns = [
    path('', ReceptionListView.as_view(), name='reception_list'),
    path('create/', ReceptionCreateView.as_view(), name='reception_create'),
]
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
    # Reception
    path('', ReceptionListView.as_view(), name='reception_list'),
    path('create/', ReceptionCreateView.as_view(), name='reception_create'),
    # Interview
    path(
        'interviews/',
        interview.InterviewListView.as_view(),
        name='interview_list',
    ),
    path(
        'interviews/<int:pk>/',
        interview.InterviewDetailView.as_view(),
        name='interview_detail',
    ),
    # Trial
    path('trials/', trial.TrialListView.as_view(), name='trial_list'),
    path(
        'trials/<int:pk>/', trial.TrialDetailView.as_view(), name='trial_detail'
    ),
]
