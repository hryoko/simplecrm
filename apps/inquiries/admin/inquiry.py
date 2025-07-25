from django.contrib import admin

from ..forms.inquiry import InquiryForm
from ..models.inquiry import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    form = InquiryForm

    list_display = ['id', 'person', 'method', 'brand', 'received_at']
    list_filter = ['brand', 'method', 'received_at']
    search_fields = [
        'person__name_kanji',
        'person__name_kana',
        'person__phone',
        'person__email',
        'person__line_name',
    ]
    # ordering = ['-received_at']
    # raw_id_fields = ['person']
    autocomplete_fields = ['person']  # 外部キー名そのまま指定
