"""
Catalog settings for Encar Parser
Настройки каталогов для парсера
"""

# ============================================================
# НАСТРОЙКИ МАРОК АВТОМОБИЛЕЙ
# ============================================================

# Марки автомобилей (корейские названия для URL)
BRANDS = {
    "hyundai": "현대",
    "kia": "기아",
    "genesis": "제네시스",
    "samsung": "삼성",
    "ssangyong": "쌍용",
    "renault": "르노",
    "chevrolet": "쉐보레",
    "peugeot": "푸조",
    "bmw": "BMW",
    "mercedes": "벤츠",
    "audi": "아우디",
    "volkswagen": "폭스바겐",
    "toyota": "토요타",
    "honda": "혼다",
    "nissan": "닛산",
    "mazda": "마쯔다",
    "lexus": "렉서스",
    "infiniti": "인피니티",
    "ford": "포드",
    "jeep": "지프",
    "volvo": "볼보",
    "jaguar": "재규어",
    "landrover": "랜드로버",
    "porsche": "포르쉐",
    "mini": "미니",
    "tesla": "테슬라",
    "dongpungsokon": "동풍소콘",
}

# ============================================================
# НАСТРОЙКИ КАТАЛОГА
# ============================================================

CATALOG_CONFIG = {
    # Базовая марка для парсинга
    "default_brand": "dongpungsokon",
    # Стартовая страница для парсинга
    "start_page": 1,
    # Максимальное количество страниц (0 = все страницы)
    "max_pages": 0,
    # Максимальное количество автомобилей для парсинга
    "max_cars": 1000,
    # Использовать headless режим
    "headless": True,
    # Использовать профиль Chrome (для обхода капчи)
    "use_profile": True,
    # Лимит автомобилей на странице
    "items_per_page": 50,
    # Тип сортировки
    "sort_by": "ModifiedDate",
    # Тип продажи
    "sell_type": "일반",
    # Тип автомобиля
    "car_type": "N",
}

# ============================================================
# ШАБЛОН URL КАТАЛОГА
# ============================================================


def build_catalog_url(brand_key=None, page=1, **kwargs):
    """
    Построение URL каталога

    Args:
        brand_key: Ключ марки из BRANDS (например, 'peugeot')
        page: Номер страницы
        **kwargs: Дополнительные параметры (sort_by, items_per_page и т.д.)

    Returns:
        str: Готовый URL для каталога
    """
    # Получаем марку
    if brand_key is None:
        brand_key = CATALOG_CONFIG["default_brand"]

    brand_korean = BRANDS.get(brand_key.lower())
    if not brand_korean:
        raise ValueError(f"Марка '{brand_key}' не найдена в списке BRANDS")

    # Параметры из конфига или переданные
    sort_by = kwargs.get("sort_by", CATALOG_CONFIG["sort_by"])
    items_per_page = kwargs.get("items_per_page", CATALOG_CONFIG["items_per_page"])
    sell_type = kwargs.get("sell_type", CATALOG_CONFIG["sell_type"])
    car_type = kwargs.get("car_type", CATALOG_CONFIG["car_type"])

    # Формируем URL
    url = (
        f"https://www.encar.com/fc/fc_carsearchlist.do?carType=for#!%7B%22action%22%3A%22(And.Hidden.N._.("
        f"C.CarType.{car_type}._."
        f"Manufacturer.{brand_korean}.)"
        f"_.SellType.{sell_type}.)"
        f"%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22"
        f"sort%22%3A%22{sort_by}%22%2C%22"
        f"page%22%3A{page}%2C%22"
        f"limit%22%3A{items_per_page}%2C%22"
        f"searchKey%22%3A%22%22%2C%22loginCheck%22%3Afalse%7D"
    )

    return url


# ============================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================

if __name__ == "__main__":
    # Пример 1: Peugeot, страница 1
    url1 = build_catalog_url("peugeot", page=1)
    print("Peugeot URL:", url1)

    # Пример 2: BMW, страница 2, сортировка по цене
    url2 = build_catalog_url("bmw", page=2, sort_by="Price")
    print("\nBMW URL:", url2)

    # Пример 3: Hyundai, все параметры из конфига
    url3 = build_catalog_url("hyundai")
    print("\nHyundai URL:", url3)

    # Пример 4: Список всех доступных марок
    print("\nДоступные марки:")
    for key in sorted(BRANDS.keys()):
        print(f"  - {key}: {BRANDS[key]}")
