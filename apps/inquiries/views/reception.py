from django.views.generic import CreateView, ListView

from ..forms.reception import ReceptionForm
from ..models.reception import Reception


class ReceptionListView(ListView):
    model = Reception
    template_name = 'inquiries/reception/list.html'
    context_object_name = 'receptions'


class ReceptionCreateView(CreateView):
    model = Reception
    form_class = ReceptionForm
    template_name = 'inquiries/reception/form.html'
    success_url = '/inquiries/receptions/'  # 適宜変更
