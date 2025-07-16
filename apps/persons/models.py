from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from apps.core.models import TimeStampedModel
from apps.masters.models import Branch


class Idcard(models.Model):
    name = models.CharField('名称', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '身分証'
        verbose_name_plural = '身分証'


class Person(models.Model):
    full_name = models.CharField('氏名', max_length=20, blank=False, null=False)
    full_name_kana = models.CharField('氏名カナ', max_length=20, blank=True, null=True)
    age = models.IntegerField('年齢', blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^[0-9]+$',
        message=(
            "Tel Number must be entered in the format: '09012345678'. Up to 11 digits allowed."
        ),
    )
    phone = models.CharField(
        'TEL',
        max_length=11,
        unique=True,
        blank=True,
        null=True,
        validators=[phone_regex],
    )
    email = models.EmailField(
        'Email',
        max_length=255,
        blank=True,
        null=True,
    )
    line_name = models.CharField('LINE', max_length=20, blank=True, null=True)
    description = models.TextField('説明', blank=True, null=True)
    branch = models.ForeignKey(
        Branch, verbose_name='登録店舗', on_delete=models.PROTECT, blank=True, null=True
    )
    idcard = models.ForeignKey(
        Idcard,
        verbose_name='身分証',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.full_name}'

    # def get_absolute_url(self):
    #     return reverse_lazy("person:detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = '個人'
        verbose_name_plural = '個人'
