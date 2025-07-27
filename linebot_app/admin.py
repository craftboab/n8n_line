from django.contrib import admin
from .models import LineUser, MessageLog


@admin.register(LineUser)
class LineUserAdmin(admin.ModelAdmin):
    list_display = ['line_user_id', 'display_name', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['line_user_id', 'display_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本情報', {
            'fields': ('line_user_id', 'display_name', 'picture_url', 'status_message')
        }),
        ('ステータス', {
            'fields': ('is_active',)
        }),
        ('日時', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'message_type', 'message_text', 'created_at']
    list_filter = ['message_type', 'created_at', 'user']
    search_fields = ['message_text', 'user__display_name', 'user__line_user_id']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    list_per_page = 50
    
    fieldsets = (
        ('メッセージ情報', {
            'fields': ('user', 'message_type', 'message_text')
        }),
        ('詳細データ', {
            'fields': ('raw_data',),
            'classes': ('collapse',)
        }),
        ('日時', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """パフォーマンス最適化"""
        return super().get_queryset(request).select_related('user') 