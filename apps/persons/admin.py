from django.contrib import admin

from .models import Idcard, Person


@admin.register(Person)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'full_name_kana',
        'age',
        'phone',
        # 'email',
        # 'line_name',
        'branch',
        'idcard',
        # 'created_at',
    )
    list_filter = ('branch', 'idcard', 'created_at')
    search_fields = ('full_name', 'full_name_kana', 'phone', 'email', 'line_name')

    # fieldsets = (
    #     ('基本情報', {'fields': ('full_name', 'full_name_kana', 'age')}),
    #     ('連絡先', {'fields': ('phone', 'email')}),
    #     ('その他', {'fields': ('memo',)}),
    # )
    readonly_fields = ('created_at',)


@admin.register(Idcard)
class IdcardAdmin(admin.ModelAdmin):
    list_display = ('name',)
