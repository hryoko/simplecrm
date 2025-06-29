from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CustomerForm
from .models import Customer


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('list')


class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'

    def namespaced_url(self, namespace, viewname, *args):
        return reverse(f'{namespace}:{viewname}', args=args)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_headers = [
            {"key": field.name, "label": field.verbose_name.title()}
            for field in Customer._meta.fields
        ]
        exclude_keys = {'created_at', 'updated_at'}
        headers = [h for h in all_headers if h['key'] not in exclude_keys]
        wanted_fields = [h['key'] for h in headers]

        # rows に URL を追加
        rows = []
        for c in context['customers']:
            row = {key: getattr(c, key) for key in wanted_fields}
            row['detail_url'] = self.namespaced_url('customers', 'detail', c.pk)
            row['update_url'] = self.namespaced_url('customers', 'update', c.pk)
            row['delete_url'] = self.namespaced_url('customers', 'delete', c.pk)
            rows.append(row)

        context['headers'] = headers
        context['rows'] = rows
        context['page_title'] = '顧客一覧'
        return context


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('list')


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('list')
