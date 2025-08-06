from django.conf import settings
from django.db import models

from ..inquiries.models import Inquiry, Interview
from ..persons.models import Person


class Entry(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    inquiry = models.OneToOneField(Inquiry, on_delete=models.CASCADE)
    interview = models.OneToOneField(
        Interview, on_delete=models.SET_NULL, null=True, blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('new', '新規'),
            ('pending', '保留'),
            ('completed', '完了'),
        ],
        default='new',
    )

    memo = models.TextField(blank=True)

    class Meta:
        verbose_name = 'エントリ'
        verbose_name_plural = 'エントリ'

    def __str__(self):
        return f"Entry #{self.id} ({self.person})"
