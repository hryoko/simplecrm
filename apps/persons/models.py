from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

# from apps.masters.models import Branch


class Person(models.Model):
    class Branch(models.IntegerChoices):
        YAKUIN = 1, '福岡薬院'
        HIROSE = 2, '仙台広瀬'
        KOKURA = 3, '北九州小倉'
        CHUO = 4, '鹿児島中央'
        HIGASHI = 5, '仙台東口'
        TENMONKAN = 6, '鹿児島天文館'
        SHINJUKU = 7, '東京新宿'

    class IdCardType(models.TextChoices):
        UNKNOWN = 'unknown', '不明'  # 未回答・不明
        NONE = 'none', '公的証なし'
        LICENSE = 'license', '運転免許証'
        PASSPORT = 'passport', 'パスポート'
        MY_NUMBER = 'my_number', 'マイナカード'
        PERMANENT_RESIDENCE = 'permanent_card', '永住カード'
        RESIDENT_CERTIFICATE = 'resident_card', '住民票'
        RESIDENCE_CARD = 'residence_card', '在留カード'  # 旧「外国人登録証明書」
        STUDENT_ID = 'student_id', '学生証'
        EMPLOYEE_ID = 'employee_id', '社員証'
        OTHER = 'other', 'その他'

    full_name = models.CharField('氏名', max_length=20, blank=False)
    full_name_kana = models.CharField('氏名カナ', max_length=20, blank=True)
    age = models.IntegerField('年齢', blank=True, null=True)
    phone = models.CharField('電話番号', max_length=11, unique=True, blank=True)
    email = models.EmailField('Email', max_length=255, blank=True)
    line_name = models.CharField('LINE名', max_length=20, blank=True)
    branch = models.IntegerField('登録店舗', choices=Branch.choices, blank=False)
    idcard = models.CharField(
        '身分証',
        max_length=20,
        choices=IdCardType.choices,
        default=IdCardType.UNKNOWN,
        blank=True,
        help_text='「その他」を選ばれた場合は、備考欄に身分証の「種類」または「名称」をご入力ください。',
    )
    description = models.TextField('説明', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.full_name}'

    def get_object_label(self):
        return self.full_name

    # def get_absolute_url(self):
    #     return reverse_lazy("person:detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = '個人'
        verbose_name_plural = '個人一覧'
