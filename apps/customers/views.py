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
    UpdateViewMixin,
)

from .forms import CustomerForm
from .models import Customer


class CustomerListView(ListViewMixin, ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'
    namespace = 'customers'
    # exclude_fields = ['memo', 'created_at', 'updated_at']
    wanted_field_keys = ['id', 'name', 'name_kana', 'age', 'phone', 'email']
    wanted_field_keys = ['id', 'name', 'age', 'phone']


class CustomerCreateView(CreateViewMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('list')
    object_title_field = 'name'


class CustomerDetailView(DetailViewMixin, DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'
    namespace = 'customers'
    # detail_exclude_fields = ['id', 'name', 'age', 'memo', 'created_at', 'updated_at']


class CustomerUpdateView(UpdateViewMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    object_title_field = 'name'

    def get_success_url(self):
        return reverse('customers:detail', kwargs={'pk': self.object.pk})


class CustomerDeleteView(DeleteViewMixin, DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customers:list')
    # back_view = 'detail'
    object_title_field = 'name'
