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


def is_valid_telegram_id(tid):
    """Check if the provided Telegram ID is real and not a frontend fallback"""
    try:
        val = int(tid)
        return val < 9000000000
    except (ValueError, TypeError):
        return False

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
    
    if not is_valid_telegram_id(telegram_user_id):
        print(f"DEBUG: Rejected invalid or fallback telegram_user_id in get_user_info: {telegram_user_id}")
        return Response({'error': 'Valid Telegram ID required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # First, try to get or create the user WITHOUT the staff filter to avoid IntegrityErrors
    user, created = UserProfile.objects.get_or_create(
        telegram_user_id=telegram_user_id,
        defaults={
            'username': f"user_{telegram_user_id}",
            'first_name': 'User',
            'is_staff': False
        }
    )
    
    # If the user is staff, we don't allow the Mini App to update their profile info
    # through these specific endpoints, to keep Admin the team separate.
    is_admin_account = user.is_staff
    
    if request.method == 'PATCH':
        if is_admin_account:
            return Response({'error': 'Admin accounts cannot be managed via Mini App'}, status=status.HTTP_403_FORBIDDEN)
            
        print(f"DEBUG: Updating user {telegram_user_id} with data: {request.data}")
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        tg_username = request.data.get('username')
        
        # Define default names that should be overwritable
        DEFAULT_NAMES = ['Admin', 'User', 'Mehmon', 'Гость', '', None]
        
        # If explicitly provided in the request, we update it.
        # But for regular users, we LOCK the name to Telegram identity.
        if is_admin_account:
            if 'first_name' in request.data:
                user.first_name = first_name
            if 'last_name' in request.data:
                user.last_name = last_name
        else:
            # Regular users: names are synced from Telegram.
            # We ONLY update if the incoming name is "real" (not one of the defaults) 
            # or if the current name is a default.
            if first_name and (user.first_name in DEFAULT_NAMES or first_name not in DEFAULT_NAMES):
                user.first_name = first_name
            
            if last_name:
                user.last_name = last_name
            
            # Update username if it looks like a real telegram username (optional)
            if tg_username and user.username.startswith('user_'):
                user.username = tg_username
            
        if 'language' in request.data:
            user.language = request.data['language']
        
        if 'phone_number' in request.data:
            user.phone_number = request.data['phone_number']
            
        user.save()
        print(f"DEBUG: User updated: {user.first_name}, {user.username}, {user.phone_number}")
        
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
    telegram_user_id = data['telegram_user_id']
    phone_number = data['phone_number']

    # 1. Primary Check: Valid Telegram User ID provided?
    if not is_valid_telegram_id(telegram_user_id):
        print(f"DEBUG: Rejected invalid or fallback telegram_user_id in phone_verify: {telegram_user_id}")
        return Response({'error': 'Valid Telegram ID required. Please restart bot.'}, status=status.HTTP_400_BAD_REQUEST)

    user = UserProfile.objects.filter(telegram_user_id=telegram_user_id).first()
    
    if user:
        print(f"DEBUG: Found user by ID {telegram_user_id}. Updating phone.")
    else:
        # Check for orphaned record by phone (record created by bot but missing ID)
        # OR any record that has this phone but no Telegram ID.
        user = UserProfile.objects.filter(phone_number=phone_number, telegram_user_id__isnull=True).first()
        if user:
            print(f"DEBUG: Linking existing phone record {phone_number} to ID {telegram_user_id}")
            user.telegram_user_id = telegram_user_id
        else:
            print(f"DEBUG: No user found for ID {telegram_user_id} or orphaned phone. Creating new.")
            user = UserProfile.objects.create(
                telegram_user_id=telegram_user_id,
                username=f"user_{telegram_user_id}",
                first_name=data.get('first_name') or 'User',
                last_name=data.get('last_name', ''),
                phone_number=phone_number,
                is_staff=False
            )

    # 4. Final Updates
    user.phone_number = phone_number
    if 'first_name' in data and data['first_name'] not in ['Admin', 'User', 'Mehmon', 'Гость', '', None]:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'username' in data and (user.username.startswith('user_') or user.username == ''):
        user.username = data['username']
    user.save()

    # Protect staff accounts
    if user.is_staff:
        return Response({'error': 'Admin accounts cannot be managed via Mini App'}, status=status.HTTP_403_FORBIDDEN)
    
    print(f"DEBUG: phone_verify completed for user: {user.telegram_user_id}, {user.first_name}, {user.username}, {user.phone_number}")
    return Response(UserSerializer(user).data)
@api_view(['PATCH'])
def change_language(request):
    """Update user language preference"""
    telegram_user_id = request.data.get('telegram_user_id')
    language = request.data.get('language')
    
    if not telegram_user_id or not language:
        return Response({'error': 'telegram_user_id and language required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get or create the user safely
    user, created = UserProfile.objects.get_or_create(
        telegram_user_id=telegram_user_id,
        defaults={
            'username': f"user_{telegram_user_id}",
            'first_name': 'User',
            'is_staff': False
        }
    )
    
    if user.is_staff:
        return Response({'error': 'Admin accounts cannot be managed via Mini App'}, status=status.HTTP_403_FORBIDDEN)
        
    user.language = language
    user.save()
    return Response(UserSerializer(user).data)
