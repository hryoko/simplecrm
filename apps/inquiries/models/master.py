from django.db import models


class InquiryMethod(models.Model):
    name = models.CharField('名称', max_length=30)
    category = models.CharField(
        'カテゴリ',
        max_length=30,
        choices=[
            ('contact', '連絡手段'),  # 電話・メール・LINEなど
            ('referral', '紹介'),  # 友人紹介・元在籍など
            ('media', '媒体'),  # 求人広告など
            ('other', 'その他'),
        ],
        default='contact',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '応募経路'
        verbose_name_plural = '応募経路'


# class InquiryType(models.Model):
#     name = models.CharField('区分名', max_length=30)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = '問い合わせ区分'
#         verbose_name_plural = '問い合わせ区分'


# class InquiryResult(models.Model):
#     name = models.CharField('結果', max_length=30)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = '問い合わせ結果'
#         verbose_name_plural = '問い合わせ結果'
