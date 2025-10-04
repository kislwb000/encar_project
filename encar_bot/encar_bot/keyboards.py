from aiogram import types


def get_car_link_keyboard(url: str) -> types.InlineKeyboardMarkup:
    """
    Создает клавиатуру со ссылкой на автомобиль

    Args:
        url: Ссылка на автомобиль

    Returns:
        Inline клавиатура
    """
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text="🔗 Открыть на Encar",
                url=url
            )]
        ]
    )
