"""
General settings for the parser
Общие настройки парсера
"""

# Основные настройки парсера
SETTINGS = {
    # Задержки и таймауты
    "scroll_pause": 2,  # Пауза между прокрутками (секунды)
    "page_load_wait": 5,  # Время ожидания загрузки страницы (секунды)
    "element_wait": 10,  # Время ожидания элемента (секунды)
    "request_delay": 2,  # Пауза между запросами (секунды)
    # Ограничения
    "max_scrolls": 2,  # Максимальное количество прокруток
    "max_images": 10,  # Максимальное количество изображений
    "max_retries": 3,  # Максимальное количество повторных попыток
    # Параметры слайдера
    "slider_clicks": 5,  # Количество кликов по слайдеру
    # Настройки вывода
    "verbose": True,  # Подробный вывод логов
    "save_screenshots": False,  # Сохранять скриншоты при ошибках
    "debug_on_error_only": True,  # Сохранять debug только при ошибках
    "debug_save_all": False,  # Сохранять для всех страниц (для отладки)
}

# Настройки WebDriver
DRIVER_SETTINGS = {
    "headless": True,
    "window_size": "1920,1080",
    "implicit_wait": 10,
    "page_load_timeout": 30,
}

# Настройки перевода
TRANSLATION_SETTINGS = {
    "enabled": True,
    "source_lang": "ko",
    "target_lang": "en",
    "use_cache": True,
}

# Настройки сохранения файлов
FILE_SETTINGS = {
    "output_dir": "output",
    "log_dir": "logs",
    "format": "json",  # json или csv
    "auto_filename": True,
}
