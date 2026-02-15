from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'message_preview', 'is_from_admin', 'admin_user', 'created_at', 'is_read']
    list_filter = ['is_from_admin', 'is_read', 'created_at']
    search_fields = ['user__username', 'user__telegram_id', 'message']
    readonly_fields = ['created_at']
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'admin_user')
