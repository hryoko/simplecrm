# from django.db import models

# class InquiryMethod(models.Model):
#     code = models.CharField(max_length=20, primary_key=True)  # 主キーを code にする
#     name = models.CharField(max_length=50)
#     category = models.CharField(
#         'カテゴリ',
#         max_length=30,
#         choices=[
#             ('contact', '直接連絡'),  # 電話・メール・LINEなど
#             ('referral', '紹介'),  # 友人紹介・元在籍など
#             ('media', '媒体'),  # 求人広告など
#             ('other', 'その他'),
#         ],
#         default='contact',
#     )
#     order = models.PositiveIntegerField(default=0)

#     class Meta:
#         verbose_name = '応募経路'
#         verbose_name_plural = '応募経路'

#     def __str__(self):
#         return self.name
