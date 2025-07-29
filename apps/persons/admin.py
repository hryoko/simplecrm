# import nested_admin
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from apps.inquiries.models import Inquiry, Reception

from .forms import PersonForm
from .models import Person

# class InquiryInline(admin.TabularInline):  # または StackedInline
#     model = Inquiry
#     extra = 0
#     fields = ['method', 'brand', 'received_at', 'previous_inquiry_display']
#     readonly_fields = ['received_at', 'previous_inquiry_display']


# class ReceptionInline(NestedTabularInline):
#     model = Reception
#     extra = 0
#     fields = ['status', 'staff', 'remarks', 'received_at']
#     readonly_fields = ['received_at']


class InquiryInline(NestedTabularInline):
    model = Inquiry
    extra = 0
    # inlines = [ReceptionInline]
    fields = ['method', 'brand', 'received_at', 'previous_inquiry_display']
    readonly_fields = ['received_at', 'previous_inquiry_display']
    # can_delete = False

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


@admin.register(Person)
class PersonAdmin(NestedModelAdmin):
    form = PersonForm
    inlines = [InquiryInline]
    list_display = [
        'name_kanji',
        'name_kana',
        'age',
        'branch',
        'idcard',
        'created_by',
        'created_at',
    ]
    list_filter = ['branch', 'created_at']
    search_fields = ['name_kanji', 'name_kana', 'phone', 'email', 'line_name']
    fieldsets = (
        ('システム情報', {'fields': ('created_by', 'created_at', 'updated_at')}),
        ('基本情報', {'fields': (('name_kanji', 'name_kana'), 'age')}),
        ('連絡先', {'fields': (('phone', 'email', 'line_name'),)}),
        ('登録情報', {'fields': (('branch', 'idcard'),)}),
        ('備考', {'fields': ('description',)}),
    )
    readonly_fields = ['created_at', 'updated_at']

    def get_form(self, request, obj=None, **kwargs):
        """
        フォーム生成時に created_by フィールドへ初期値（ログインユーザー）をセット
        created_by が存在する時だけ初期値セット（安全に）
        """
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            # created_by が存在する時だけ初期値セット（安全に）
            if 'created_by' in form.base_fields:
                form.base_fields['created_by'].initial = request.user
        return form

    def save_model(self, request, obj, form, change):
        """
        保存時、created_by が未設定の場合にログインユーザーで補完（冗長だが安全策）
        change = False のとき＝新規登録時のみ実行
        """
        if not change and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
