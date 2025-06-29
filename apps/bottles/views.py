from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import BottleForm
from .models import Bottle


class BottleListView(ListView):
    model = Bottle
    template_name = 'bottles/bottle_list.html'
    context_object_name = 'bottles'
    queryset = Bottle.objects.select_related('customer').all()

    def namespaced_url(self, namespace, viewname, *args):
        return reverse(f'{namespace}:{viewname}', args=args)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_headers = [
            {"key": field.name, "label": field.verbose_name.title()}
            for field in Bottle._meta.fields
        ]
        exclude_keys = {'created_at', 'updated_at'}
        headers = [h for h in all_headers if h['key'] not in exclude_keys]
        wanted_fields = [h['key'] for h in headers]

        # rows に URL を追加
        rows = []
        for c in context['bottles']:
            # row = {key: getattr(c, key) for key in wanted_fields}
            row = {}
            for key in wanted_fields:
                value = getattr(c, key)
                if key == 'customer':
                    value = str(value)
                row[key] = value
            row['detail_url'] = self.namespaced_url('bottles', 'detail', c.pk)
            row['update_url'] = self.namespaced_url('bottles', 'update', c.pk)
            row['delete_url'] = self.namespaced_url('bottles', 'delete', c.pk)
            rows.append(row)

        context['headers'] = headers
        context['rows'] = rows
        context['page_title'] = 'ボトル一覧'
        return context


class BottleCreateView(CreateView):
    model = Bottle
    form_class = BottleForm
    template_name = 'bottles/bottle_form.html'
    success_url = reverse_lazy('list')


class BottleDetailView(DetailView):
    model = Bottle
    template_name = 'bottles/bottle_detail.html'


class BottleUpdateView(UpdateView):
    model = Bottle
    form_class = BottleForm
    template_name = 'bottles/bottle_form.html'
    success_url = reverse_lazy('list')


class BottleDeleteView(DeleteView):
    model = Bottle
    template_name = 'bottles/bottle_confirm_delete.html'
    success_url = reverse_lazy('list')
