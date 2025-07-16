from core.models import TimeStampedModel
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse_lazy


class InquiryMethod(models.Model):
    method = models.CharField(max_length=20)

    def __str__(self):
        return self.method

    class Meta:
        db_table = 'r_inquiry_methods'
        verbose_name = '応募方法'
        verbose_name_plural = '応募方法'


class InquiryType(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type

    class Meta:
        db_table = 'r_inquiry_types'
        verbose_name = '問合わせ区分'
        verbose_name_plural = '問合わせ区分'


class InquiryResult(models.Model):
    result = models.CharField(max_length=20)

    def __str__(self):
        return self.result

    class Meta:
        db_table = 'r_inquiry_results'
        verbose_name = '問合わせ結果'
        verbose_name_plural = '問合わせ結果'


class Reception(TimeStampedModel):
    INTERVIEW_CONFIRM_CHOICES = (
        ('確認OK', '確認OK'),
        ('日程変更', '日程変更'),
        ('キャンセル', 'キャンセル'),
        ('辞退', '辞退'),
        ('返信なし', '返信なし'),
    )
    INTERVIEW_RESULT_CHOICES = (
        ('体験', '体験'),
        ('保留', '保留'),
        ('辞退・NG', '辞退・NG'),
        ('キャンセル', 'キャンセル'),
        ('連絡なし', '連絡なし'),
        ('日程変更', '日程変更'),
        ('後日体験予定', '後日体験予定'),
        ('身分証取得後', '身分証取得後'),
    )
    TRIAL_RESULT_CHOICES = (
        ('OK', 'OK'),
        ('辞退・NG', '辞退・NG'),
        ('保留', '保留'),
        ('確認中', '確認中'),
        ('連絡なし', '連絡なし'),
    )
    person = models.ForeignKey(Person, verbose_name='氏名', on_delete=models.CASCADE)
    branch = models.ForeignKey(
        Branch, verbose_name='店舗', blank=False, null=False, on_delete=models.CASCADE
    )
    trade = models.ForeignKey(
        Trade, verbose_name='屋号', blank=True, null=True, on_delete=models.PROTECT
    )
    method = models.ForeignKey(
        InquiryMethod,
        verbose_name='応募方法',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    type = models.ForeignKey(
        InquiryType,
        verbose_name='問合区分',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    interview_date = models.DateTimeField('面接日', blank=True, null=True)
    interview_time = models.TimeField('面接時間', blank=True, null=True)

    question = models.TextField('問合内容', blank=True, null=True)
    respond = models.TextField('対応内容', blank=True, null=True)

    inquiry_result = models.ForeignKey(
        InquiryResult,
        verbose_name='問合結果',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    interview_confirm = models.CharField(
        '面接前日確認',
        max_length=20,
        blank=True,
        null=True,
        choices=INTERVIEW_CONFIRM_CHOICES,
    )
    interview_result = models.CharField(
        '面接結果',
        max_length=20,
        blank=True,
        null=True,
        choices=INTERVIEW_RESULT_CHOICES,
    )

    trial_date = models.DateTimeField('体験日', blank=True, null=True)
    trial_result = models.CharField(
        '体験結果', max_length=20, blank=True, null=True, choices=TRIAL_RESULT_CHOICES
    )

    def __str__(self):
        return str(self.person)

    class Meta:
        db_table = 't_receptions'
        # verbose_name = ''
        # verbose_name_plural = '問合せ'

    # ticket = models.IntegerField('チケットID', blank=True, null=True)
