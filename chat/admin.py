from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django import forms
from .models import ChatMessage


class ChatMessageAdminForm(forms.ModelForm):
    reply_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'style': 'width: 100%;'}),
        required=False,
        label="Javob yozish",
        help_text="Foydalanuvchiga javob yozing va 'Save' tugmasini bosing."
    )

    class Meta:
        model = ChatMessage
        fields = '__all__'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    form = ChatMessageAdminForm
    list_display = ['user', 'message_preview', 'image_preview', 'is_from_admin', 'reply_link', 'created_at', 'is_read']
    list_filter = ['user', 'is_from_admin', 'is_read', 'created_at']
    search_fields = ['user__username', 'user__telegram_id', 'message']
    readonly_fields = ['created_at', 'history_viewer']
    
    fieldsets = (
        ('Message Info', {
            'fields': ('user', 'message', 'image', 'is_from_admin', 'admin_user', 'is_read', 'created_at')
        }),
        ('Reply to User', {
            'fields': ('reply_text',),
            'classes': ('wide',),
        }),
        ('Conversation History', {
            'fields': ('history_viewer',),
        }),
    )

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
        url = reverse('admin:chat_chatmessage_change', args=[obj.id])
        return format_html('<a class="button" href="{}">Javob yozish</a>', url)

    @admin.display(description='History')
    def history_viewer(self, obj):
        if not obj or not obj.user:
            return "No history"
        
        messages = ChatMessage.objects.filter(user=obj.user).order_by('-created_at')[:10]
        html = ['<div style="max-height: 300px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; border-radius: 4px; background: #f9f9f9;">']
        
        for m in reversed(messages):
            color = "#e3f2fd" if not m.is_from_admin else "#f1f1f1"
            align = "right" if not m.is_from_admin else "left"
            sender = "Foydalanuvchi" if not m.is_from_admin else "Admin"
            
            html.append(f'<div style="text-align: {align}; margin-bottom: 10px;">')
            html.append(f'<span style="font-size: 10px; color: #888;">{sender} - {m.created_at.strftime("%H:%M")}</span><br/>')
            html.append(f'<div style="display: inline-block; padding: 6px 10px; border-radius: 10px; background: {color}; max-width: 80%; word-wrap: break-word;">')
            if m.image:
                html.append(f'<img src="{m.image.url}" style="max-width: 100px; display: block; margin-bottom: 5px; border-radius: 4px;"/><br/>')
            html.append(f'{m.message}</div></div>')
            
        html.append('</div>')
        return format_html("".join(html))

    def save_model(self, request, obj, form, change):
        reply_text = form.cleaned_data.get('reply_text')
        
        # Save the current object first (e.g. mark as read)
        super().save_model(request, obj, form, change)
        
        if reply_text:
            # Create a NEW message from admin to user
            ChatMessage.objects.create(
                user=obj.user,
                message=reply_text,
                is_from_admin=True,
                admin_user=request.user if hasattr(request.user, 'id') else None
            )
            # Clear reply_text for next view (though it depends on redirect)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'admin_user')
