import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).parent.parent / '.env')

# Bot token
BOT_TOKEN = os.getenv('BOT_TOKEN', '')

# Backend API URL
BACKEND_API_URL = os.getenv('BACKEND_API_URL', 'http://localhost:8000/api')

# Web App URLs
WEB_APP_SHOP_URL = os.getenv('WEB_APP_SHOP_URL', 'https://your-webapp.com/shop')
WEB_APP_CHAT_URL = os.getenv('WEB_APP_CHAT_URL', 'https://your-webapp.com/chat')
WEB_APP_ORDERS_URL = os.getenv('WEB_APP_ORDERS_URL', 'https://your-webapp.com/orders')
