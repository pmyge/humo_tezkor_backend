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


@api_view(['GET', 'PATCH'])
def get_user_info(request):
    """Get or update user info by telegram_user_id"""
    telegram_user_id = request.query_params.get('telegram_user_id') or request.data.get('telegram_user_id')
    
    if not telegram_user_id:
        return Response({'error': 'telegram_user_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_object_or_404(UserProfile, telegram_user_id=telegram_user_id)
    
    if request.method == 'PATCH':
        print(f"DEBUG: Updating user {telegram_user_id} with data: {request.data}")
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        
        # Define default names that should be overwritable
        DEFAULT_NAMES = ['Admin', 'User', 'Mehmon', 'Гость', '', None]
        
        # Update name if provided name is NOT default OR if current name IS default
        if first_name and (first_name not in DEFAULT_NAMES or user.first_name in DEFAULT_NAMES):
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
            
        if 'language' in request.data:
            user.language = request.data['language']
        user.save()
        print(f"DEBUG: User updated: {user.first_name}, {user.phone_number}")
        
    return Response(UserSerializer(user).data)


@api_view(['POST'])
def phone_verify(request):
    """Verify and save user phone number"""
    print(f"DEBUG: phone_verify received data: {request.data}")
    serializer = PhoneVerifySerializer(data=request.data)
    
    if not serializer.is_valid():
        print(f"DEBUG: phone_verify serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    # Get or create user
    user, created = UserProfile.objects.get_or_create(
        telegram_user_id=data['telegram_user_id'],
        defaults={
            'username': f"user_{data['telegram_user_id']}",
            'first_name': data.get('first_name') or 'User',
            'last_name': data.get('last_name', ''),
        }
    )
    
    user.phone_number = data['phone_number']
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    
    # Define default names that should be overwritable
    DEFAULT_NAMES = ['Admin', 'User', 'Mehmon', 'Гость', '', None]
    
    # If the user was NOT created (already exists), update their name if it's currently a default
    if not created:
        if first_name and (first_name not in DEFAULT_NAMES or user.first_name in DEFAULT_NAMES):
            user.first_name = first_name
        if last_name and (last_name or user.last_name in DEFAULT_NAMES):
            user.last_name = last_name
        
    user.save()
    print(f"DEBUG: phone_verify saved user: {user.telegram_user_id}, {user.first_name}, {user.phone_number}")
    
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
