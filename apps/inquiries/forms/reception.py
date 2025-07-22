from django import forms

from ..models.reception import Reception


class ReceptionForm(forms.ModelForm):
    class Meta:
        model = Reception
        fields = ['inquiry', 'remarks', 'staff', 'status']

    def __init__(self, *args, **kwargs):
        self.instance: Reception = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean_status(self):
        new_status = self.cleaned_data['status']
        current_status = self.instance.status if self.instance else None

        if current_status and not Reception.Status.can_transition(
            current_status, new_status
        ):
            raise forms.ValidationError(
                f'ステータスを {current_status} から {new_status} に変更できません。'
            )
        return new_status
