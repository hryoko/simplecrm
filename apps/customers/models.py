from django.core import validators
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

# from django.db.models import Q


class Customer(models.Model):
    name = models.CharField('名前', max_length=100)
    name_kana = models.CharField('カナ', max_length=100, blank=True)
    age = models.IntegerField(
        verbose_name='年齢',
        help_text=('登録できるのは20歳以上に限ります。'),
        validators=[validators.MinValueValidator(20)],
        blank=True,
    )
    phone_regex = RegexValidator(
        regex=r'^[0-9]+$',
        message=('数字のみ10〜15桁で入力してください'),
    )
    phone = models.CharField(
        verbose_name='電話番号',
        max_length=15,
        unique=True,
        validators=[phone_regex],
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name='メールアドレス',
        max_length=63,
        unique=True,
        error_messages={
            'unique': ('そのメールアドレスはすでに登録されています。'),
        },
        blank=True,
        null=True,
    )
    memo = models.TextField('メモ', blank=True)
    created_at = models.DateTimeField('登録日', default=timezone.now)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        # verbose_name = '顧客'
        # verbose_name_plural = '顧客一覧'
        # ordering = ['name_kana']
        pass


# class PersonQuerySet(models.QuerySet):
#     # https://itc.tokyo/2021/06/27/3571/
#     # def all(self):
#     #     return super().all().select_related('office', 'idcard')

#     def lookup(self, query=None):
#         qs = self
#         qs = qs.select_related('Affiliation')

#         if query is not None:
#             or_lookup = (
#                 Q(id__icontains=query)
#                 | Q(name__icontains=query)
#                 | Q(name_kana__icontains=query)
#                 | Q(tel__icontains=query)
#                 | Q(line__icontains=query)
#                 | Q(email__icontains=query)
#                 # | Q(Affiliation__icontains=query)
#                 # | Q(description__icontains=query)
#             )
#             qs = qs.filter(or_lookup).distinct()
#         return qs.order_by("-id")

#     def sorted(self):
#         return self.order_by('-created_at')

#     # def choice(self, *query=None):
#     #     pass
#     pass
