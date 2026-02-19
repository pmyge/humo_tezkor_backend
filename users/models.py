from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class UserProfile(AbstractUser):
    """User profile model for storing telegram user info and phone number"""
    telegram_user_id = models.BigIntegerField(unique=True, db_index=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    language = models.CharField(max_length=10, default='uz')
    
    # We use username for internal django auth (maybe telegram_id as username)
    # first_name, last_name are already in AbstractUser
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Manager (Staff)"
        verbose_name_plural = "Administration Team"
        ordering = ['-created_at']
    
    def __str__(self):
        try:
            name = f"{self.first_name} {self.last_name}".strip() or self.username or f"User {self.id}"
            if self.is_staff:
                return f"{name} (ADMIN)"
            return f"{self.id or '?'}. {name} ({self.phone_number or 'No phone'})"
        except Exception:
            return f"User {self.id or 'Unknown'}"


class Customer(UserProfile):
    """Proxy model for Mini App customers (Non-staff)"""
    class Meta:
        proxy = True
        verbose_name = "Mini App User"
        verbose_name_plural = "Users (Mini App)"
        ordering = ['-created_at']

    def __str__(self):
        name = f"{self.first_name} {self.last_name}".strip() or self.username
        return f"{self.id}. {name} ({self.phone_number or 'No phone'})"


class Notification(models.Model):
    """System notification model"""
    title = models.CharField(max_length=200, help_text="Deprecated: use title_uz/ru")
    description = models.TextField(help_text="Deprecated: use description_uz/ru")
    
    title_uz = models.CharField(max_length=200, verbose_name="Sarlavha (UZ)", null=True, blank=True)
    title_ru = models.CharField(max_length=200, verbose_name="Заголовок (RU)", null=True, blank=True)
    
    description_uz = models.TextField(verbose_name="Tavsif (UZ)", null=True, blank=True)
    description_ru = models.TextField(verbose_name="Описание (RU)", null=True, blank=True)
    
    is_broadcast = models.BooleanField(default=False, help_text="If checked, all users will see this notification")
    recipients = models.ManyToManyField(UserProfile, blank=True, related_name='notifications', help_text="Select specific users if not a broadcast")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'about_us'
        db_table = 'users_notification'
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']

    def __str__(self):
        return self.title_uz or self.title or "Untitled Notification"


class NotificationRead(models.Model):
    """Tracks which users have read which notifications"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'about_us'
        db_table = 'users_notificationread'
        unique_together = ('user', 'notification')


class About(models.Model):
    """Shop information model"""
    phone_number = models.CharField(max_length=20, help_text="Store contact phone number")
    email = models.EmailField(help_text="Store contact email")
    
    address = models.TextField(help_text="Deprecated: use address_uz/ru", null=True, blank=True)
    address_uz = models.TextField(verbose_name="Manzil (UZ)", null=True, blank=True)
    address_ru = models.TextField(verbose_name="Адрес (RU)", null=True, blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'about_us'
        db_table = 'users_about'
        verbose_name = "About Us"
        verbose_name_plural = "About Us"

    def __str__(self):
        return "Shop Information"
