from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from ..core.mixins.mixins import (
    CreateContextMixin,
    DeleteContextMixin,
    DetailContextMixin,
    FormContextMixin,
    ListViewMixin,
    UpdateContextMixin,
)
from .forms import CustomerForm
from .models import Customer


class CustomerCreateView(CreateContextMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('list')
    object_title_field = 'name'


class CustomerListView(ListViewMixin, ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'
    namespace = 'customers'
    # exclude_fields = ['memo', 'created_at', 'updated_at']
    wanted_field_keys = ['id', 'name', 'name_kana', 'age', 'phone', 'email']


class CustomerDetailView(DetailContextMixin, DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'
    namespace = 'customers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = self.object
        exclude_keys = ['id', 'created_at', 'updated_at']
        # exclude_keys = ['id', 'name']
        # exclude_keys = ['id', 'name', 'age', 'memo', 'created_at', 'updated_at']

        # ラベルと値を動的に構成
        context['details'] = [
            {
                "label": field.verbose_name.title(),
                "value": getattr(obj, field.name),
            }
            for field in Customer._meta.fields
            if field.name not in exclude_keys
        ]

        return context


class CustomerUpdateView(UpdateContextMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customers:list')
    object_title_field = 'name'


class CustomerDeleteView(DeleteContextMixin, DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customers:list')
    # back_view = 'detail'
    object_title_field = 'name'
