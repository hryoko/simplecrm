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

from .forms import PersonForm
from .models import Person


class PersonListView(ListViewMixin, ListView):
    model = Person
    template_name = 'persons/list.html'
    context_object_name = 'persons'
    namespace = 'persons'
    # exclude_fields = ['memo', 'created_at', 'updated_at']
    # wanted_field_keys = ['id', 'full_name', 'full_name_kana', 'age', 'phone', 'email']
    paginate_by = 10


class PersonCreateView(CreateViewMixin, CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'persons/form.html'
    success_url = reverse_lazy('list')


class PersonDetailView(PageTitleFromObjectMixin, DetailViewMixin, DetailView):
    model = Person
    template_name = 'persons/detail.html'
    context_object_name = 'person'
    namespace = 'persons'
    # detail_exclude_fields = ['id', 'name', 'age', 'memo', 'created_at', 'updated_at']
    title_attr = 'full_name'


class PersonUpdateView(UpdateViewMixin, UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'persons/form.html'

    def get_success_url(self):
        return reverse('persons:detail', kwargs={'pk': self.object.pk})


class PersonDeleteView(DeleteViewMixin, DeleteView):
    model = Person
    template_name = 'persons/confirm_delete.html'
    success_url = reverse_lazy('persons:list')
    # back_view = 'detail'
