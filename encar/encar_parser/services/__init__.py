"""
Services module for Encar Parser
Содержит бизнес-логику для различных операций парсинга
"""

from .image_extractor import ImageExtractor
from .options_extractor import OptionsExtractor
from .translator import is_english, translate_text

__all__ = ["translate_text", "is_english", "ImageExtractor", "OptionsExtractor"]
