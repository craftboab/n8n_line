from django.db import models
from django.utils import timezone


class LineUser(models.Model):
    """LINEユーザー情報を管理するモデル"""
    line_user_id = models.CharField(max_length=100, unique=True, verbose_name='LINE User ID')
    display_name = models.CharField(max_length=100, blank=True, verbose_name='表示名')
    picture_url = models.URLField(blank=True, verbose_name='プロフィール画像URL')
    status_message = models.CharField(max_length=200, blank=True, verbose_name='ステータスメッセージ')
    is_active = models.BooleanField(default=True, verbose_name='アクティブ')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')

    class Meta:
        verbose_name = 'LINEユーザー'
        verbose_name_plural = 'LINEユーザー'

    def __str__(self):
        return f"{self.display_name} ({self.line_user_id})"


class MessageLog(models.Model):
    """メッセージログを管理するモデル"""
    user = models.ForeignKey(LineUser, on_delete=models.CASCADE, verbose_name='ユーザー')
    message_type = models.CharField(max_length=20, verbose_name='メッセージタイプ')
    message_text = models.TextField(blank=True, verbose_name='メッセージ内容')
    raw_data = models.JSONField(default=dict, verbose_name='生データ')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='作成日時')

    class Meta:
        verbose_name = 'メッセージログ'
        verbose_name_plural = 'メッセージログ'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['message_type', 'created_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.display_name} - {self.message_type} ({self.created_at})" 