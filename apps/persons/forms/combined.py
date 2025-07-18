# inquiries/forms/combined.py
from django import forms

from apps.inquiries.models import Inquiry, InquiryMethod, Reception
from apps.masters.models import Branch, Idcard
from apps.persons.models import Person


class PersonInquiryReceptionForm(forms.Form):
    # Person
    full_name = forms.CharField(label='氏名')
    full_name_kana = forms.CharField(required=False, label='氏名カナ')
    age = forms.IntegerField(required=False, label='年齢')
    phone = forms.CharField(required=False, label='電話番号')
    email = forms.EmailField(required=False, label='E-mail')
    line_name = forms.CharField(required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)

    # ForeignKeyフィールド
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        required=False,
        label='登録店舗',
        # empty_label="選択してください",
    )

    idcard = forms.ModelChoiceField(
        queryset=Idcard.objects.all(),
        required=False,
        label='身分証',
        # empty_label="選択してください",
    )
    # Inquiry
    method = forms.ModelChoiceField(
        queryset=InquiryMethod.objects.all(), label='問い合わせ方法'
    )
    content = forms.CharField(
        widget=forms.Textarea, required=True, label='問い合わせ内容'
    )

    # Reception
    status = forms.ChoiceField(choices=Reception.Status.choices, label='受付ステータス')
    remarks = forms.CharField(widget=forms.Textarea, required=False, label='受付メモ')

    def save(self, staff=None):
        # Person
        person, _ = Person.objects.get_or_create(
            phone=self.cleaned_data['phone'],
            defaults={
                'full_name': self.cleaned_data['full_name'],
                'full_name_kana': self.cleaned_data.get('full_name_kana'),
                'age': self.cleaned_data.get('age'),
                'email': self.cleaned_data.get('email'),
                'line_name': self.cleaned_data.get('line_name'),
                'description': self.cleaned_data.get('description'),
            },
        )

        # Inquiry
        inquiry = Inquiry.objects.create(
            person=person,
            method=self.cleaned_data['method'],
            content=self.cleaned_data['content'],
        )

        # Reception
        reception = Reception.objects.create(
            inquiry=inquiry,
            staff=staff,
            status=self.cleaned_data['status'],
            remarks=self.cleaned_data.get('remarks', ''),
        )

        return person, inquiry, reception
