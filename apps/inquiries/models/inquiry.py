from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.persons.models import Person


class Inquiry(models.Model):
    # --- 定義内クラス（TextChoices） ---
    class Brand(models.TextChoices):
        ALICE = 'alice', 'アリス'
        ROSE = 'rose', 'ローズ'
        ADELE = 'adele', 'アデル'
        LABO = 'labo', 'ラボ'
        MYCHANNEL = 'mychannel', 'Myチャネ'
        UNKNOWN = 'unknown', '不明'
        OUTREACH = 'outreach', '掘起'

    class Method(models.TextChoices):
        LINE = 'line', 'LINE'
        PHONE = 'phone', '電話'
        EMAIL = 'email', 'メール'
        FRIEND = 'friend', '友人紹介'
        OTHER = 'other', '他社紹介'
        REAPPLY = 'reapply', '再応募'

    class Status(models.TextChoices):
        NEW = 'new', '未対応'
        HANDLING = 'handling', '対応中'
        PENDING = 'pending', '保留'
        REJECTED = 'rejected', '不採用'
        DECLINED = 'declined', '辞退'
        RESCHEDULED = 'rescheduled', '日程変更'
        UNDER_CONSIDERATION = 'under_consideration', '検討中'
        LOST_CONTACT = 'lost_contact', '連絡途絶'
        IGNORED = 'ignored', '対応不要'
        DECIDED = 'decided', '面接決定'  # 面接に進むと決まった
        COMPLETED = 'completed', '対応完了'  # 問い合わせ完了（終了）
        CANCELED = 'canceled', 'キャンセル'

        @classmethod
        def can_transition(cls, current_status, next_status):
            return next_status in Reception.ALLOWED_RECEPTION_STATUS_TRANSITIONS.get(
                current_status, set()
            )

    # クラス外でもアクセスできるようにここで定義
    # 対応状況ステータスの許可された状態遷移ルールを定義する辞書
    # キー：現在のステータス（Statusの値）
    # バリュー：現在のステータスから遷移可能なステータスの集合（set）
    ALLOWED_RECEPTION_STATUS_TRANSITIONS = {
        # 新規受付時は、対応開始・不要・キャンセルの3つに遷移可能
        Status.NEW: {
            Status.HANDLING,  # 対応開始
            Status.IGNORED,  # 対応不要と判断
            Status.CANCELED,  # 申込者側キャンセル
        },
        # 対応中からは、さまざまな最終状態へ遷移可能
        Status.HANDLING: {
            Status.DECIDED,  # 面接決定
            Status.COMPLETED,  # 問い合わせ対応完了（面接しない）
            Status.LOST_CONTACT,  # 音信不通
            Status.IGNORED,  # 対応不要と判断（状況変化など）
            Status.CANCELED,  # 申込者側キャンセル
        },
        # 面接が決定した後は、結果に応じた遷移が可能
        Status.DECIDED: {
            Status.COMPLETED,  # 面接後の対応完了
            Status.CANCELED,  # キャンセル（来社辞退など）
            Status.LOST_CONTACT,  # 連絡途絶（未来社）
        },
        # 連絡が途絶えた場合も、再連絡がつけば再開可能
        Status.LOST_CONTACT: {
            Status.HANDLING,  # 再対応開始
            Status.DECIDED,  # 面接が決定する
            Status.COMPLETED,  # 状況を確認のうえ完了とする
            Status.IGNORED,  # 対応不要
            Status.CANCELED,  # キャンセル扱いにする
        },
        # 対応不要にしたものは、それ以上遷移しない（固定）
        Status.IGNORED: set(),
        # 完了したものも、基本的に固定
        Status.COMPLETED: set(),
        # キャンセルも固定
        Status.CANCELED: set(),
    }

    # --- 基本 ---
    person = models.ForeignKey(
        Person,
        verbose_name='個人',
        on_delete=models.PROTECT,
        related_name='person_inquiries',
    )
    method = models.CharField(
        max_length=20,
        choices=Method.choices,
        verbose_name='応募方法',
        blank=False,
    )
    brand = models.CharField(
        max_length=20,
        choices=Brand.choices,
        verbose_name='屋号',
        blank=False,
    )
    content = models.TextField('問い合わせ内容', blank=True, null=True)

    # --- スタッフと対応状況 ---
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='スタッフ',
        on_delete=models.PROTECT,
        blank=False,
    )
    status = models.CharField(
        '対応状況', max_length=20, choices=Status.choices, default=Status.NEW
    )

    # --- 日付 ---
    received_at = models.DateTimeField('受付日時', default=timezone.now)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    # --- 関連・メモ ---
    previous_inquiry = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, editable=False
    )
    remarks = models.TextField(verbose_name='内容メモ', blank=True)

    # --- メソッド ---
    def save(self, *args, **kwargs):
        if not self.previous_inquiry and self.person and self.brand:
            previous = (
                Inquiry.objects.filter(
                    person=self.person,
                    brand=self.brand,
                    received_at__lt=self.received_at,
                )
                .exclude(id=self.id)
                .order_by('-received_at')
                .first()
            )
            self.previous_inquiry = previous
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.person.name_kanji}（{self.get_method_display()} / {self.get_brand_display()}）'

    class Meta:
        verbose_name = '問い合わせ'
        verbose_name_plural = '問い合わせ一覧'
        ordering = ['-received_at']
