from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


@extend_schema(
    summary="Get all active categories",
    description="Returns list of all active categories ordered by 'order' field",
    responses={200: CategorySerializer(many=True)}
)
@api_view(['GET'])
def get_categories(request):
    """Get all active categories"""
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    serializer = CategorySerializer(categories, many=True, context={'request': request})
    return Response(serializer.data)


@extend_schema(
    summary="Get products by category",
    description="Returns list of active products for a specific category",
    responses={200: ProductSerializer(many=True)}
)
@api_view(['GET'])
def get_category_products(request, category_id):
    """Get products by category ID"""
    products = Product.objects.filter(
        category_id=category_id,
        is_active=True
    ).order_by('order', 'name')
    
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)
@extend_schema(
    summary="Get all active products",
    description="Returns list of all active products",
    responses={200: ProductSerializer(many=True)}
)
@api_view(['GET'])
def get_all_products(request):
    """Get all active products"""
    products = Product.objects.filter(is_active=True).order_by('order', 'name')
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)
