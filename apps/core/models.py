from django.db import models
from django.utils import timezone

# from datetime import datetime


class TimeStampedModel(models.Model):
    """
    created,modifiedフィールドを更新する抽象基底クラス
    """

    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        auto_now = kwargs.pop('updated_at_auto_now', True)
        if auto_now:
            # self.updated_at = datetime.now()
            self.updated_at = timezone.now()
        super(TimeStampedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True  # db化されない


# from django.db import models
# from core.models import TimeStampedModel

# class Flavor(TimeStampedModel):
#     title = models.CharField(max_length=200)


# Django SQL データベース INSERT UPDATE 追加更新方法 save() create() add() update()
# https://opendata-web.site/blog/entry/22/
