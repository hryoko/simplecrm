from django import forms
from django.core.exceptions import ValidationError

from ..models import Inquiry


class InquiryForm(forms.ModelForm):

    class Meta:
        model = Inquiry
        fields = ['person', 'method', 'brand', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        empty = [('', '選択してください')]
        self.fields['method'].choices = empty + list(self.fields['method'].choices)
        self.fields['brand'].choices = empty + list(self.fields['brand'].choices)

    def clean_status(self):
        new_status = self.cleaned_data.get('status')
        current_status = None
        if self.instance and hasattr(self.instance, 'status'):
            current_status = self.instance.status
        if current_status and not Reception.Status.can_transition(
            current_status, new_status
        ):
            raise ValidationError(
                f'ステータスを {current_status} から {new_status} に変更できません。'
            )
        return new_status
