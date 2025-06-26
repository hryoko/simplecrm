from django.shortcuts import render, redirect, get_object_or_404
from .models import Bottle
from .forms import BottleForm


def bottle_create(request):
    if request.method == 'POST':
        form = BottleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bottle_list')
    else:
        form = BottleForm()
    return render(request, 'bottles/bottle_form.html', {'form': form})


def bottle_list(request):
    bottles = Bottle.objects.select_related('customer').all()
    return render(request, 'bottles/bottle_list.html', {'bottles': bottles})


def bottle_detail(request, pk):
    bottle = get_object_or_404(Bottle, pk=pk)
    return render(request, 'bottles/bottle_detail.html', {'bottle': bottle})


def bottle_update(request, pk):
    bottle = get_object_or_404(Bottle, pk=pk)
    if request.method == 'POST':
        form = BottleForm(request.POST, instance=bottle)
        if form.is_valid():
            form.save()
            return redirect('bottle_detail', pk=pk)
    else:
        form = BottleForm(instance=bottle)
    return render(request, 'bottles/bottle_form.html', {'form': form})


def bottle_delete(request, pk):
    bottle = get_object_or_404(Bottle, pk=pk)
    if request.method == 'POST':
        bottle.delete()
        return redirect('bottle_list')
    return render(request, 'bottles/bottle_confirm_delete.html', {'bottle': bottle})
