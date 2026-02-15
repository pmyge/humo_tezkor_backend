from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.get_categories, name='categories'),
    path('category/<int:category_id>/products/', views.get_category_products, name='category-products'),
]
