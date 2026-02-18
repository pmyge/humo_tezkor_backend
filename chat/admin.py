from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'message_preview', 'image_preview', 'is_from_admin', 'reply_link', 'created_at', 'is_read']
    list_filter = ['user', 'is_from_admin', 'is_read', 'created_at']
    search_fields = ['user__username', 'user__telegram_id', 'message']
    readonly_fields = ['created_at']

    @admin.display(description='Image')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 4px;" />', obj.image.url)
        return ""
    
    @admin.display(description='Message')
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    
    @admin.display(description='Reply')
    def reply_link(self, obj):
        if obj.is_from_admin:
            return ""
        url = reverse('admin:chat_chatmessage_add') + f"?user={obj.user.id}&is_from_admin=1"
        return format_html('<a class="button" href="{}">Javob yozish</a>', url)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'admin_user')
