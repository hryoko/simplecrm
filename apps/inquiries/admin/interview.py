from django.contrib import admin

from ..forms.interview import InterviewForm
from ..models.interview import Interview


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    form = InterviewForm

    list_display = ['id', 'inquiry', 'scheduled_date', 'status', 'result_status']
    list_filter = ['status', 'result_status']
    search_fields = [
        'inquiry__person__name_kanji',
        'inquiry__person__name_kana',
        'inquiry__person__phone',
        'inquiry__person__email',
        'inquiry__person__line_name',
    ]
    # ordering = ['-scheduled_date']
    autocomplete_fields = ['inquiry']  # 外部キー名そのまま指定
