"""Keyboard layouts for Uzbek and Russian languages"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Uzbek keyboards
def get_main_menu_uz(shop_url: str, chat_url: str, orders_url: str):
    """Main menu keyboard in Uzbek with 2x2 layout"""
    keyboard = [
        [
            KeyboardButton(text="🛒 Do'kon", web_app=WebAppInfo(url=shop_url)),
            KeyboardButton(text="📦 Buyurtmalar", web_app=WebAppInfo(url=orders_url))
        ],
        [
            KeyboardButton(text="💬 Yordam", web_app=WebAppInfo(url=chat_url)),
            KeyboardButton(text="🌐 Til: O'zbek")
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_language_selection_uz():
    """Language selection keyboard"""
    keyboard = [
        [KeyboardButton(text="🇺🇿 O'zbek tili")],
        [KeyboardButton(text="🇷🇺 Rus tili")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_orders_menu_uz():
    """Orders menu in Uzbek"""
    keyboard = [
        [KeyboardButton(text="⏳ Faol buyurtmalar")],
        [KeyboardButton(text="📋 Barcha buyurtmalar")],
        [KeyboardButton(text="🔙 Orqaga")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_phone_request_uz():
    """Phone number request keyboard in Uzbek"""
    keyboard = [
        [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)],
        [KeyboardButton(text="🔙 Orqaga")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# Russian keyboards
def get_main_menu_ru(shop_url: str, chat_url: str, orders_url: str):
    """Main menu keyboard in Russian with 2x2 layout"""
    keyboard = [
        [
            KeyboardButton(text="🛒 Магазин", web_app=WebAppInfo(url=shop_url)),
            KeyboardButton(text="📦 Заказы", web_app=WebAppInfo(url=orders_url))
        ],
        [
            KeyboardButton(text="💬 Поддержка", web_app=WebAppInfo(url=chat_url)),
            KeyboardButton(text="🌐 Язык: Русский")
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_language_selection_ru():
    """Language selection keyboard"""
    keyboard = [
        [KeyboardButton(text="🇺🇿 Узбекский язык")],
        [KeyboardButton(text="🇷🇺 Русский язык")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_orders_menu_ru():
    """Orders menu in Russian"""
    keyboard = [
        [KeyboardButton(text="⏳ Активные заказы")],
        [KeyboardButton(text="📋 Все заказы")],
        [KeyboardButton(text="🔙 Назад")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_phone_request_ru():
    """Phone number request keyboard in Russian"""
    keyboard = [
        [KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)],
        [KeyboardButton(text="🔙 Назад")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
