import requests
import os
import logging

logger = logging.getLogger(__name__)

def send_telegram_notification(message):
    """
    Sends a message to a Telegram chat/group using the bot token.
    Uses BOT_TOKEN and TELEGRAM_CHAT_ID from environment variables.
    """
    token = os.getenv('BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')  # e.g., @humotezkor or numeric ID

    if not token or not chat_id:
        logger.error("Telegram notification failed: BOT_TOKEN or TELEGRAM_CHAT_ID not configured.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"Error sending Telegram notification: {e}")
        return False
