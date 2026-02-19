from django.contrib import admin
from django.utils.html import format_html, escape
from django.utils.safestring import mark_safe
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
    list_filter = ['is_from_admin', 'is_read', 'created_at']
    search_fields = ['user__username', 'message']
    list_per_page = 15
    readonly_fields = ['created_at', 'history_viewer']
 bitumen

    fieldsets = (
        ('Xabar ma\'lumoti', {
            'fields': ('user', 'message', 'image', 'is_from_admin', 'admin_user', 'is_read', 'created_at')
        }),
        ('Javob yozish', {
            'fields': ('reply_text',),
            'classes': ('wide',),
        }),
        ('Suhbat tarixi', {
            'fields': ('history_viewer',),
        }),
    )

    @admin.display(description='Rasm')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 4px;" />', obj.image.url)
        return ""

    @admin.display(description='Xabar')
    def message_preview(self, obj):
        msg = obj.message or ''
        return (msg[:50] + '...') if len(msg) > 50 else msg

    @admin.display(description='Javob')
    def reply_link(self, obj):
        if obj.is_from_admin:
            return ""
        url = reverse('admin:chat_chatmessage_change', args=[obj.id])
        return format_html('<a class="button" href="{}">Javob yozish</a>', url)

    @admin.display(description='Suhbat tarixi')
    def history_viewer(self, obj):
        if not obj or not obj.pk or not obj.user:
            return "Tarix yo'q"

        messages = ChatMessage.objects.filter(user=obj.user).order_by('created_at')[:20]
        parts = ['<div style="max-height:320px;overflow-y:auto;border:1px solid #ddd;padding:10px;border-radius:6px;background:#f9f9f9;">']

        for m in messages:
            bg = '#d1ecf1' if not m.is_from_admin else '#d4edda'
            align = 'right' if not m.is_from_admin else 'left'
            sender = escape(str(m.user)) if not m.is_from_admin else 'Admin'
            time_str = m.created_at.strftime('%d.%m %H:%M') if m.created_at else ''
            msg_text = escape(m.message or '')

            parts.append(
                f'<div style="text-align:{align};margin-bottom:8px;">'
                f'<small style="color:#888;">{sender} – {time_str}</small><br>'
                f'<span style="display:inline-block;padding:6px 10px;border-radius:10px;'
                f'background:{bg};max-width:80%;word-wrap:break-word;text-align:left;">'
            )
            if m.image:
                img_url = escape(m.image.url)
                parts.append(f'<img src="{img_url}" style="max-width:120px;display:block;margin-bottom:4px;border-radius:4px;"><br>')
            parts.append(f'{msg_text}</span></div>')

        parts.append('</div>')
        return mark_safe(''.join(parts))

    def save_model(self, request, obj, form, change):
        reply_text = form.cleaned_data.get('reply_text', '').strip()
        super().save_model(request, obj, form, change)
        if reply_text:
            ChatMessage.objects.create(
                user=obj.user,
                message=reply_text,
                is_from_admin=True,
                admin_user=request.user,
            )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'admin_user')
