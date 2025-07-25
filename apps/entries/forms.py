from django import forms
from django.db import transaction

from apps.inquiries.forms.inquiry import InquiryForm
from apps.inquiries.forms.interview import InterviewForm
from apps.inquiries.forms.reception import ReceptionForm
from apps.persons.forms import PersonForm


class EntryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.initial = kwargs.get('initial', {})
        self.data = kwargs.get('data') if 'data' in kwargs else None
        super().__init__(*args, **kwargs)
        self.person_form = PersonForm(self.data, prefix='person')
        self.inquiry_form = InquiryForm(self.data, prefix='inquiry')
        self.reception_form = ReceptionForm(self.data, prefix='reception')
        self.interview_form = InterviewForm(self.data, prefix='interview')

    def is_valid(self):
        return (
            self.person_form.is_valid()
            and self.inquiry_form.is_valid()
            and self.reception_form.is_valid()
            and self.interview_form.is_valid()
        )

    @transaction.atomic
    def save(self):
        person = self.person_form.save()
        inquiry = self.inquiry_form.save(commit=False)
        inquiry.person = person
        inquiry.save()

        reception = self.reception_form.save(commit=False)
        reception.inquiry = inquiry
        reception.save()

        interview = self.interview_form.save(commit=False)
        interview.inquiry = inquiry
        interview.save()

        return inquiry
