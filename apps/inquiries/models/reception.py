from django.conf import settings
from django.db import models

from .inquiry import Inquiry


class Reception(models.Model):
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

    inquiry = models.ForeignKey(
        Inquiry,
        verbose_name='問い合わせ',
        on_delete=models.CASCADE,
        related_name='receptions',
    )
    remarks = models.TextField(verbose_name='受付メモ', blank=True)
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='スタッフ',
        on_delete=models.PROTECT,
        blank=True,
    )
    received_at = models.DateTimeField(verbose_name='受付日時', auto_now_add=True)
    status = models.CharField(
        '対応状況', max_length=20, choices=Status.choices, default=Status.NEW
    )

    class Meta:
        verbose_name = '受付'
        verbose_name_plural = '受付一覧'
        ordering = ['-received_at']

    def __str__(self):
        return f"{self.inquiry} - {self.get_status_display()}"

    def update_status(self, new_status):
        if self.Status.can_transition(self.status, new_status):
            self.status = new_status
            self.save(update_fields=['status'])
            return True
        else:
            raise ValueError(
                f"ステータスを {self.get_status_display()} から {self.Status(new_status).label} に変更できません。"
            )
