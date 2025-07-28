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
from apps.inquiries.models import Inquiry

from .forms import PersonForm
from .models import Person


class PersonListView(ListViewMixin, ListView):
    model = Person
    template_name = 'persons/list.html'
    context_object_name = 'persons'
    namespace = 'persons'
    # exclude_fields = ['memo', 'created_at', 'updated_at']
    wanted_field_keys = ['id', 'name_kanji', 'name_kana', 'age', 'phone', 'email']
    paginate_by = 10


class PersonDetailView(PageTitleFromObjectMixin, DetailViewMixin, DetailView):
    model = Person
    template_name = 'persons/detail.html'
    context_object_name = 'person'
    namespace = 'persons'
    # detail_exclude_fields = ['id', 'name', 'age', 'memo', 'created_at', 'updated_at']
    title_attr = 'name_kanji'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inquiries'] = Inquiry.objects.filter(person=self.object).order_by(
            '-received_at'
        )
        return context


class PersonCreateView(CreateViewMixin, CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'persons/form.html'
    success_url = reverse_lazy('list')

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super().form_valid(form)

    # def form_valid(self, form):
    #     print('request.user:', self.request.user)
    #     print('form.user:', getattr(form, 'user', None))

    #     person = form.save(commit=False)
    #     print('Before save, person.created_by:', person.created_by)

    #     person = form.save()  # commit=True で保存
    #     print('After save, person.created_by:', person.created_by)

    #     return super().form_valid(form)


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
