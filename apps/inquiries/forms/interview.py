# interviews/forms/interview.py
from django import forms

from ..models.interview import Interview


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
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'decided_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
