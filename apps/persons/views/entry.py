from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView

from apps.core.mixins import CreateViewMixin
from apps.inquiries.models import Reception

from ..forms import PersonInquiryReceptionForm


class EntryCreateView(CreateViewMixin, TemplateView):
    template_name = 'persons/create_entry.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = PersonInquiryReceptionForm(request.POST)
        if form.is_valid():
            person, inquiry, reception = form.save(staff=request.user)
            messages.success(request, '登録が完了しました。')
            return redirect('persons:list')
        # バリデーションエラー時はフォームを渡して再表示
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # フォームはkwargsで渡されたら使い、なければ新規生成
        context['form'] = kwargs.get('form') or PersonInquiryReceptionForm()
        context['person_fields'] = [
            "full_name",
            "full_name_kana",
            "phone",
            "age",
            "email",
            "line_name",
            "branch",
            "idcard",
            "description",
        ]
        context['inquiry_fields'] = ["method", "content"]
        context['reception_fields'] = ["status", "remarks"]
        return context


class EntryListView(ListView):
    model = Reception
    template_name = "persons/entry_list.html"
    context_object_name = "entries"

    def get_queryset(self):
        return Reception.objects.select_related(
            "inquiry__person", "staff", "inquiry__method"
        ).order_by("-received_at")
