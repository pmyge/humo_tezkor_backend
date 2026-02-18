"""Language change handler"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.menus import (
    get_language_selection_uz, 
    get_language_selection_ru,
    get_main_menu_uz, 
    get_main_menu_ru
)
from keyboards.texts import get_text
from services.api import APIService
from config import BACKEND_API_URL, WEB_APP_SHOP_URL, WEB_APP_CHAT_URL, WEB_APP_ORDERS_URL

router = Router()
api = APIService(BACKEND_API_URL)


@router.message(F.text.in_(["🌐 Tilni o'zgartirish", "🌐 Сменить язык", "🌐 Til: O'zbek", "🌐 Язык: Русский"]))
async def change_language(message: Message, state: FSMContext):
    """Show language selection"""
    data = await state.get_data()
    language = data.get('language', 'uz')
    
    text = get_text(language, 'language_select')
    
    if language == 'uz':
        keyboard = get_language_selection_uz()
    else:
        keyboard = get_language_selection_ru()
    
    await message.answer(text, reply_markup=keyboard)


@router.message(F.text.in_(["🇺🇿 O'zbek tili", "🇺🇿 Узбекский язык"]))
async def select_uzbek(message: Message, state: FSMContext):
    """Select Uzbek language"""
    user_id = message.from_user.id
    
    # Update language in backend
    result = await api.update_language(user_id, 'uz')
    
    if "error" not in result:
        await state.update_data(language='uz')
        
        text = get_text('uz', 'language_changed')
        keyboard = get_main_menu_uz(WEB_APP_SHOP_URL, WEB_APP_CHAT_URL, WEB_APP_ORDERS_URL)
        
        await message.answer(text, reply_markup=keyboard)
    else:
        await message.answer("❌ Xatolik yuz berdi.")


@router.message(F.text.in_(["🇷🇺 Rus tili", "🇷🇺 Русский язык"]))
async def select_russian(message: Message, state: FSMContext):
    """Select Russian language"""
    user_id = message.from_user.id
    
    # Update language in backend
    result = await api.update_language(user_id, 'ru')
    
    if "error" not in result:
        await state.update_data(language='ru')
        
        text = get_text('ru', 'language_changed')
        keyboard = get_main_menu_ru(WEB_APP_SHOP_URL, WEB_APP_CHAT_URL, WEB_APP_ORDERS_URL)
        
        await message.answer(text, reply_markup=keyboard)
    else:
        await message.answer("❌ Произошла ошибка.")
