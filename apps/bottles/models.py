from django.db import models
from django.utils import timezone
from apps.customers.models import Customer


class Bottle(models.Model):
    customer = models.ForeignKey(
        Customer,
        verbose_name=('顧客'),
        on_delete=models.CASCADE,
        related_name='bottles',
    )
    name = models.CharField(
        verbose_name=('ボトル名'),
        max_length=100,
        help_text=('ボトルの銘柄名を入力してください'),
    )
    memo = models.TextField(blank=True)
    opened_at = models.DateField(
        verbose_name=('キープ日'),
        blank=True,
        help_text=('ボトルのキープ日を入力してください'),
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.customer.name}'
