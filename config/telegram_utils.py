import json
import os
import logging
import urllib.request
import urllib.parse
import urllib.error

logger = logging.getLogger(__name__)

def send_telegram_notification(message):
    """
    Sends a message to a Telegram chat/group using the bot token.
    Uses BOT_TOKEN and TELEGRAM_CHAT_ID from environment variables.
    Uses urllib.request for zero dependencies.
    """
    # Fallback values if environment variables are not set on Render
    token = os.getenv('BOT_TOKEN', '8354261773:AAEh6AvvE3rrvnUoUoIN2lv3pj468ebZ5jQ')
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '-1003528740543')

    print(f"DEBUG: Attempting to send TG notification. Chat ID: {chat_id}, Token exists: {bool(token)}")

    if not token or not chat_id:
        msg = f"Telegram notification failed: Configuration missing. Token: {bool(token)}, ChatID: {chat_id}"
        logger.error(msg)
        print(f"DEBUG: {msg}")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    
    try:
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(data).encode('utf-8')
        
        with urllib.request.urlopen(req, jsondata, timeout=10) as response:
            result = response.read().decode('utf-8')
            print(f"DEBUG: TG Notification sent successfully. Response: {result}")
            return True
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        msg = f"Telegram API Error (HTTP {e.code}): {error_body}"
        logger.error(msg)
        print(f"DEBUG: {msg}")
        return False
    except Exception as e:
        msg = f"Error sending Telegram notification: {str(e)}"
        logger.error(msg)
        print(f"DEBUG: {msg}")
        return False
