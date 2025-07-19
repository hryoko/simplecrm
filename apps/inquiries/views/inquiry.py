from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.core.mixins import (
    CreateViewMixin,
    DeleteViewMixin,
    DetailViewMixin,
    ListViewMixin,
    PageTitleFromObjectMixin,
    UpdateViewMixin,
)

# from .forms import PersonForm
from ..models import Inquiry


class InquiryListView(ListViewMixin, ListView):
    model = Inquiry
    template_name = 'inquiries/inquiry/list.html'
    context_object_name = 'inquiry'
    namespace = 'inquiry'
    # exclude_fields = ['memo', 'created_at', 'updated_at']
    # wanted_field_keys = ['id', 'full_name', 'full_name_kana', 'age', 'phone', 'email']
    paginate_by = 10
