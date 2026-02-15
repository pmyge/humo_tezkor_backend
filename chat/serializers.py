from rest_framework import serializers
from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    admin_name = serializers.CharField(source='admin_user.full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'user_name', 'message', 'is_from_admin', 
                  'admin_user', 'admin_name', 'created_at', 'is_read']
        read_only_fields = ['id', 'created_at']


class SendMessageSerializer(serializers.Serializer):
    telegram_id = serializers.CharField(max_length=50)
    message = serializers.CharField()


class AdminReplySerializer(serializers.Serializer):
    user_telegram_id = serializers.CharField(max_length=50)
    admin_telegram_id = serializers.CharField(max_length=50)
    message = serializers.CharField()
