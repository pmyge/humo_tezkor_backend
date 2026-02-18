"""Orders handler"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.menus import get_main_menu_uz, get_main_menu_ru
from keyboards.texts import get_text
from services.api import APIService
from config import BACKEND_API_URL, WEB_APP_SHOP_URL, WEB_APP_CHAT_URL, WEB_APP_ORDERS_URL

router = Router()
api = APIService(BACKEND_API_URL)


@router.message(F.text.in_(["⏳ Faol buyurtmalar", "⏳ Активные заказы"]))
async def show_active_orders(message: Message, state: FSMContext):
    """Show active orders"""
    data = await state.get_data()
    language = data.get('language', 'uz')
    user_id = message.from_user.id
    
    # Get active orders from backend
    result = await api.get_active_orders(user_id)
    
    if "error" in result:
        await message.answer(get_text(language, 'error'))
        return
    
    orders = result.get('orders', [])
    
    if not orders:
        await message.answer(get_text(language, 'no_active_orders'))
    else:
        # Format orders list
        text = "⏳ Faol buyurtmalar:\n\n" if language == 'uz' else "⏳ Активные заказы:\n\n"
        
        for order in orders:
            order_id = order.get('id')
            status = order.get('status')
            total = order.get('total')
            text += f"📦 Buyurtma #{order_id}\n"
            text += f"Status: {status}\n"
            text += f"Summa: {total} so'm\n\n"
        
        await message.answer(text)


@router.message(F.text.in_(["📋 Barcha buyurtmalar", "📋 Все заказы"]))
async def show_all_orders(message: Message, state: FSMContext):
    """Show all orders"""
    data = await state.get_data()
    language = data.get('language', 'uz')
    user_id = message.from_user.id
    
    # Get all orders from backend
    result = await api.get_all_orders(user_id)
    
    if "error" in result:
        await message.answer(get_text(language, 'error'))
        return
    
    orders = result.get('orders', [])
    
    if not orders:
        await message.answer(get_text(language, 'no_orders'))
    else:
        # Format orders list
        text = "📋 Barcha buyurtmalar:\n\n" if language == 'uz' else "📋 Все заказы:\n\n"
        
        for order in orders:
            order_id = order.get('id')
            status = order.get('status')
            total = order.get('total')
            text += f"📦 Buyurtma #{order_id}\n"
            text += f"Status: {status}\n"
            text += f"Summa: {total} so'm\n\n"
        
        await message.answer(text)


@router.message(F.text.in_(["🔙 Orqaga", "🔙 Назад"]))
async def back_to_main_menu(message: Message, state: FSMContext):
    """Return to main menu"""
    data = await state.get_data()
    language = data.get('language', 'uz')
    
    if language == 'uz':
        keyboard = get_main_menu_uz(WEB_APP_SHOP_URL, WEB_APP_CHAT_URL, WEB_APP_ORDERS_URL)
    else:
        keyboard = get_main_menu_ru(WEB_APP_SHOP_URL, WEB_APP_CHAT_URL, WEB_APP_ORDERS_URL)
    
    await message.answer(get_text(language, 'back_to_menu'), reply_markup=keyboard)
