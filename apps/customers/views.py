from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.core.mixins import (
    BaseContextMixin,
    CreateViewMixin,
    DeleteViewMixin,
    DetailViewMixin,
    ListViewMixin,
    PageTitleFromObjectMixin,
    UpdateViewMixin,
)

from .forms import CustomerForm
from .models import Customer


class CustomerListView(ListViewMixin, ListView):
    model = Customer
    template_name = 'customers/list.html'
    context_object_name = 'customers'
    namespace = 'customers'
    # exclude_fields = ['memo', 'created_at', 'updated_at']
    wanted_field_keys = ['id', 'name', 'name_kana', 'age', 'phone', 'email']


class CustomerCreateView(CreateViewMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/form.html'
    success_url = reverse_lazy('list')


class CustomerDetailView(PageTitleFromObjectMixin, DetailViewMixin, DetailView):
    model = Customer
    template_name = 'customers/detail.html'
    context_object_name = 'customer'
    namespace = 'customers'
    # detail_exclude_fields = ['id', 'name', 'age', 'memo', 'created_at', 'updated_at']
    title_attr = 'name'


class CustomerUpdateView(UpdateViewMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/form.html'

    def get_success_url(self):
        return reverse('customers:detail', kwargs={'pk': self.object.pk})


class CustomerDeleteView(DeleteViewMixin, DeleteView):
    model = Customer
    template_name = 'customers/confirm_delete.html'
    success_url = reverse_lazy('customers:list')
    # back_view = 'detail'
