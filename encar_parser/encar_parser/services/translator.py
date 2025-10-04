"""
Translation service
Сервис перевода с корейского на английский
"""

from deep_translator import GoogleTranslator

from encar_parser.data.translation_cache import TRANSLATION_CACHE


def is_english(text):
    """
    Проверка является ли текст английским

    Args:
        text: Текст для проверки

    Returns:
        bool: True если текст на английском
    """
    if not text:
        return True

    latin_chars = sum(1 for c in text if c.isascii() and c.isalpha())
    total_chars = sum(1 for c in text if c.isalpha())

    if total_chars == 0:
        return True  # Только цифры/символы

    return (latin_chars / total_chars) > 0.7


def translate_text(text, view_log=False):
    """
    Перевод текста с корейского на английский
    Использует кэш для частых фраз, API переводчик для новых

    Args:
        text: Текст для перевода
        view_log: Выводить ли лог перевода

    Returns:
        str: Переведенный текст
    """
    if not text or not text.strip():
        return ""

    # Очищаем текст
    clean_text = text.strip()

    # Проверяем, не английский ли уже
    if is_english(clean_text):
        return clean_text

    # Проверяем кэш готовых переводов
    if clean_text in TRANSLATION_CACHE:
        cached_translation = TRANSLATION_CACHE[clean_text]
        if view_log:
            print(f"Cache: '{clean_text}' -> '{cached_translation}'")
        return cached_translation

    # Используем API переводчик
    try:
        translator = GoogleTranslator(source="ko", target="en")
        api_translation = translator.translate(clean_text)

        if api_translation and api_translation.strip():
            if view_log:
                print(f"API: '{clean_text}' -> '{api_translation}'")
            return api_translation
        else:
            if view_log:
                print(f"Empty API translation for: '{clean_text}'")
            return clean_text

    except Exception as e:
        print(f"Translation error for '{clean_text}': {e}")
        return clean_text
