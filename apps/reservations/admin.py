from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'reserved_at', 'number_of_people', 'created_at')
    search_fields = ('customer__name',)
    list_filter = ('reserved_at',)
