from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)
from .models import Reservation
from .forms import ReservationForm


class ReservationListView(ListView):
    model = Reservation
    template_name = 'reservations/reservation_list.html'
    context_object_name = 'reservations'


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/reservation_form.html'
    success_url = reverse_lazy('reservation_list')


class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/reservation_form.html'
    success_url = reverse_lazy('reservation_list')


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'reservations/reservation_detail.html'


class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'reservations/reservation_confirm_delete.html'
    success_url = reverse_lazy('reservation_list')
