from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from users.models import UserProfile
from .models import Order, OrderItem
from .serializers import OrderSerializer


from django.db import transaction
from products.models import Product
from decimal import Decimal
import traceback

@api_view(['POST'])
@transaction.atomic
def create_order(request):
    """Create a new order with items and location"""
    try:
        data = request.data
        telegram_user_id = data.get('telegram_user_id')
        items_data = data.get('items', [])
        
        print(f"DEBUG: Creating order for user {telegram_user_id}. Data: {data}")
        
        if not telegram_user_id:
            return Response({'error': 'telegram_user_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not items_data:
            return Response({'error': 'items required'}, status=status.HTTP_400_BAD_REQUEST)
            
        user = get_object_or_404(UserProfile, telegram_user_id=telegram_user_id)
        
        # Create the Order
        order = Order.objects.create(
            user=user,
            phone_number=data.get('phone_number', user.phone_number),
            delivery_address=data.get('delivery_address', ''),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            notes=data.get('notes', ''),
            status='pending'
        )
        
        total_amount = Decimal('0')
        # Create OrderItems
        for item in items_data:
            product_id = item.get('product_id')
            quantity = int(item.get('quantity', 1))
            product = get_object_or_404(Product, id=product_id)
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
            total_amount += product.price * quantity
            
        order.total_amount = total_amount
        order.save()
        
        # Send notification to Telegram group
        try:
            from config.telegram_utils import send_telegram_notification
            from django.conf import settings
            
            # Dynamic admin URL based on current host
            scheme = request.scheme
            host = request.get_host()
            admin_link = f"{scheme}://{host}/admin/orders/order/{order.id}/change/"
            
            msg = (
                "<b>Diqqat Humo_tezkor mini app dan yangi buyurtma kelib tushdi!</b>\n\n"
                f"🆔 <b>Buyurtma ID:</b> #{order.id}\n"
                f"👤 <b>Mijoz:</b> {user.first_name} {user.last_name}\n"
                f"💰 <b>Jami summa:</b> {order.total_amount:,.0f} UZS\n\n"
                "🚀 Tezroq tekshirish uchun admin panelga kiring:\n"
                f"🔗 <a href='{admin_link}'>Buyurtmani ko'rish</a>"
            )
            send_telegram_notification(msg)
        except Exception as e:
            print(f"DEBUG: Failed to send TG notification: {e}")

        serializer = OrderSerializer(order)
        print(f"DEBUG: Order #{order.id} created successfully.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"ERROR in create_order: {str(e)}")
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_active_orders(request):
    """Get user's pending (Faol) orders"""
    telegram_user_id = request.query_params.get('telegram_user_id')
    
    if not telegram_user_id:
        return Response({'error': 'telegram_user_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_object_or_404(UserProfile, telegram_user_id=telegram_user_id)
    orders = Order.objects.filter(user=user, status='pending')
    
    serializer = OrderSerializer(orders, many=True)
    return Response({'orders': serializer.data})


@api_view(['GET'])
def get_confirmed_orders(request):
    """Get user's confirmed (active) orders"""
    telegram_user_id = request.query_params.get('telegram_user_id')
    
    if not telegram_user_id:
        return Response({'error': 'telegram_user_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_object_or_404(UserProfile, telegram_user_id=telegram_user_id)
    orders = Order.objects.filter(user=user, status='active')
    
    serializer = OrderSerializer(orders, many=True)
    return Response({'orders': serializer.data})


@api_view(['GET'])
def get_all_orders(request):
    """Get all user orders"""
    telegram_user_id = request.query_params.get('telegram_user_id')
    
    if not telegram_user_id:
        return Response({'error': 'telegram_user_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_object_or_404(UserProfile, telegram_user_id=telegram_user_id)
    orders = Order.objects.filter(user=user)
    
    serializer = OrderSerializer(orders, many=True)
    return Response({'orders': serializer.data})
