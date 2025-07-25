from django.contrib import admin

from ..forms.reception import ReceptionForm
from ..models.reception import Reception


@admin.register(Reception)
class ReceptionAdmin(admin.ModelAdmin):
    form = ReceptionForm

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = [field.name for field in model._meta.fields]

    # list_display = ['id', 'inquiry', 'staff', 'received_at', 'status']
    list_filter = ['status', 'received_at']
    search_fields = [
        'inquiry__person__name_kanji',
        'inquiry__person__name_kana',
        'inquiry__person__phone',
        'inquiry__person__email',
        'inquiry__person__line_name',
    ]
    autocomplete_fields = ['inquiry']  # 外部キー名そのまま指定
