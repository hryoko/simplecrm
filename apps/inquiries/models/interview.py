from django.db import models

from .inquiry import Inquiry


class Interview(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', '予定'
        COMPLETED = 'completed', '完了'
        CANCELED = 'canceled', 'キャンセル'

    class ResultStatus(models.TextChoices):
        PASS = 'pass', '合格'
        FAIL = 'fail', '不合格'
        PENDING = 'pending', '保留'
        NO_SHOW = 'no_show', '無断欠席'

    inquiry = models.ForeignKey(
        Inquiry, on_delete=models.CASCADE, related_name='interviews'
    )
    scheduled_date = models.DateTimeField('面接日時')
    status = models.CharField('面接ステータス', choices=Status.choices, max_length=20)
    result_status = models.CharField(
        '結果', choices=ResultStatus.choices, max_length=20, blank=True, null=True
    )
    result_memo = models.TextField('結果メモ', blank=True, null=True)
    decided_at = models.DateTimeField('結果入力日時', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '面接'
        verbose_name_plural = '面接一覧'
