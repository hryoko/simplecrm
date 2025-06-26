from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Customer
from .forms import CustomerForm


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


def customer_list(request):
    customers = Customer.objects.all()
    name = request.GET.get('name')
    phone = request.GET.get('phone')
    if name:
        customers = customers.filter(name__icontains=name)
    if phone:
        customers = customers.filter(phone__icontains=phone)
    return render(request, 'customers/customer_list.html', {'customers': customers})


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
