"""Text messages in Uzbek and Russian"""

MESSAGES = {
    'uz': {
        'welcome': "Assalomu Aleykum {name}, Humo Tezkor botiga xush kelibsiz!",
        'choose_action': "Quyidagilardan birini tanlang:",
        'language_changed': "✅ Til o'zgartirildi",
        'language_select': "Tilni tanlang:",
        'phone_required': "Chat ishlatish uchun telefon raqamingizni yuboring:",
        'phone_received': "✅ Telefon raqam saqlandi",
        'no_active_orders': "Sizda faol buyurtmalar yo'q",
        'no_orders': "Sizda buyurtmalar yo'q",
        'error': "❌ Xatolik yuz berdi. Iltimos qayta urinib ko'ring.",
        'back_to_menu': "Asosiy menyu",
    },
    'ru': {
        'welcome': "Здравствуйте {name}, добро пожаловать в бот Humo Tezkor!",
        'choose_action': "Выберите одно из следующих:",
        'language_changed': "✅ Язык изменен",
        'language_select': "Выберите язык:",
        'phone_required': "Для использования чата отправьте свой номер телефона:",
        'phone_received': "✅ Номер телефона сохранен",
        'no_active_orders': "У вас нет активных заказов",
        'no_orders': "У вас нет заказов",
        'error': "❌ Произошла ошибка. Пожалуйста, попробуйте снова.",
        'back_to_menu': "Главное меню",
    }
}


def get_text(language: str, key: str, **kwargs) -> str:
    """Get text message in specified language"""
    text = MESSAGES.get(language, MESSAGES['uz']).get(key, '')
    return text.format(**kwargs) if kwargs else text
