from django.db import models
from django.utils import timezone

from apps.persons.models import Person


class Inquiry(models.Model):

    class Brand(models.TextChoices):
        ALICE = 'alice', 'アリス'
        ROSE = 'rose', 'ローズ'
        ADELE = 'adele', 'アデル'
        LABO = 'labo', 'ラボ'
        MYCHANNEL = 'mychannel', 'Myチャネ'
        UNKNOWN = 'unknown', '不明'
        OUTREACH = 'outreach', '掘起'

    class Method(models.TextChoices):
        LINE = 'line', 'LINE'
        PHONE = 'phone', '電話'
        EMAIL = 'email', 'メール'
        FRIEND = 'friend', '友人紹介'
        OTHER = 'other', '他社紹介'
        REAPPLY = 'reapply', '再応募'

    person = models.ForeignKey(
        Person,
        verbose_name='個人',
        on_delete=models.PROTECT,
        related_name='person_inquiries',
    )
    brand = models.CharField(
        max_length=20,
        choices=Brand.choices,
        verbose_name='屋号',
        blank=True,
    )
    method = models.CharField(
        max_length=20,
        choices=Method.choices,
        verbose_name='応募方法',
        blank=True,
    )
    content = models.TextField('問い合わせ内容', blank=True, null=True)
    received_at = models.DateTimeField('受付日時', default=timezone.now)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return f'{self.person.full_name} ({self.method})'

    # class Meta:
    # verbose_name = '問い合わせ'
    # verbose_name_plural = '問い合わせ一覧'
