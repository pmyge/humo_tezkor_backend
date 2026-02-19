import json
import os
import logging
import urllib.request
import urllib.parse

logger = logging.getLogger(__name__)

def send_telegram_notification(message):
    """
    Sends a message to a Telegram chat/group using the bot token.
    Uses BOT_TOKEN and TELEGRAM_CHAT_ID from environment variables.
    Uses urllib.request for zero dependencies.
    """
    token = os.getenv('BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')  # e.g., @humotezkor or numeric ID

    if not token or not chat_id:
        logger.error("Telegram notification failed: BOT_TOKEN or TELEGRAM_CHAT_ID not configured.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(data).encode('utf-8')
        
        with urllib.request.urlopen(req, jsondata, timeout=10) as response:
            result = response.read()
            return True
    except Exception as e:
        logger.error(f"Error sending Telegram notification: {e}")
        return False
