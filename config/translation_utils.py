from deep_translator import GoogleTranslator

def translate_uz_to_ru(text):
    """
    Translates text from Uzbek to Russian using Google Translator.
    """
    if not text:
        return ""
    try:
        # Uzbek to Russian
        translated = GoogleTranslator(source='uz', target='ru').translate(text)
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text # Fallback to original text if translation fails
