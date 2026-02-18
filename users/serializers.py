from rest_framework import serializers
from .models import UserProfile, Notification, NotificationRead

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'telegram_user_id', 'username', 'first_name', 'last_name', 'phone_number', 'language', 'is_staff']

class TelegramLoginSerializer(serializers.Serializer):
    telegram_user_id = serializers.IntegerField()
    username = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)

class PhoneVerifySerializer(serializers.Serializer):
    telegram_user_id = serializers.BigIntegerField()
    phone_number = serializers.CharField()
    first_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    username = serializers.CharField(required=False, allow_null=True, allow_blank=True)

class NotificationSerializer(serializers.ModelSerializer):
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'is_broadcast', 'created_at', 'is_read']

    def get_is_read(self, obj):
        telegram_user_id = self.context.get('telegram_user_id')
        if not telegram_user_id:
            # Fallback to session user if available
            request = self.context.get('request')
            user = request.user if request and not request.user.is_anonymous else None
            if user:
                return NotificationRead.objects.filter(user=user, notification=obj).exists()
            return False
            
        user = UserProfile.objects.filter(telegram_user_id=telegram_user_id).first()
        if user:
            return NotificationRead.objects.filter(user=user, notification=obj).exists()
        return False
