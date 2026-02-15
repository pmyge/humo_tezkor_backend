from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'user_name', 'status', 'total', 'items_data', 
                  'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
