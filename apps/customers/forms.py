from django import forms
from django.core.validators import RegexValidator

from .models import Customer


class CustomerForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=15,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{10,15}$',
                message='電数字のみ10〜15桁で入力してください。',
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': '例: 09012345678'}),
    )

    class Meta:
        model = Customer
        fields = ['name', 'name_kana', 'age', 'phone', 'email', 'memo']

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None:
            if age < 20:
                raise forms.ValidationError("年齢は20歳以上で入力してください。")
        return age

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Customer.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('このメールアドレスは既に登録されています。')
        return email
