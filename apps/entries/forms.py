# inquiries/forms/combined.py
from django import forms

from apps.inquiries.models import Inquiry, Reception
from apps.persons.models import Person


class PersonInquiryReceptionForm(forms.Form):
    # Person
    full_name = forms.CharField(label='氏名')
    full_name_kana = forms.CharField(label='氏名カナ', required=False)
    age = forms.IntegerField(label='年齢', required=False)
    phone = forms.CharField(label='電話番号', required=False)
    email = forms.EmailField(label='メールアドレス', required=False)
    line_name = forms.CharField(label='LINE名', required=False)
    branch = forms.ChoiceField(
        label='登録店舗', choices=Person.Branch.choices, required=False
    )
    idcard = forms.ChoiceField(
        label='身分証', choices=Person.IdCardType.choices, required=False
    )
    description = forms.CharField(label='説明', widget=forms.Textarea, required=False)

    # Inquiry
    method = forms.ChoiceField(
        label='問い合わせ方法', choices=Inquiry.Method.choices, required=True
    )
    content = forms.CharField(
        label='問い合わせ内容', widget=forms.Textarea, required=True
    )

    # Reception
    status = forms.ChoiceField(choices=Reception.Status.choices, label='受付ステータス')
    remarks = forms.CharField(widget=forms.Textarea, required=False, label='受付メモ')

    def __init__(self, *args, person=None, inquiry=None, reception=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.person = person
        self.inquiry = inquiry
        self.reception = reception

        if person:
            self.fields['full_name'].initial = person.full_name
            self.fields['full_name_kana'].initial = person.full_name_kana
            self.fields['phone'].initial = person.phone
            self.fields['age'].initial = person.age
            self.fields['email'].initial = person.email
            self.fields['line_name'].initial = person.line_name
            self.fields['branch'].initial = person.branch
            self.fields['idcard'].initial = person.idcard
            self.fields['description'].initial = person.description

        if inquiry:
            self.fields['method'].initial = inquiry.method
            self.fields['content'].initial = inquiry.content

        if reception:
            self.fields['status'].initial = reception.status
            self.fields['remarks'].initial = reception.remarks

    def save(self, staff=None):
        # 更新か新規か
        person = self.person or Person()
        inquiry = self.inquiry or Inquiry()
        reception = self.reception or Reception()

        # Person
        person.full_name = self.cleaned_data['full_name']
        person.full_name_kana = self.cleaned_data.get('full_name_kana')
        person.age = self.cleaned_data.get('age')
        person.phone = self.cleaned_data.get('phone')
        person.email = self.cleaned_data.get('email')
        person.line_name = self.cleaned_data.get('line_name')
        person.branch = self.cleaned_data.get('branch')
        person.idcard = self.cleaned_data.get('idcard')
        person.description = self.cleaned_data.get('description')
        person.save()

        # Inquiry
        inquiry.person = person
        inquiry.method = self.cleaned_data['method']
        inquiry.content = self.cleaned_data['content']
        inquiry.save()

        # Reception
        reception.inquiry = inquiry
        reception.staff = staff
        reception.status = self.cleaned_data['status']
        reception.remarks = self.cleaned_data.get('remarks')
        reception.save()

        return person, inquiry, reception
