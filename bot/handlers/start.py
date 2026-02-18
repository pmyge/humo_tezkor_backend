"""Start command handler"""

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.menus import get_main_menu_uz, get_main_menu_ru
from keyboards.texts import get_text
from services.api import APIService
from config import BACKEND_API_URL, WEB_APP_SHOP_URL, WEB_APP_CHAT_URL, WEB_APP_ORDERS_URL

router = Router()
api = APIService(BACKEND_API_URL)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command"""
    user = message.from_user
    language = 'uz' # Default language
    
    # Save user data in state (minimal)
    await state.update_data(language=language)
    
    # Send welcome message
    welcome_text = get_text(language, 'welcome', name=user.first_name or user.username)
    choose_action = get_text(language, 'choose_action')
    
    # Show main menu with appended user ID for robust identification
    sep = '&' if '?' in WEB_APP_SHOP_URL else '?'
    shop_url = f"{WEB_APP_SHOP_URL}{sep}tid={user.id}"
    chat_url = f"{WEB_APP_CHAT_URL}{sep}tid={user.id}"
    orders_url = f"{WEB_APP_ORDERS_URL}{sep}tid={user.id}"

    if language == 'uz':
        keyboard = get_main_menu_uz(shop_url, chat_url, orders_url)
    else:
        keyboard = get_main_menu_ru(shop_url, chat_url, orders_url)
    
    await message.answer(f"{welcome_text}\n\n{choose_action}", reply_markup=keyboard)
