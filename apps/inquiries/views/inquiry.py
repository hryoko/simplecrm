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

from ..forms import InquiryForm
from ..models import Inquiry


class ViewSettingsMixin:
    model = Inquiry
    namespace = 'inquiries'
    back_view = 'inquiry-list'
    list_view = 'inquiry-list'
    detail_view = 'inquiry-detail'
    update_view = 'inquiry-update'
    delete_view = 'inquiry-delete'

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


class InquiryListView(ViewSettingsMixin, ListViewMixin, ListView):
    model = Inquiry
    template_name = 'inquiries/inquiry/list.html'
    context_object_name = 'inquiries'
    paginate_by = 10
    ordering = ['-created_at']


class InquiryDetailView(
    ViewSettingsMixin, PageTitleFromObjectMixin, DetailViewMixin, DetailView
):
    model = Inquiry
    template_name = 'inquiries/inquiry/detail.html'
    context_object_name = 'inquiry'
    # detail_exclude_fields = ['id', 'name', 'age', 'memo', 'created_at', 'updated_at']
    # title_attr = 'full_name'


class InquiryCreateView(ViewSettingsMixin, CreateViewMixin, CreateView):
    model = Inquiry
    form_class = InquiryForm
    template_name = 'inquiries/inquiry/form.html'
    success_url = reverse_lazy('inquiry-list')


class InquiryUpdateView(ViewSettingsMixin, UpdateViewMixin, UpdateView):
    model = Inquiry
    form_class = InquiryForm
    template_name = 'inquiries/inquiry/form.html'

    def get_success_url(self):
        return reverse('inquiries:inquiry-detail', kwargs={'pk': self.object.pk})


class InquiryDeleteView(ViewSettingsMixin, DeleteViewMixin, DeleteView):
    model = Inquiry
    template_name = 'inquiries/inquiry/confirm_delete.html'
    success_url = reverse_lazy('inquiries:inquiry-list')
    # back_view = 'detail'
