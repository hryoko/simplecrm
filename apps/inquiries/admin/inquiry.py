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
        'brand',
        'method',
        'status',
        'staff',
        'received_at',
        'previous_inquiry_link',
    ]
    list_filter = ['brand', 'method', 'status', 'staff', 'received_at']
    search_fields = [
        'person__name_kanji',
        'person__name_kana',
        'person__phone',
        'person__email',
        'person__line_name',
        'content',
        'remarks',
    ]
    ordering = ['-received_at']

    readonly_fields = ['previous_inquiry', 'updated_at']
    autocomplete_fields = ['person']
    exclude = ['previous_inquiry']  # フォームから除外
    fieldsets = (
        ('基本情報', {'fields': ('person', 'brand', 'method', 'content')}),
        ('対応情報', {'fields': ('status', 'staff', 'remarks', 'previous_inquiry')}),
        ('日付情報', {'fields': ('received_at', 'updated_at')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['staff'].initial = request.user
        return form

    def save_model(self, request, obj, form, change):
        if not obj.staff:
            obj.staff = request.user
        super().save_model(request, obj, form, change)

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

    def previous_inquiry_display(self, obj):
        if not obj.previous_inquiry:
            return '-'
        url = reverse('admin:inquiries_inquiry_change', args=[obj.previous_inquiry.id])
        return format_html(
            '<a href="{}">#{} | {} | {} ({})</a>',
            url,
            obj.previous_inquiry.id,
            obj.previous_inquiry.received_at.strftime('%Y-%m-%d %H:%M'),
            obj.previous_inquiry.get_method_display(),
            obj.previous_inquiry.get_brand_display(),
        )

    previous_inquiry_display.short_description = 'Previous Inquiry'
