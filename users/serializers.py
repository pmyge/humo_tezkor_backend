from rest_framework import serializers
from .models import Notification, NotificationRead

class NotificationSerializer(serializers.ModelSerializer):
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'created_at', 'is_broadcast', 'is_read']

    def get_is_read(self, obj):
        user = self.context.get('request').user
        if not user or user.is_anonymous:
            # For Mini App, we usually pass telegram_user_id to the view, 
            # so the view should handle the context or we check via telegram_user_id
            telegram_user_id = self.context.get('telegram_user_id')
            if telegram_user_id:
                return NotificationRead.objects.filter(notification=obj, user__telegram_user_id=telegram_user_id).exists()
            return False
            
        return NotificationRead.objects.filter(notification=obj, user=user).exists()
