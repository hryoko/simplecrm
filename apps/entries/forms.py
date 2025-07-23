import re

from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.inquiries.models import Inquiry, Interview, Reception
from apps.persons.models import Person

from .models import Entry


class EntryForm(forms.ModelForm):
    # --- Person fields ---
    full_name = forms.CharField(label='氏名')
    full_name_kana = forms.CharField(label='氏名カナ', required=False)
    age = forms.IntegerField(label='年齢', min_value=18, required=False)
    phone = forms.CharField(label='電話番号')
    email = forms.EmailField(label='Email', required=False)
    line_name = forms.CharField(label='LINE', required=False)
    branch = forms.ChoiceField(
        label='登録店舗',
        choices=[('', '選択してください')] + list(Person.Branch.choices),
        required=True,
    )
    idcard = forms.ChoiceField(
        label='身分証',
        choices=[('', '選択してください')] + list(Person.IdCardType.choices),
    )
    description = forms.CharField(label='説明', widget=forms.Textarea, required=False)

    # --- Inquiry fields ---
    inquiry_method = forms.ChoiceField(
        label='問い合わせ方法',
        choices=[('', '選択してください')] + list(Inquiry.Method.choices),
        required=True,
    )
    inquiry_brand = forms.CharField(label='ブランド', required=False)
    inquiry_content = forms.CharField(
        label='問い合わせ内容', widget=forms.Textarea, required=False
    )

    # --- Reception fields ---
    reception_status = forms.ChoiceField(
        label='受付状況', choices=Reception.Status.choices
    )
    reception_remarks = forms.CharField(
        label='受付メモ', widget=forms.Textarea, required=False
    )

    # --- Interview fields ---
    interview_scheduled_date = forms.DateTimeField(label='面接日時')
    interview_status = forms.ChoiceField(
        label='面接ステータス', choices=Interview.Status.choices
    )
    interview_result_status = forms.ChoiceField(
        label='面接結果', choices=Interview.ResultStatus.choices, required=False
    )
    interview_result_memo = forms.CharField(
        label='結果メモ', widget=forms.Textarea, required=False
    )
    interview_decided_at = forms.DateTimeField(label='結果入力日時', required=False)

    class Meta:
        model = Entry
        fields = []  # モデルのフィールドは直接使わず、手動で管理する

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 更新モード時、初期値を設定
        instance = kwargs.get('instance')
        if instance:
            self.fields['full_name'].initial = instance.person.full_name
            self.fields['full_name_kana'].initial = instance.person.full_name_kana
            self.fields['age'].initial = instance.person.age
            self.fields['phone'].initial = instance.person.phone
            self.fields['email'].initial = instance.person.email
            self.fields['line_name'].initial = instance.person.line_name
            self.fields['branch'].initial = instance.person.branch
            self.fields['idcard'].initial = instance.person.idcard
            self.fields['description'].initial = instance.person.description

            self.fields['inquiry_method'].initial = instance.inquiry.method
            self.fields['inquiry_brand'].initial = instance.inquiry.brand
            self.fields['inquiry_content'].initial = instance.inquiry.content

            self.fields['reception_status'].initial = instance.reception.status
            self.fields['reception_remarks'].initial = instance.reception.remarks

            interview = Interview.objects.filter(inquiry=instance.inquiry).first()
            if interview:
                self.fields['interview_scheduled_date'].initial = (
                    interview.scheduled_date
                )
                self.fields['interview_status'].initial = interview.status
                self.fields['interview_result_status'].initial = interview.result_status
                self.fields['interview_result_memo'].initial = interview.result_memo
                self.fields['interview_decided_at'].initial = interview.decided_at

    @transaction.atomic
    def save(self, commit=True):
        if self.instance and self.instance.pk:
            # 更新処理
            person = self.instance.person
            person.full_name = self.cleaned_data['full_name']
            person.full_name_kana = self.cleaned_data['full_name_kana']
            person.age = self.cleaned_data['age']
            person.phone = self.cleaned_data['phone']
            person.email = self.cleaned_data['email']
            person.line_name = self.cleaned_data['line_name']
            person.branch = self.cleaned_data['branch']
            person.idcard = self.cleaned_data['idcard']
            person.description = self.cleaned_data['description']
            person.save()

            inquiry = self.instance.inquiry
            inquiry.method = self.cleaned_data['inquiry_method']
            inquiry.brand = self.cleaned_data['inquiry_brand']
            inquiry.content = self.cleaned_data['inquiry_content']
            inquiry.save()

            reception = self.instance.reception
            reception.status = self.cleaned_data['reception_status']
            reception.remarks = self.cleaned_data['reception_remarks']
            reception.save()

            interview = Interview.objects.filter(inquiry=inquiry).first()
            if interview:
                interview.scheduled_date = self.cleaned_data['interview_scheduled_date']
                interview.status = self.cleaned_data['interview_status']
                interview.result_status = self.cleaned_data['interview_result_status']
                interview.result_memo = self.cleaned_data['interview_result_memo']
                interview.decided_at = self.cleaned_data['interview_decided_at']
                interview.save()
            else:
                Interview.objects.create(
                    inquiry=inquiry,
                    scheduled_date=self.cleaned_data['interview_scheduled_date'],
                    status=self.cleaned_data['interview_status'],
                    result_status=self.cleaned_data['interview_result_status'],
                    result_memo=self.cleaned_data['interview_result_memo'],
                    decided_at=self.cleaned_data['interview_decided_at'],
                )

            return self.instance
        else:
            # 新規登録処理
            person = getattr(self, 'existing_person', None)

            if person:
                # 既存を更新
                person.full_name = self.cleaned_data['full_name']
                person.full_name_kana = self.cleaned_data['full_name_kana']
                person.age = self.cleaned_data['age']
                person.email = self.cleaned_data['email']
                person.line_name = self.cleaned_data['line_name']
                person.branch = self.cleaned_data['branch']
                person.idcard = self.cleaned_data['idcard']
                person.description = self.cleaned_data['description']
                person.save()
            else:
                # 新規作成
                person = Person.objects.create(
                    full_name=self.cleaned_data['full_name'],
                    full_name_kana=self.cleaned_data['full_name_kana'],
                    age=self.cleaned_data['age'],
                    phone=self.cleaned_data['phone'],
                    email=self.cleaned_data['email'],
                    line_name=self.cleaned_data['line_name'],
                    branch=self.cleaned_data['branch'],
                    idcard=self.cleaned_data['idcard'],
                    description=self.cleaned_data['description'],
                )

            inquiry = Inquiry.objects.create(
                person=person,
                method=self.cleaned_data['inquiry_method'],
                brand=self.cleaned_data['inquiry_brand'],
                content=self.cleaned_data['inquiry_content'],
            )

            reception = Reception.objects.create(
                inquiry=inquiry,
                status=self.cleaned_data['reception_status'],
                remarks=self.cleaned_data['reception_remarks'],
            )

            Interview.objects.create(
                inquiry=inquiry,
                scheduled_date=self.cleaned_data['interview_scheduled_date'],
                status=self.cleaned_data['interview_status'],
                result_status=self.cleaned_data['interview_result_status'],
                result_memo=self.cleaned_data['interview_result_memo'],
                decided_at=self.cleaned_data['interview_decided_at'],
            )

            entry = Entry.objects.create(
                person=person,
                inquiry=inquiry,
                reception=reception,
            )

            return entry

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

    def clean_interview_scheduled_date(self):
        date = self.cleaned_data.get('interview_scheduled_date')
        if date and date < timezone.now():
            raise ValidationError('面接日時は未来の日付を指定してください。')
        return date

    def clean_reception_status(self):
        new_status = self.cleaned_data.get('reception_status')
        current_status = None
        # Entryモデルにreceptionがあるならcurrent_status取得
        if self.instance and hasattr(self.instance, 'reception'):
            current_status = self.instance.reception.status

        if current_status and not Reception.Status.can_transition(
            current_status, new_status
        ):
            raise ValidationError(
                f'ステータスを {current_status} から {new_status} に変更できません。'
            )
        return new_status

    def clean(self):
        cleaned_data = super().clean()

        status = cleaned_data.get('interview_status')
        decided_at = cleaned_data.get('interview_decided_at')

        if status == 'completed' and not decided_at:
            raise ValidationError(
                '面接ステータスが完了の場合、結果入力日時を入力してください。'
            )

        return cleaned_data
