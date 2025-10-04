"""
Хэндлеры парсера с реальной интеграцией
"""

import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto

from encar_bot.keyboards import get_car_link_keyboard
from encar_bot.states import ParserStates
from encar_bot.utils.formatters import format_car_images, format_car_info
from encar_bot.utils.parser import extract_car_id, run_encar_parser

parser_router = Router()
logger = logging.getLogger(__name__)


@parser_router.message(ParserStates.waiting_for_link, F.text)
async def process_link(message: types.Message, state: FSMContext):
    """Обработчик ссылок на автомобили"""
    url = message.text.strip()  # type: ignore

    # Валидация URL
    if not url.startswith("http"):
        await message.answer(
            "⚠️ Отправьте корректную ссылку на автомобиль с Encar.", parse_mode="HTML"
        )
        return

    # Извлечение ID
    car_id = extract_car_id(url)
    if not car_id:
        await message.answer(
            "❌ Не удалось извлечь ID автомобиля из ссылки.\n\n"
            "Пример правильной ссылки:\n"
            "<code>https://fem.encar.com/cars/detail/40647630?carid=40647630</code>",
            parse_mode="HTML",
        )
        return

    # Уведомление о начале
    processing_msg = await message.answer(
        f"🔍 Получаю информацию об автомобиле...\n"
        f"🆔 ID: <code>{car_id}</code>\n"
        f"⏳ Это может занять 10-30 секунд...",
        parse_mode="HTML",
    )

    try:
        # ЗАПУСК ПАРСЕРА
        car_data = await run_encar_parser(car_id)

        # Форматирование текста
        formatted_message = format_car_info(car_data)

        # Обновляем сообщение
        await processing_msg.edit_text(formatted_message, parse_mode="HTML")

        # Отправка изображений (если есть)
        images = format_car_images(car_data)
        if images:
            media_group = [InputMediaPhoto(media=url) for url in images[:10]]
            try:
                await message.answer_media_group(media_group)  # type: ignore
            except Exception as e:
                logger.error(f"Ошибка отправки изображений: {e}")

        # Кнопка со ссылкой
        await message.answer(
            "✅ Готово! Отправьте ещё одну ссылку для парсинга.",
            reply_markup=get_car_link_keyboard(url),
        )

    except Exception as e:
        logger.error(f"Ошибка парсинга car_id={car_id}: {e}", exc_info=True)
        await processing_msg.edit_text(
            f"❌ Произошла ошибка при получении данных:\n"
            f"<code>{str(e)}</code>\n\n"
            f"Возможные причины:\n"
            f"• Автомобиль удален с сайта\n"
            f"• Проблемы с сетью\n"
            f"• Капча на сайте\n\n"
            f"Попробуйте позже или отправьте другую ссылку.",
            parse_mode="HTML",
        )


@parser_router.message()
async def handle_other_messages(message: types.Message):
    """Обработчик остальных сообщений"""
    await message.answer(
        "🤔 Отправьте ссылку на автомобиль с Encar.\n\n"
        "Используйте /help для инструкций.",
        parse_mode="HTML",
    )
