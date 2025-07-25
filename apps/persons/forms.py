import re

from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Person


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = [
            'full_name',
            'full_name_kana',
            'age',
            'phone',
            'email',
            'line_name',
            'branch',
            'idcard',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        empty = [('', '選択してください')]
        self.fields['branch'].choices = empty + list(self.fields['branch'].choices)
        self.fields['idcard'].choices = empty + list(self.fields['idcard'].choices)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')

        if not phone:
            return phone

        # 全角数字→半角数字
        phone = phone.translate(str.maketrans('０１２３４５６７８９', '0123456789'))

        # 数字以外除去
        phone = re.sub(r'[^\d]', '', phone)

        if not re.match(r'^\d{10,11}$', phone):
            raise ValidationError('電話番号は10〜11桁の半角数字で入力してください。')

        # 同一電話番号の既存 Person がいれば再利用
        existing = Person.objects.filter(phone=phone).first()
        if existing and not self.instance.pk:
            self.existing_person = existing  # 保存時に使う
        return phone

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age < 18:
            raise ValidationError('年齢は18歳以上で入力してください。')
        return age

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return email
        qs = Person.objects.filter(email=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('このメールアドレスは既に登録されています。')
        return email

    @transaction.atomic
    def save(self, commit=True):
        person = getattr(self, 'existing_person', None)

        if person:
            # 既存データの更新
            for field in self.Meta.fields:
                setattr(person, field, self.cleaned_data[field])
            if commit:
                person.save()
                print("save: instance =", self.instance)
                print("model =", self._meta.model)
            return person
        else:
            # 通常の保存（新規）
            print("save: instance =", self.instance)
            print("model =", self._meta.model)
            return super().save(commit=commit)
