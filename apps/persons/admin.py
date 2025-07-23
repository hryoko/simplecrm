from django.contrib import admin

from .forms import PersonForm
from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # def __init__(self, model, admin_site):
    #     super().__init__(model, admin_site)
    #     self.list_display = [field.name for field in model._meta.fields]
    form = PersonForm
    list_display = (
        'full_name',
        'full_name_kana',
        'age',
        'branch',
        'idcard',
        'created_at',
    )
    list_filter = ('branch', 'created_at')
    search_fields = ('full_name', 'full_name_kana', 'phone', 'email', 'line_name')
    fieldsets = (
        ('基本情報', {'fields': ('full_name', 'full_name_kana', 'age')}),
        ('連絡先', {'fields': ('phone', 'email', 'line_name')}),
        ('その他', {'fields': ('description',)}),
        ('登録情報', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')
