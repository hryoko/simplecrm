from django.db import models


class Branch(models.Model):
    name = models.CharField('支店名', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '支店'
        verbose_name_plural = '支店'


class Brand(models.Model):
    name = models.CharField('屋号', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '屋号'
        verbose_name_plural = '屋号'


# class Idcard(models.Model):
#     name = models.CharField('身分証', max_length=20)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = '身分証'
#         verbose_name_plural = '身分証'
