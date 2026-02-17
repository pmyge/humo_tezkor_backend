from django.urls import path
from . import views

urlpatterns = [
    path('active/', views.get_active_orders, name='active-orders'),
    path('confirmed/', views.get_confirmed_orders, name='confirmed-orders'),
    path('all/', views.get_all_orders, name='all-orders'),
    path('create/', views.create_order, name='create-order'),
]
