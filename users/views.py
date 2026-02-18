from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import UserProfile, Notification, NotificationRead, About
from .serializers import (
    UserSerializer, 
    TelegramLoginSerializer, 
    PhoneVerifySerializer
)


def is_valid_telegram_id(tid):
    """Check if the provided Telegram ID is real and not a frontend fallback"""
    try:
        val = int(tid)
        # Allow 0 as a signifier for 'missing identity' during registration
        return val == 0 or val < 9000000000
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
    
    if not is_valid_telegram_id(telegram_user_id):
        print(f"DEBUG: Rejected invalid telegram_user_id in telegram_login: {telegram_user_id}")
        return Response({'error': 'Valid Telegram ID required'}, status=status.HTTP_400_BAD_REQUEST)

    # Try to find user by telegram_user_id first
    user = UserProfile.objects.filter(telegram_user_id=telegram_user_id).first()
    
    if user:
        # Update existing user data
        if data.get('username'): user.username = data['username']
        if data.get('first_name'): user.first_name = data['first_name']
        if data.get('last_name'): user.last_name = data['last_name']
        user.save()
        created = False
    else:
        # Try to find by username (bot often uses telegram_{id} or actual username)
        username = data.get('username')
        user = UserProfile.objects.filter(telegram_user_id=telegram_user_id).first()
        
        if not user:
            print(f"DEBUG: User {telegram_user_id} not found in telegram_login. Returning dummy success for bot compatibility.")
            # Return a dummy object that looks like a user to satisfy the old bot code
            return Response({
                'telegram_user_id': telegram_user_id,
                'username': data.get('username') or f"user_{telegram_user_id}",
                'first_name': data.get('first_name') or '',
                'language': 'uz',
                'is_registered': False # Flag for future use
            }, status=status.HTTP_200_OK)
        
        created = False
    
    return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


@api_view(['GET', 'PATCH', 'DELETE'])
def get_user_info(request):
    """Get, update or delete user info by telegram_user_id"""
    telegram_user_id = request.query_params.get('telegram_user_id') or request.data.get('telegram_user_id')
    
    if not is_valid_telegram_id(telegram_user_id):
        print(f"DEBUG: Rejected invalid or fallback telegram_user_id in get_user_info: {telegram_user_id}")
        return Response({'error': 'Valid Telegram ID required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # First, try to get the user
    user = UserProfile.objects.filter(telegram_user_id=telegram_user_id).first()
    
    if request.method == 'DELETE':
        if user:
            print(f"DEBUG: Deleting user {telegram_user_id} account.")
            user.delete()
            return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if not user:
        print(f"DEBUG: User {telegram_user_id} not found in get_user_info. Returning dummy success.")
        return Response({
            'telegram_user_id': telegram_user_id,
            'first_name': 'Guest',
            'phone_number': '',
            'language': 'uz',
            'is_registered': False
        }, status=status.HTTP_200_OK)
    
    created = False
    
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

    # Strategy: Explicitly use update_or_create by telegram_user_id if valid
    if telegram_user_id and int(telegram_user_id) > 0:
        user, created = UserProfile.objects.update_or_create(
            telegram_user_id=telegram_user_id,
            defaults={
                'phone_number': phone_number,
                'first_name': data.get('first_name') or 'User',
                'last_name': data.get('last_name', ''),
                'username': data.get('username') or f"user_{telegram_user_id}"
            }
        )
        print(f"DEBUG: update_or_create result for ID {telegram_user_id}: created={created}")
    else:
        # Fallback for ID=0 (should be rare now with our Bot URL update)
        user = UserProfile.objects.filter(phone_number=phone_number).first()
        if not user and data.get('username'):
             user = UserProfile.objects.filter(username=data['username']).first()
        
        if user:
            user.phone_number = phone_number
            if data.get('first_name'): user.first_name = data['first_name']
            user.save()
            print(f"DEBUG: Found and updated user for phone registration without ID: {user.username}")
        else:
            print(f"DEBUG: Creating new user for phone registration without ID: {phone_number}")
            user = UserProfile.objects.create(
                phone_number=phone_number,
                username=data.get('username') or f"phone_{phone_number.replace('+', '')}",
                first_name=data.get('first_name') or 'User'
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


@api_view(['GET'])
def get_notifications(request):
    """Get active notifications for the user"""
    telegram_user_id = request.query_params.get('telegram_user_id')
    if not telegram_user_id:
        return Response({'error': 'telegram_user_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
    user = UserProfile.objects.filter(telegram_user_id=telegram_user_id).first()
    if not user:
        return Response([], status=status.HTTP_200_OK)
        
    from django.db.models import Q
    from .serializers import NotificationSerializer
    
    # Notifications are either broadcast OR strictly for this user
    notifications = Notification.objects.filter(
        Q(is_broadcast=True) | Q(recipients=user)
    ).distinct().order_by('-created_at')
    
    serializer = NotificationSerializer(notifications, many=True, context={'telegram_user_id': telegram_user_id})
    return Response(serializer.data)


@api_view(['POST'])
def mark_notification_as_read(request):
    """Mark a specific notification as read by the user"""
    telegram_user_id = request.data.get('telegram_user_id')
    notification_id = request.data.get('notification_id')
    
    if not telegram_user_id or not notification_id:
        return Response({'error': 'telegram_user_id and notification_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
    user = UserProfile.objects.filter(telegram_user_id=telegram_user_id).first()
    notification = get_object_or_404(Notification, id=notification_id)
    
    if user:
        NotificationRead.objects.get_or_create(user=user, notification=notification)
        
    return Response({'status': 'ok'})


@api_view(['GET'])
def get_about(request):
    """Get store information"""
    from .serializers import AboutSerializer
    about = About.objects.first()
    if not about:
        return Response({
            'phone_number': '+998XXXXXXXXX',
            'email': 'shop@example.com',
            'address': 'Tashkent, Uzbekistan'
        })
    serializer = AboutSerializer(about)
    return Response(serializer.data)
