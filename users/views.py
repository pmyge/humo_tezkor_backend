from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import UserProfile
from .serializers import (
    UserSerializer, 
    TelegramLoginSerializer, 
    PhoneVerifySerializer
)


@api_view(['POST'])
def telegram_login(request):
    """Login or register user via Telegram"""
    serializer = TelegramLoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    telegram_user_id = data['telegram_user_id']
    
    # Get or create user
    user, created = UserProfile.objects.get_or_create(
        telegram_user_id=telegram_user_id,
        defaults={
            'username': data.get('username', ''),
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
        }
    )
    
    # If user exists, update info
    if not created:
        user.username = data.get('username', user.username)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.save()
    
    return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_user_info(request):
    """Get user info by telegram_user_id"""
    telegram_user_id = request.query_params.get('telegram_user_id')
    
    if not telegram_user_id:
        return Response({'error': 'telegram_user_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_object_or_404(UserProfile, telegram_user_id=telegram_user_id)
    return Response(UserSerializer(user).data)


@api_view(['POST'])
def phone_verify(request):
    """Verify and save user phone number"""
    serializer = PhoneVerifySerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    user = get_object_or_404(UserProfile, telegram_user_id=data['telegram_user_id'])
    
    user.phone_number = data['phone_number']
    user.save()
    
    return Response(UserSerializer(user).data)
@api_view(['PATCH'])
def change_language(request):
    """Update user language preference"""
    telegram_user_id = request.data.get('telegram_user_id')
    language = request.data.get('language')
    
    if not telegram_user_id or not language:
        return Response({'error': 'telegram_user_id and language required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_object_or_404(UserProfile, telegram_user_id=telegram_user_id)
    user.language = language  # Ensure language field exists in model
    # Wait, does the model have a language field? Let me check.
    user.save()
    
    return Response(UserSerializer(user).data)
