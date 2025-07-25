from django import forms
from django.core.exceptions import ValidationError

from ..models.reception import Reception


class ReceptionForm(forms.ModelForm):
    # reception_status = forms.ChoiceField(
    #     label='受付状況', choices=Reception.Status.choices
    # )

    class Meta:
        model = Reception
        fields = ['inquiry', 'remarks', 'staff', 'status']

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
