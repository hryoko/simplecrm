from .entry import EntryCreateView, EntryListView, EntryUpdateView
from .person import (
    PersonCreateView,
    PersonDeleteView,
    PersonDetailView,
    PersonListView,
    PersonUpdateView,
)

__all__ = [
    'PersonListView',
    'PersonCreateView',
    'PersonDetailView',
    'PersonUpdateView',
    'PersonDeleteView',
    'EntryCreateView',
    'EntryListView',
    'EntryUpdateView',
]
