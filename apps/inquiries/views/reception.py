from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.core.mixins import (
    CreateViewMixin,
    DeleteViewMixin,
    DetailViewMixin,
    ListViewMixin,
    PageTitleFromObjectMixin,
    UpdateViewMixin,
)

from ..forms.reception import ReceptionForm
from ..models.reception import Reception


class ViewSettingsMixin:
    model = Reception
    namespace = 'inquiries'
    back_view = 'reception-list'
    list_view = 'reception-list'
    detail_view = 'reception-detail'
    update_view = 'reception-update'
    delete_view = 'reception-delete'

    def dispatch(self, request, *args, **kwargs):
        print('[...]')
        print('  model       =', self.model)
        print('  namespace   =', self.namespace)
        print('  back_view   =', self.back_view)
        print('  list_view   =', self.list_view)
        print('  detail_view =', self.detail_view)
        print('  update_view =', self.update_view)
        print('  delete_view =', self.delete_view)
        return super().dispatch(request, *args, **kwargs)


class ReceptionListView(ViewSettingsMixin, ListViewMixin, ListView):
    model = Reception
    template_name = 'inquiries/reception/list.html'
    context_object_name = 'receptions'
    paginate_by = 10


class ReceptionDetailView(
    ViewSettingsMixin, PageTitleFromObjectMixin, DetailViewMixin, DetailView
):
    model = Reception
    template_name = 'inquiries/reception/detail.html'
    context_object_name = 'reception'
    # detail_exclude_fields = ['id', 'name', 'age', 'memo', 'created_at', 'updated_at']
    title_attr = 'full_name'


class ReceptionCreateView(ViewSettingsMixin, CreateViewMixin, CreateView):
    model = Reception
    form_class = ReceptionForm
    template_name = 'inquiries/reception/form.html'
    success_url = reverse_lazy('reception-list')


class ReceptionUpdateView(ViewSettingsMixin, UpdateViewMixin, UpdateView):
    model = Reception
    form_class = ReceptionForm
    template_name = 'inquiries/reception/form.html'

    def get_success_url(self):
        return reverse('receptions:reception-detail', kwargs={'pk': self.object.pk})


class ReceptionDeleteView(ViewSettingsMixin, DeleteViewMixin, DeleteView):
    model = Reception
    template_name = 'inquiries/reception/confirm_delete.html'
    success_url = reverse_lazy('receptions:reception-list')
    # back_view = 'detail'
