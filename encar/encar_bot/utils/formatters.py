"""
Форматирование данных автомобиля для Telegram
"""


def format_car_info(data: dict) -> str:
    """
    Форматирует данные автомобиля из парсера
    """
    message = "🚗 <b>Информация об автомобиле</b>\n\n"

    # Основная информация
    if data.get("brand"):
        message += f"🏢 Марка: <b>{data['brand']}</b>\n"
    if data.get("model"):
        message += f"🚙 Модель: <b>{data['model']}</b>\n"
    if data.get("year"):
        message += f"📅 Год: <b>{data['year']}</b>\n"
    if data.get("price"):
        message += f"💰 Цена: <b>{data['price']} ₩</b>\n"
    if data.get("mileage"):
        message += f"📏 Пробег: <b>{data['mileage']} км</b>\n"

    message += "\n<b>Характеристики:</b>\n"

    if data.get("fuel"):
        message += f"⛽ Топливо: {data['fuel']}\n"
    if data.get("transmission"):
        message += f"⚙️ КПП: {data['transmission']}\n"
    if data.get("color"):
        message += f"🎨 Цвет: {data['color']}\n"
    if data.get("displacement"):
        message += f"🔧 Объем: {data['displacement']}\n"
    if data.get("seating"):
        message += f"👥 Мест: {data['seating']}\n"

    # Дополнительно
    if data.get("region"):
        message += f"\n📍 Регион: {data['region']}\n"
    if data.get("vehnumber"):
        message += f"🔢 Номер: {data['vehnumber']}\n"

    # Изображения
    if data.get("images") and len(data["images"]) > 0:
        message += f"\n📸 Фотографий: {len(data['images'])}\n"

    # Опции
    if data.get("options"):
        active_options = sum(1 for v in data["options"].values() if v)
        if active_options > 0:
            message += f"✅ Опций: {active_options}\n"

    return message


def format_car_images(data: dict) -> list:
    """
    Возвращает список URL изображений для отправки
    """
    return data.get("images", [])[:10]  # Максимум 10 фото


def get_welcome_message() -> str:
    """Возвращает приветственное сообщение"""
    return (
        "👋 Привет! Я бот для парсинга автомобилей с Encar.\n\n"
        "Отправьте мне ссылку на автомобиль, и я получу всю информацию о нём.\n\n"
        "Пример ссылки:\n"
        "<code>https://fem.encar.com/cars/detail/40647630?carid=40647630</code>\n\n"
        "Используйте /help для получения помощи."
    )


def get_help_message() -> str:
    """Возвращает сообщение помощи"""
    return (
        "ℹ️ <b>Как использовать бота:</b>\n\n"
        "1️⃣ Отправьте ссылку на автомобиль с сайта Encar\n"
        "2️⃣ Бот извлечет ID автомобиля\n"
        "3️⃣ Запустит парсер и получит данные\n"
        "4️⃣ Отправит вам отформатированную информацию\n\n"
        "<b>Поддерживаемые форматы ссылок:</b>\n"
        "• https://fem.encar.com/cars/detail/40647630?carid=40647630\n"
        "• https://www.encar.com/dc/dc_carsearchpay.do?carid=40647630\n\n"
        "<b>Команды:</b>\n"
        "/start - Начать работу\n"
        "/help - Помощь\n"
        "/cancel - Отменить текущую операцию"
    )
