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

        # wanted_field_keys = ['name_kana', 'age', 'phone', 'email', 'memo']  # 任意順
        # headers = [h for h in all_headers if h['key'] in wanted_field_keys]

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
    context_object_name = 'customer'

    def namespaced_url(self, namespace, viewname, *args):
        return reverse(f'{namespace}:{viewname}', args=args)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = self.object
        exclude_keys = {'id', 'created_at', 'updated_at'}

        # ラベルと値を動的に構成
        context['details'] = [
            {
                "label": field.verbose_name.title(),
                "value": getattr(obj, field.name),
            }
            for field in Customer._meta.fields
            if field.name not in exclude_keys
        ]

        # 別枠で登録日などを渡す
        context['created_at'] = obj.created_at

        # 操作用URL（テンプレート共通化用に）
        context['update_url'] = self.namespaced_url('customers', 'update', obj.pk)
        context['delete_url'] = self.namespaced_url('customers', 'delete', obj.pk)
        context['back_url'] = self.namespaced_url('customers', 'list')

        context['title'] = obj.name
        context['page_title'] = '顧客詳細'
        return context


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object
        context['title'] = f'title: {obj.name}'
        context['page_title'] = 'page_title顧客編集'
        return context


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('list')
