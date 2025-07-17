# inquiries/models/inquiry.py

from django.db import models
from django.utils import timezone

from apps.persons.models import Person

from .master import InquiryMethod


class Inquiry(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', '未対応'
        HANDLING = 'handling', '対応中'
        COMPLETED = 'completed', '完了'
        CANCELED = 'canceled', 'キャンセル'
        LOST_CONTACT = 'lost_contact', '連絡途絶'

    person = models.ForeignKey(
        Person, verbose_name='個人', on_delete=models.CASCADE, related_name='inquiries'
    )
    method = models.ForeignKey(
        InquiryMethod,
        on_delete=models.PROTECT,
        verbose_name='応募方法',
    )
    content = models.TextField('問い合わせ内容', blank=True, null=True)
    status = models.CharField(
        '対応状況',
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    created_at = models.DateTimeField('受付日時', default=timezone.now)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return f'{self.person.full_name} ({self.method} - {self.get_status_display()})'

    class Meta:
        verbose_name = '問い合わせ'
        verbose_name_plural = '問い合わせ'
