from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from apps.inquiries.forms.inquiry import InquiryForm
from apps.inquiries.models import Inquiry, Reception


class ReceptionInline(admin.TabularInline):  # または admin.StackedInline
    model = Reception
    extra = 0
    fields = ['status', 'staff', 'remarks', 'received_at']
    readonly_fields = ['received_at']
    ordering = ['-received_at']


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    form = InquiryForm
    inlines = [ReceptionInline]

    list_display = [
        'id',
        'person',
        'method',
        'brand',
        'received_at',
        'previous_inquiry_link',
    ]
    list_filter = ['brand', 'method', 'received_at']
    search_fields = [
        'person__name_kanji',
        'person__name_kana',
        'person__phone',
        'person__email',
        'person__line_name',
    ]
    autocomplete_fields = ['person']

    def previous_inquiry_link(self, obj):
        """同一人物＆ブランドの過去問い合わせがあればリンク付きで表示"""
        qs = Inquiry.objects.filter(
            person=obj.person, brand=obj.brand, received_at__lt=obj.received_at
        ).exclude(id=obj.id)
        if qs.exists():
            previous = qs.latest('received_at')
            url = reverse("admin:inquiries_inquiry_change", args=[previous.id])
            return format_html(
                '<a href="{}">{}（{}）</a>',
                url,
                "過去の同ブランド応募あり",
                previous.received_at.strftime('%Y-%m-%d %H:%M'),
            )
        return "なし"

    previous_inquiry_link.short_description = "過去応募履歴"

    readonly_fields = ['previous_inquiry_display']

    def previous_inquiry_display(self, obj):
        if not obj.previous_inquiry:
            return '-'
        url = reverse('admin:inquiries_inquiry_change', args=[obj.previous_inquiry.id])
        return format_html(
            '<a href="{}">#{} - {} - {}</a>',
            url,
            obj.previous_inquiry.id,
            obj.previous_inquiry.received_at.strftime('%Y-%m-%d'),
            obj.previous_inquiry.method,
        )

    previous_inquiry_display.short_description = 'Previous Inquiry'
