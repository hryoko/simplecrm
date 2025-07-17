from django.urls import include, path

app_name = 'inquiries'

urlpatterns = [
    path('receptions/', include('inquiries.urls.reception')),
    path('inquiries/', include('inquiries.urls.inquiry')),
]
