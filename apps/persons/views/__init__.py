from .entry import EntryCreateView, EntryListView
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
]
