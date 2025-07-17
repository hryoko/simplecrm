from django import forms
from inquiries.models.reception import Reception


class ReceptionForm(forms.ModelForm):
    class Meta:
        model = Reception
        fields = ['inquiry', 'staff', 'status', 'memo']
