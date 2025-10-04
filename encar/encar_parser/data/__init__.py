"""
Data module for Encar Parser
Содержит данные и модели
"""

from .models import CarData, CarOption
from .translation_cache import TRANSLATION_CACHE

__all__ = ["TRANSLATION_CACHE", "CarData", "CarOption"]
