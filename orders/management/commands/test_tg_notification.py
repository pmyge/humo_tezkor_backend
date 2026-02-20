from django.core.management.base import BaseCommand
from config.telegram_utils import send_telegram_notification
import os

class Command(BaseCommand):
    help = 'Test Telegram notification'

    def handle(self, *args, **options):
        self.stdout.write("Testing Telegram notification...")
        
        token = os.getenv('BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        self.stdout.write(f"Environment - Token: {bool(token)}, ChatID: {chat_id}")
        
        message = "<b>🔔 TEST:</b> Humo Tezkor bildirishnoma tizimi tekshirilmoqda!"
        success = send_telegram_notification(message)
        
        if success:
            self.stdout.write(self.style.SUCCESS("Success! Message sent."))
        else:
            self.stdout.write(self.style.ERROR("Failed to send message. Check logs."))
