from django.urls import path

from .views import entry, person

app_name = 'persons'

urlpatterns = [
    # Person用
    path('', person.PersonListView.as_view(), name='list'),
    path('create/', person.PersonCreateView.as_view(), name='create'),
    path('<int:pk>/', person.PersonDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', person.PersonUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', person.PersonDeleteView.as_view(), name='delete'),
    # Entry用（統一的な命名）
    path('entries/', entry.EntryListView.as_view(), name='entry_list'),
    path('entries/create/', entry.EntryCreateView.as_view(), name='entry_create'),
    path(
        'entries/<int:pk>/edit/', entry.EntryUpdateView.as_view(), name='entry_update'
    ),
    # path('create-entry/', entry.EntryCreateView.as_view(), name='entry-create'),
    # path('entry-list/', entry.EntryListView.as_view(), name='entry-list'),
    # path('<int:pk>/entry/edit/', entry.EntryUpdateView.as_view(), name='entry_update'),
]
