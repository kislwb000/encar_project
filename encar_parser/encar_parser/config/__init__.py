"""
Configuration module for Encar Parser
Содержит все настройки и конфигурации парсера
"""

from .catalog_settings import BRANDS, CATALOG_CONFIG, build_catalog_url
from .field_mappings import CAR_DATA, CAR_OPTIONS, FIELD_MAPPING, FIELDS_TRANSLATE
from .selectors import CAR_LINK_SELECTORS, EXTRA_BUTTON_SELECTORS
from .settings import SETTINGS

__all__ = [
    "SETTINGS",
    "CAR_LINK_SELECTORS",
    "EXTRA_BUTTON_SELECTORS",
    "CAR_DATA",
    "CAR_OPTIONS",
    "FIELD_MAPPING",
    "FIELDS_TRANSLATE",
    "BRANDS",
    "CATALOG_CONFIG",
    "build_catalog_url",
]
