import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class BotConfig:
    """Конфигурация бота"""

    token: str
    admin_ids: list[int] = None  # type: ignore

    def __post_init__(self):
        if self.admin_ids is None:
            self.admin_ids = []


def load_config() -> BotConfig:
    """Загрузка конфигурации из переменных окружения или файла"""
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise ValueError("Не задан BOT_TOKEN! Проверьте .env файл.")

    # Можно добавить админов через переменную окружения
    admin_ids_str = os.getenv("ADMIN_IDS", "")
    admin_ids = [int(id.strip()) for id in admin_ids_str.split(",") if id.strip()]

    return BotConfig(token=token, admin_ids=admin_ids)
