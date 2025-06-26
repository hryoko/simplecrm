from django.db import models
from django.utils import timezone
from apps.customers.models import Customer


class Reservation(models.Model):
    customer = models.ForeignKey(
        Customer,
        verbose_name='顧客',
        on_delete=models.CASCADE,
        related_name='reservations',
    )
    reserved_at = models.DateTimeField(
        verbose_name='予約日時',
        help_text='予約日時を選択してください。',
    )
    number_of_people = models.PositiveIntegerField(
        verbose_name='人数',
        default=1,
    )
    memo = models.TextField(
        verbose_name='メモ',
        blank=True,
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '予約'
        verbose_name_plural = '予約'

    def __str__(self):
        return f"{self.customer.name} - {self.reserved_at.strftime('%Y-%m-%d %H:%M')}"
