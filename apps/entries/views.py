from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from apps.core.mixins import (
    AutoNamespaceMixin,
    CreateViewMixin,
    DeleteViewMixin,
    DetailViewMixin,
    ListViewMixin,
    PageTitleFromObjectMixin,
    UpdateViewMixin,
)
from apps.inquiries.models import Inquiry, Interview, Reception
from apps.persons.models import Person

from .forms import PersonInquiryReceptionForm


class EntryCreateView(TemplateView):
    template_name = 'entries/form.html'
    namespace = 'inquiries'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = PersonInquiryReceptionForm(request.POST)
        if form.is_valid():
            person, inquiry, reception = form.save(staff=request.user)
            messages.success(request, '登録が完了しました。')
            return redirect('entries:list')
        # バリデーションエラー時はフォームを渡して再表示
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # フォームはkwargsで渡されたら使い、なければ新規生成
        context['form'] = kwargs.get('form') or PersonInquiryReceptionForm()
        context['person_fields'] = [
            'full_name',
            'full_name_kana',
            'phone',
            'age',
            'email',
            'line_name',
            'branch',
            'idcard',
            'description',
        ]
        context['inquiry_fields'] = ['method', 'content']
        context['reception_fields'] = ['status', 'remarks']
        context['title'] = 'エントリー新規作成'
        context['submit_label'] = '登録する'
        return context


class EntryListView(ListView):
    model = Reception
    template_name = 'entries/list.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return Reception.objects.select_related(
            'inquiry__person', 'staff', 'inquiry__method'
        ).order_by('-received_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interviews'] = Interview.objects.select_related(
            'inquiry__person'
        ).order_by('-scheduled_date')
        return context


class EntryDetailView(DetailView):
    model = Reception
    template_name = 'entries/detail.html'
    context_object_name = 'reception'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reception = self.object
        context['inquiry'] = reception.inquiry
        context['person'] = reception.inquiry.person
        return context


class EntryUpdateView(TemplateView):
    template_name = 'entries/form.html'

    def get_object(self):
        return get_object_or_404(
            Reception.objects.select_related('inquiry__person'), pk=self.kwargs['pk']
        )

    def get(self, request, *args, **kwargs):
        reception = self.get_object()
        inquiry = reception.inquiry
        person = inquiry.person
        form = PersonInquiryReceptionForm(
            person=person, inquiry=inquiry, reception=reception
        )
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        reception = self.get_object()
        inquiry = reception.inquiry
        person = inquiry.person
        form = PersonInquiryReceptionForm(
            request.POST, person=person, inquiry=inquiry, reception=reception
        )
        if form.is_valid():
            form.save(staff=request.user)
            messages.success(request, '更新が完了しました。')
            return redirect('entries:entry_list')
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs['form']
        context['person_fields'] = [
            'full_name',
            'full_name_kana',
            'phone',
            'age',
            'email',
            'line_name',
            'branch',
            'idcard',
            'description',
        ]
        context['inquiry_fields'] = ['method', 'content']
        context['reception_fields'] = ['status', 'remarks']
        context['title'] = 'エントリー編集'
        context['submit_label'] = '更新する'
        return context


class EntryDeleteView(TemplateView): ...
