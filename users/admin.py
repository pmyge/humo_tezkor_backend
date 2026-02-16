from django.contrib import admin
from .models import UserProfile, Customer


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'is_staff', 'is_superuser', 'last_login')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    
    def get_queryset(self, request):
        # Show only staff in this specific section
        return super().get_queryset(request).filter(is_staff=True)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('telegram_user_id', 'first_name', 'last_name', 'phone_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('telegram_user_id', 'first_name', 'last_name', 'phone_number', 'username')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        # Show only Mini App users (non-staff)
        return super().get_queryset(request).filter(is_staff=False)
    
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
