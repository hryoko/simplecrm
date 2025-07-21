from django import forms

from ..models.inquiry import Inquiry


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = [
            'person',
            'method',
            'content',
        ]  # created_at は自動で設定されるので除外

        widgets = {
            'person': forms.Select(attrs={'class': 'form-select'}),
            'method': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': '問い合わせ内容を入力してください',
                }
            ),
        }

        labels = {
            'person': '応募者',
            'method': '問い合わせ手段',
            'content': '問い合わせ内容',
        }
