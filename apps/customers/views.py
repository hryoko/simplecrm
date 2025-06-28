from django.shortcuts import get_object_or_404, redirect, render
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


def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_success')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form})


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer_list')


# def customer_create(request):
#     if request.method == 'POST':
#         form = CustomerForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('customer_list')
#     else:
#         form = CustomerForm()
#     return render(request, 'customers/customer_form.html', {'form': form})


def customer_success(request):
    return render(request, 'customers/customer_success.html')


# def customer_list(request):
#     customers = Customer.objects.all()
#     name = request.GET.get('name')
#     phone = request.GET.get('phone')
#     if name:
#         customers = customers.filter(name__icontains=name)
#     if phone:
#         customers = customers.filter(phone__icontains=phone)
#     return render(request, 'customers/customer_list.html', {'customers': customers})


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
        return context


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customers/customer_detail.html', {'customer': customer})


def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form})


def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(
        request, 'customers/customer_confirm_delete.html', {'customer': customer}
    )
