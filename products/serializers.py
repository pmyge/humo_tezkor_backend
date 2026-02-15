from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer"""
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'name_ru', 'image', 'order', 'products_count']
    
    def get_products_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ProductSerializer(serializers.ModelSerializer):
    """Product serializer"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_name_ru = serializers.CharField(source='category.name_ru', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_name', 'category_name_ru', 
            'name', 'name_ru', 'image', 'price', 
            'description', 'description_ru', 'order'
        ]
