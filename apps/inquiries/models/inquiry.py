# inquiries/models/inquiry.py

from django.db import models
from django.utils import timezone

from apps.persons.models import Person

from .master import InquiryMethod


class Inquiry(models.Model):

    person = models.ForeignKey(
        Person, verbose_name='個人', on_delete=models.CASCADE, related_name='inquiries'
    )
    method = models.ForeignKey(
        InquiryMethod,
        on_delete=models.PROTECT,
        verbose_name='応募方法',
    )
    content = models.TextField('問い合わせ内容', blank=True, null=True)
    created_at = models.DateTimeField('受付日時', default=timezone.now)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return f'{self.person.full_name} ({self.method})'

    class Meta:
        verbose_name = '問い合わせ'
        verbose_name_plural = '問い合わせ一覧'
