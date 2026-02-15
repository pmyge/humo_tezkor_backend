from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.get_messages, name='get-messages'),
    path('send/', views.send_message, name='send-message'),
    path('admin-reply/', views.admin_reply, name='admin-reply'),
]
