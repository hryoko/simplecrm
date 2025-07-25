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
    search_fields = ['inquiry__applicant__name', 'staff__username']
