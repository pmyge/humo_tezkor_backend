from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from users.models import UserProfile
from .models import ChatMessage
from .serializers import ChatMessageSerializer, SendMessageSerializer, AdminReplySerializer


@api_view(['GET'])
def get_messages(request):
    """Get chat messages for a user"""
    telegram_user_id = request.query_params.get('telegram_user_id')
    
    if not telegram_user_id:
        return Response({'error': 'telegram_user_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_object_or_404(UserProfile, telegram_user_id=telegram_user_id)
    messages = ChatMessage.objects.filter(user=user).order_by('created_at')
    
    serializer = ChatMessageSerializer(messages, many=True)
    return Response({'messages': serializer.data})


@api_view(['POST'])
def send_message(request):
    """User sends a message"""
    serializer = SendMessageSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    user = get_object_or_404(UserProfile, telegram_user_id=data['telegram_user_id'])
    
    # Create message
    message = ChatMessage.objects.create(
        user=user,
        message=data['message'],
        is_from_admin=False
    )
    
    return Response(ChatMessageSerializer(message).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def admin_reply(request):
    """Admin replies to user"""
    serializer = AdminReplySerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    user = get_object_or_404(UserProfile, telegram_user_id=data['user_telegram_id'])
    admin = get_object_or_404(UserProfile, telegram_user_id=data['admin_telegram_id'])
    
    # Create admin reply message
    message = ChatMessage.objects.create(
        user=user,
        message=data['message'],
        is_from_admin=True,
        admin_user=admin
    )
    
    return Response(ChatMessageSerializer(message).data, status=status.HTTP_201_CREATED)
