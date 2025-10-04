"""
Утилиты для парсинга - интеграция с Encar парсером
"""

import re
from typing import Optional

# Импорт интерфейса парсера
from shared.parser_interface import parse_car_by_id


def extract_car_id(url: str) -> Optional[str]:
    """Извлекает ID автомобиля из ссылки Encar"""
    patterns = [
        r"carid=(\d+)",
        r"/detail/(\d+)",
        r"/(\d+)\?",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


async def run_encar_parser(car_id: str, preset_brand: str = None) -> dict:  # type: ignore
    """
    Запускает настоящий парсер Encar

    Args:
        car_id: ID автомобиля
        preset_brand: Предустановленная марка

    Returns:
        Словарь с данными автомобиля
    """
    return await parse_car_by_id(car_id, preset_brand)
