from django.urls import path

from .views import entry, person

app_name = 'persons'

urlpatterns = [
    path('', person.PersonListView.as_view(), name='list'),
    path('create/', person.PersonCreateView.as_view(), name='create'),
    path('<int:pk>/', person.PersonDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', person.PersonUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', person.PersonDeleteView.as_view(), name='delete'),
    path('create-entry/', entry.EntryCreateView.as_view(), name='entry-create'),
    path('entry-list/', entry.EntryListView.as_view(), name='entry-list'),
]
