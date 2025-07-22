from django.contrib import admin

from .models import Person


@admin.register(Person)
class CustomerAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = [field.name for field in model._meta.fields]

    # list_display = (
    #     'id',
    #     'full_name',
    #     'full_name_kana',
    #     'age',
    #     'phone',
    #     # 'email',
    #     # 'line_name',
    #     'branch',
    #     'idcard',
    #     # 'created_at',
    # )
    list_filter = ('branch', 'created_at')
    search_fields = ('full_name', 'full_name_kana', 'phone', 'email', 'line_name')

    # fieldsets = (
    #     ('基本情報', {'fields': ('full_name', 'full_name_kana', 'age')}),
    #     ('連絡先', {'fields': ('phone', 'email')}),
    #     ('その他', {'fields': ('memo',)}),
    # )
    readonly_fields = ('created_at',)
