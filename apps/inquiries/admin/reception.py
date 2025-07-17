from django.contrib import admin

from ..models.reception import Reception


@admin.register(Reception)
class ReceptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'inquiry', 'staff', 'received_at', 'status']
    list_filter = ['status', 'received_at']
    search_fields = ['inquiry__applicant__name', 'staff__username']
