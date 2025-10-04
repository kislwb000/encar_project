import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Главная функция запуска бота"""
    from encar_bot.config import load_config
    from encar_bot.handlers.common import common_router
    from encar_bot.handlers.parser import parser_router

    # Загрузка конфигурации
    config = load_config()

    # Инициализация бота
    bot = Bot(token=config.token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Подключение роутеров
    dp.include_router(common_router)
    dp.include_router(parser_router)

    logger.info("Запуск бота...")

    # Удаление вебхуков
    await bot.delete_webhook(drop_pending_updates=True)

    # Запуск polling
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
