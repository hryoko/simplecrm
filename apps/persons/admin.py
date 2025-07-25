from django.contrib import admin

from .forms import PersonForm
from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # def __init__(self, model, admin_site):
    #     super().__init__(model, admin_site)
    #     self.list_display = [field.name for field in model._meta.fields]
    form = PersonForm
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
    # fieldsets = (
    #     ('基本情報', {'fields': ('name_kanji', 'name_kana', 'age')}),
    #     ('連絡先', {'fields': ('phone', 'email', 'line_name')}),
    #     ('登録情報', {'fields': ('branch', 'idcard')}),
    #     ('備考', {'fields': ('description',)}),
    #     ('システム情報', {'fields': ('created_at', 'updated_at')}),
    # )
    fieldsets = (
        ('基本情報', {'fields': (('name_kanji', 'name_kana', 'age'),)}),
        ('連絡先', {'fields': (('phone', 'email', 'line_name'),)}),
        ('登録情報', {'fields': (('branch', 'idcard'),)}),
        ('備考', {'fields': ('description',)}),
        ('システム情報', {'fields': ('created_by', 'created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at']
