from django.conf import settings
from django.db import models

from .inquiry import Inquiry


class Reception(models.Model):
    STATUS_CHOICES = [
        ('pending', '未対応'),
        ('responded', '対応済み'),
        ('ignored', '対応不要'),
    ]

    inquiry = models.ForeignKey(
        Inquiry, on_delete=models.CASCADE, related_name='receptions'
    )
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    received_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    memo = models.TextField(blank=True)

    class Meta:
        verbose_name = '受付'
        verbose_name_plural = '受付一覧'
        ordering = ['-received_at']

    def __str__(self):
        return f"{self.inquiry} - {self.get_status_display()}"
