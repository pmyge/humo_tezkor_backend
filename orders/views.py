from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from users.models import UserProfile
from .models import Order, OrderItem
from .serializers import OrderSerializer


from django.db import transaction
from products.models import Product

@api_view(['POST'])
@transaction.atomic
def create_order(request):
    """Create a new order with items and location"""
    data = request.data
    telegram_user_id = data.get('telegram_user_id')
    items_data = data.get('items', [])
    
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
    
    total_amount = 0
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
    
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


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
