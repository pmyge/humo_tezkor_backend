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
        name = f"{self.first_name} {self.last_name}".strip() or self.username
        if self.is_staff:
            return f"{name} (ADMIN)"
        return f"{name} ({self.phone_number or 'No phone'}) - {self.telegram_user_id}"


class Customer(UserProfile):
    """Proxy model for Mini App customers (Non-staff)"""
    class Meta:
        proxy = True
        verbose_name = "Mini App User"
        verbose_name_plural = "Users (Mini App)"
        ordering = ['-created_at']

    def __str__(self):
        name = f"{self.first_name} {self.last_name}".strip() or self.username
        return f"{name} ({self.phone_number or 'No phone'}) - {self.telegram_user_id}"
