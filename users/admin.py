from django.contrib import admin
from .models import UserProfile, Customer, Notification


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'created_at')
    search_fields = ('username', 'first_name', 'last_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=True)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'phone_number', 'created_at', 'last_login')
    list_filter = ('created_at', 'last_login')
    search_fields = ('id', 'first_name', 'phone_number', 'username')
    readonly_fields = ('id', 'created_at', 'updated_at', 'last_login')
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=False)
    
    fieldsets = (
        ('User Info', {
            'fields': ('username', 'first_name', 'last_login')
        }),
        ('Contact', {
            'fields': ('phone_number',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_broadcast', 'created_at')
    list_filter = ('is_broadcast', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('recipients',)
    
    def get_queryset(self, request):
        return super().get_queryset(request)
