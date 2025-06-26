from django import forms
from django.utils import timezone
from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer', 'reserved_at', 'number_of_people', 'memo']
        widgets = {
            'reserved_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_reserved_at(self):
        reserved_at = self.cleaned_data.get('reserved_at')
        if reserved_at and reserved_at < timezone.now():
            raise forms.ValidationError('予約日時は未来の日付にしてください。')
        return reserved_at
