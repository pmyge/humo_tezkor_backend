from django.urls import path
from . import views

urlpatterns = [
    path('active/', views.get_active_orders, name='active-orders'),
    path('', views.get_all_orders, name='all-orders'),
]
