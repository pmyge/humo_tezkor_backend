from rest_framework import serializers
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'telegram_user_id', 'username', 'first_name', 'last_name', 
                  'full_name', 'phone_number', 'language', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class TelegramLoginSerializer(serializers.Serializer):
    telegram_user_id = serializers.IntegerField()
    username = serializers.CharField(max_length=150, required=False, allow_blank=True)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)


class PhoneVerifySerializer(serializers.Serializer):
    telegram_user_id = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=20)
