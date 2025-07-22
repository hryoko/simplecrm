from django.contrib import admin

from ..models.interview import Interview


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('inquiry', 'scheduled_date', 'status', 'result_status')
    list_filter = ('status', 'result_status')
    search_fields = ('inquiry__id', 'inquiry__person__full_name')
    ordering = ('-scheduled_date',)
