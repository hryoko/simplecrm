from django.conf import settings
from django.db import models

from .inquiry import Inquiry


class Reception(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', '未対応'
        HANDLING = 'handling', '対応中'
        LOST_CONTACT = 'lost_contact', '連絡途絶'
        IGNORED = 'ignored', '対応不要'
        COMPLETED = 'completed', '対応完了'
        CANCELED = 'canceled', 'キャンセル'

        @classmethod
        def can_transition(cls, current_status, next_status):
            return next_status in Reception.ALLOWED_RECEPTION_STATUS_TRANSITIONS.get(
                current_status, set()
            )

    # クラス外でもアクセスできるようにここで定義
    ALLOWED_RECEPTION_STATUS_TRANSITIONS = {
        Status.NEW: {Status.HANDLING, Status.IGNORED, Status.CANCELED},
        Status.HANDLING: {
            Status.COMPLETED,
            Status.LOST_CONTACT,
            Status.IGNORED,
            Status.CANCELED,
        },
        Status.LOST_CONTACT: {
            Status.HANDLING,
            Status.COMPLETED,
            Status.IGNORED,
            Status.CANCELED,
        },
        Status.IGNORED: set(),
        Status.COMPLETED: set(),
        Status.CANCELED: set(),
    }

    inquiry = models.ForeignKey(
        Inquiry, on_delete=models.CASCADE, related_name='receptions'
    )
    remarks = models.TextField(blank=True)
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    received_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        '対応状況',
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    class Meta:
        verbose_name = '受付'
        verbose_name_plural = '受付一覧'
        ordering = ['-received_at']

    def __str__(self):
        return f"{self.inquiry} - {self.get_status_display()}"

    def update_status(self, new_status):
        if self.Status.can_transition(self.status, new_status):
            self.status = new_status
            self.save(update_fields=['status'])
            return True
        else:
            raise ValueError(
                f"ステータスを {self.get_status_display()} から {self.Status(new_status).label} に変更できません。"
            )
