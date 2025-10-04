"""
Интерфейс для вызова парсера из Telegram бота
"""

import asyncio

from encar_parser.core.parser import EncarParser


async def parse_car_by_url(car_url: str, preset_brand: str = None) -> dict:  # type: ignore
    """
    Асинхронная обертка для парсера

    Args:
        car_url: URL автомобиля
        preset_brand: Предустановленная марка (опционально)

    Returns:
        dict: Данные автомобиля
    """
    # Запускаем парсер в executor для неблокирующего выполнения
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, _parse_car_sync, car_url, preset_brand)
    return result


def _parse_car_sync(car_url: str, preset_brand: str = None) -> dict:  # type: ignore
    """
    Синхронная функция парсинга
    """
    parser = None
    try:
        # Создаем парсер (headless для серверного режима)
        parser = EncarParser(
            headless=True, enable_translation=True, preset_brand=preset_brand
        )

        # Парсим автомобиль
        car_data = parser.parse_car_page(car_url)

        if not car_data:
            raise Exception("Не удалось получить данные автомобиля")

        return car_data

    except Exception as e:
        raise Exception(f"Ошибка парсинга: {str(e)}")

    finally:
        if parser:
            parser.close()


async def parse_car_by_id(car_id: str, preset_brand: str = None) -> dict:  # type: ignore
    """
    Парсинг по ID автомобиля

    Args:
        car_id: ID автомобиля
        preset_brand: Предустановленная марка

    Returns:
        dict: Данные автомобиля
    """
    car_url = f"https://fem.encar.com/cars/detail/{car_id}?carid={car_id}"
    return await parse_car_by_url(car_url, preset_brand)
