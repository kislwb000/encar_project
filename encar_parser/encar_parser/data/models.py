"""
Data models for type hints and validation
Модели данных для типизации и валидации
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class CarData:
    """
    Модель данных автомобиля
    """

    # Основные данные
    id: str = ""
    brand: str = ""
    model: str = ""
    price: str = ""
    configuration: str = ""
    year: str = ""
    mileage: str = ""
    fuel: str = ""
    vehnumber: str = ""

    # Дополнительные данные из модального окна
    transmission: str = ""
    car_type: str = ""
    color: str = ""
    seating: str = ""
    displacement: str = ""
    region: str = ""

    # Метаданные
    url: str = ""
    parsed_at: str = ""
    images: List[str] = field(default_factory=list)
    options: Dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Преобразование в словарь"""
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "price": self.price,
            "configuration": self.configuration,
            "year": self.year,
            "mileage": self.mileage,
            "fuel": self.fuel,
            "vehnumber": self.vehnumber,
            "transmission": self.transmission,
            "car_type": self.car_type,
            "color": self.color,
            "seating": self.seating,
            "displacement": self.displacement,
            "region": self.region,
            "url": self.url,
            "parsed_at": self.parsed_at,
            "images": self.images,
            "options": self.options,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CarData":
        """Создание из словаря"""
        return cls(**data)

    def validate(self) -> bool:
        """
        Базовая валидация данных

        Returns:
            bool: True если данные валидны
        """
        # Проверяем обязательные поля
        if not self.id:
            return False
        if not self.brand:
            return False
        if not self.model:
            return False

        return True

    def get_summary(self) -> str:
        """
        Получение краткой информации об автомобиле

        Returns:
            str: Краткая информация
        """
        return f"{self.brand} {self.model} ({self.year}) - {self.price}"


@dataclass
class CarOption:
    """
    Модель опции автомобиля
    """

    name: str
    enabled: bool = False
    category: Optional[str] = None

    def to_dict(self) -> dict:
        """Преобразование в словарь"""
        return {
            "name": self.name,
            "enabled": self.enabled,
            "category": self.category,
        }


@dataclass
class ParsingSession:
    """
    Модель сессии парсинга
    """

    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_cars: int = 0
    successful_cars: int = 0
    failed_cars: int = 0
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Преобразование в словарь"""
        return {
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "total_cars": self.total_cars,
            "successful_cars": self.successful_cars,
            "failed_cars": self.failed_cars,
            "errors": self.errors,
        }
