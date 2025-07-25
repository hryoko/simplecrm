from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.inquiries.models import Interview


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = [
            'inquiry',
            'scheduled_date',
            'status',
            'result_status',
            'result_memo',
            'decided_at',
        ]

    def clean_scheduled_date(self):
        date = self.cleaned_data.get('scheduled_date')
        if date and date < timezone.now():
            raise ValidationError('面接日時は未来の日付を指定してください。')
        return date

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        decided_at = cleaned_data.get('decided_at')

        if status == 'completed' and not decided_at:
            raise ValidationError(
                '面接ステータスが完了の場合、結果入力日時を入力してください。'
            )

        return cleaned_data
