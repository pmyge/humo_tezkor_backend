from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Customer, Notification, About


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'created_at')
    search_fields = ('username', 'first_name', 'last_name', 'phone_number')
    list_per_page = 15
    readonly_fields = ('created_at', 'updated_at')
    
    # Customizing fieldsets to include our custom fields while keeping standard UserAdmin fields
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'language')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_superuser'),
        }),
    )

    def get_queryset(self, request):
        # Allow superusers to see everyone, but filter for is_staff for others (optional)
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_staff=True)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'phone_number', 'created_at', 'last_login')
    list_filter = ('created_at', 'last_login')
    search_fields = ('id', 'first_name', 'phone_number', 'username')
    list_per_page = 15
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
    list_display = ('title_uz', 'is_broadcast', 'created_at')
    list_filter = ('is_broadcast', 'created_at')
    search_fields = ('title_uz', 'title_ru', 'description_uz', 'description_ru')
    list_per_page = 15
    filter_horizontal = ('recipients',)
    
    fieldsets = (
        ('Uzbek Content', {
            'fields': ('title_uz', 'description_uz')
        }),
        ('Russian Content', {
            'fields': ('title_ru', 'description_ru')
        }),
        ('Settings', {
            'fields': ('is_broadcast', 'recipients')
        }),
        ('Deprecated', {
            'fields': ('title', 'description'),
            'classes': ('collapse',)
        }),
    )

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'email', 'updated_at')
    
    fieldsets = (
        ('Contact Info', {
            'fields': ('phone_number', 'email')
        }),
        ('Location (Uzbek)', {
            'fields': ('address_uz',)
        }),
        ('Location (Russian)', {
            'fields': ('address_ru',)
        }),
        ('Deprecated', {
            'fields': ('address',),
            'classes': ('collapse',)
        }),
    )

    # Allowed more control over About instances as requested
    def has_add_permission(self, request):
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj)
