from django.db import models
from users.models import UserProfile


class ChatMessage(models.Model):
    """Chat message between user and admin"""
    
    user = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="User who sent/received the message"
    )
    message = models.TextField(help_text="Message content")
    is_from_admin = models.BooleanField(
        default=False,
        help_text="True if message is from admin to user"
    )
    admin_user = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admin_messages',
        help_text="Admin who sent the reply"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
        ordering = ['created_at']

    def __str__(self):
        direction = "Admin → User" if self.is_from_admin else "User → Admin"
        return f"{direction}: {self.user.first_name} - {self.message[:50]}"
