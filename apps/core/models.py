from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """
    created,modifiedフィールドを更新する抽象基底クラス
    """

    # created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # db化されない
