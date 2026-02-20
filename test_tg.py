import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from config.telegram_utils import send_telegram_notification

def diag_telegram():
    token = os.getenv('BOT_TOKEN', 'NOT_SET')
    chat_id = os.getenv('TELEGRAM_CHAT_ID', 'NOT_SET')
    
    print(f"--- Telegram Diagnostic ---")
    
    token_str = str(token)
    display_token = token_str[:10] + "..." + (token_str[-4:] if len(token_str) > 4 and token_str != 'NOT_SET' else '')
    print(f"BOT_TOKEN env: {display_token}")
    print(f"TELEGRAM_CHAT_ID env: {chat_id}")
    
    msg = "🔍 <b>Backend Diagnostic:</b> Telegram notification check."
    success = send_telegram_notification(msg)
    
    if success:
        print("✅ Notification sent successfully!")
    else:
        print("❌ Notification failed.")

if __name__ == "__main__":
    diag_telegram()
