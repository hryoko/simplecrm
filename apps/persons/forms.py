import re

from django import forms
from django.core.validators import RegexValidator

from .models import Person  # モデルを使っている場合


class PersonForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=15,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{10,15}$',
                message='電数字のみ10〜11桁で入力してください。',
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': '例: 09012345678'}),
    )

    class Meta:
        model = Person
        fields = [
            'full_name',
            'full_name_kana',
            'age',
            'phone',
            'email',
            'line_name',
            'description',
            'branch',
            'idcard',
        ]

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')

        # 全角→半角変換
        phone = phone.translate(str.maketrans('０１２３４５６７８９', '0123456789'))

        # 数字以外（ハイフン・空白など）を除去
        phone = re.sub(r'[^\d]', '', phone)

        # バリデーション：10桁または11桁の数字のみ
        if not re.match(r'^\d{10,11}$', phone):
            raise forms.ValidationError(
                '電話番号は10〜11桁の半角数字で入力してください。'
            )

        return phone

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None:
            if age < 18:
                raise forms.ValidationError("年齢は18歳以上で入力してください。")
        return age

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Person.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('このメールアドレスは既に登録されています。')
        return email
