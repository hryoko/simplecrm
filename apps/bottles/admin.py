from django.contrib import admin
from .models import Bottle


@admin.register(Bottle)
class BottleAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer', 'opened_at', 'created_at')
    search_fields = ('name', 'customer__name')
