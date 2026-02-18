from django.urls import path
from . import views

urlpatterns = [
    path('telegram-login/', views.telegram_login, name='telegram-login'),
    path('me/', views.get_user_info, name='user-info'),
    path('phone-verify/', views.phone_verify, name='phone-verify'),
    path('language/', views.change_language, name='change-language'),
    path('notifications/', views.get_notifications, name='get-notifications'),
    path('notifications/mark-read/', views.mark_notification_as_read, name='mark-notification-read'),
]
