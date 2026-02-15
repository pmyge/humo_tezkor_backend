from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('telegram_user_id', 'first_name', 'last_name', 'phone_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('telegram_user_id', 'first_name', 'last_name', 'phone_number', 'username')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Telegram Info', {
            'fields': ('telegram_user_id', 'username', 'first_name', 'last_name')
        }),
        ('Contact', {
            'fields': ('phone_number',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
