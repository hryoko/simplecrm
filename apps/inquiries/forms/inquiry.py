from django import forms

from apps.inquiries.models import Inquiry


class InquiryForm(forms.ModelForm):

    class Meta:
        model = Inquiry
        fields = ['person', 'method', 'brand', 'content', 'previous_inquiry']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        empty = [('', '選択してください')]
        self.fields['method'].choices = empty + list(self.fields['method'].choices)
        self.fields['brand'].choices = empty + list(self.fields['brand'].choices)
