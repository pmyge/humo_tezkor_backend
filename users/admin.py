from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db.models import Q
from .models import UserProfile, Customer
from about_us.models import Notification, About, NotificationRead


class UserProfileCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_superuser', 'groups', 'user_permissions')


class UserProfileChangeForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = '__all__'


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    add_form = UserProfileCreationForm
    form = UserProfileChangeForm
    
    list_display = ('username', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'created_at')
    search_fields = ('username', 'first_name', 'last_name', 'phone_number')
    list_per_page = 15
    readonly_fields = ('created_at', 'updated_at')
    
    # Customizing fieldsets for the edit page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'language')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )

    # Customizing fieldsets for the "Add User" page
    # Note: UserCreationForm uses password1 and password2
    add_fieldsets = (
        ('General', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_superuser'),
        }),
        ('Permissions and Roles', {
            'classes': ('wide',),
            'fields': ('groups', 'user_permissions'),
        }),
    )

    def get_queryset(self, request):
        # Strict filtering for Administration Team (Staff OR Superuser)
        qs = super().get_queryset(request)
        return qs.filter(Q(is_staff=True) | Q(is_superuser=True))


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'phone_number', 'created_at', 'last_login')
    list_filter = ('created_at', 'last_login')
    search_fields = ('id', 'first_name', 'phone_number', 'username')
    list_per_page = 15
    readonly_fields = ('id', 'created_at', 'updated_at', 'last_login', 'date_joined')
    
    def get_queryset(self, request):
        # Strict filtering for Users (Mini App) - NOT Staff AND NOT Superuser
        return super().get_queryset(request).filter(is_staff=False, is_superuser=False)
    
    fieldsets = (
        ('User Info', {
            'fields': ('username', 'first_name', 'last_login')
        }),
        ('Contact', {
            'fields': ('phone_number',)
        }),
        ('Status', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Usually customers are added via Mini App, not admin panel
        return False
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
