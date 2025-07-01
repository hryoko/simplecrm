from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ReservationForm
from .models import Reservation


class ReservationListView(ListView):
    model = Reservation
    template_name = 'reservations/reservation_list.html'
    context_object_name = 'reservations'
    queryset = Reservation.objects.select_related('customer').all()

    def namespaced_url(self, namespace, viewname, *args):
        return reverse(f'{namespace}:{viewname}', args=args)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_headers = [
            {"key": field.name, "label": field.verbose_name.title()}
            for field in Reservation._meta.fields
        ]
        exclude_keys = {'created_at', 'updated_at'}
        headers = [h for h in all_headers if h['key'] not in exclude_keys]
        wanted_fields = [h['key'] for h in headers]

        # rows に URL を追加
        rows = []
        for c in context['reservations']:
            # row = {key: getattr(c, key) for key in wanted_fields}
            row = {}
            for key in wanted_fields:
                value = getattr(c, key)
                if key == 'customer':
                    value = str(value)
                row[key] = value
            row['detail_url'] = self.namespaced_url('reservations', 'detail', c.pk)
            row['update_url'] = self.namespaced_url('reservations', 'update', c.pk)
            row['delete_url'] = self.namespaced_url('reservations', 'delete', c.pk)
            rows.append(row)

        context['headers'] = headers
        context['rows'] = rows
        context['page_title'] = '予約一覧'
        return context


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/reservation_form.html'
    success_url = reverse_lazy('reservation_list')


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'reservations/reservation_detail.html'

    context_object_name = 'reservation'

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
            for field in Reservation._meta.fields
            if field.name not in exclude_keys
        ]

        # 別枠で登録日などを渡す
        context['created_at'] = obj.created_at

        # 操作用URL（テンプレート共通化用に）
        context['update_url'] = self.namespaced_url('customers', 'update', obj.pk)
        context['delete_url'] = self.namespaced_url('customers', 'delete', obj.pk)
        context['back_url'] = self.namespaced_url('customers', 'list')

        context['title'] = f'{obj.customer.name} の予約'
        context['page_title'] = '予約詳細'
        return context


class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/reservation_form.html'
    success_url = reverse_lazy('reservation_list')


class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'reservations/reservation_confirm_delete.html'
    success_url = reverse_lazy('reservation_list')
