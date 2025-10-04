"""
Encar Parser - Main Entry Point
Парсер данных автомобилей с сайта Encar.com
"""
import argparse
from datetime import datetime

from encar_parser.core.parser import EncarParser


def print_menu():
    """Вывод главного меню"""
    print("\n" + "=" * 50)
    print("ENCAR PARSER")
    print("=" * 50)
    print("Выберите режим:")
    print("1. Обычный запуск (20 авто)")
    print("2. Парсинг одного автомобиля")
    print("3. Полный запуск (настраиваемый)")
    print("0. Выход")
    print("=" * 50)


def mode_standard_run():
    """Обычный запуск - 20 автомобилей"""
    catalog_url = input("Введите URL каталога (или Enter для примера): ").strip()
    if not catalog_url:
        catalog_url = "https://www.encar.com/fc/fc_carsearchlist.do?carType=for"

    parser = EncarParser(headless=False, enable_translation=True)
    parser.parse_catalog(catalog_url, max_cars=20)


def mode_single_car():
    """Парсинг одного автомобиля"""
    test_url = input("Введите URL автомобиля: ").strip()
    if not test_url:
        print("URL не указан")
        return

    preset_brand = input(
        "Введите марку автомобиля (или Enter для авто-определения): "
    ).strip()

    debug_all = (
        input("Сохранять debug для всех действий? (y/n, Enter = n): ").strip().lower()
    )

    parser = EncarParser(
        headless=False,
        enable_translation=True,
        preset_brand=preset_brand if preset_brand else None,
    )

    # Временно включаем полный debug
    if debug_all == "y":
        parser.settings["debug_save_all"] = True

    result = parser.parse_car_page(test_url)

    if result:
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТ ПАРСИНГА")
        print("=" * 50)
        for key, value in result.items():
            if key == "images":
                print(f"{key}: {len(value)} изображений")
                for i, img in enumerate(value[:3]):
                    print(f"  {i + 1}. ...{img[-50:]}")
                if len(value) > 3:
                    print(f"  ... и ещё {len(value) - 3}")
            elif key == "options":
                true_count = sum(1 for v in value.values() if v)
                false_count = sum(1 for v in value.values() if not v)
                print(f"{key}: True: {true_count}, False: {false_count}")
            else:
                print(f"{key}: {value}")

    parser.close()


def mode_full_run():
    """Полный запуск с параметрами из конфига"""
    from encar_parser.config.catalog_settings import BRANDS, CATALOG_CONFIG

    # Все параметры берутся из конфига
    brand_key = CATALOG_CONFIG["default_brand"]
    max_pages = CATALOG_CONFIG.get("max_pages", 0)  # 0 = все страницы

    print("\n" + "=" * 60)
    print("ПОЛНЫЙ ЗАПУСК (параметры из config)")
    print("=" * 60)
    print(f"Марка: {brand_key.upper()} ({BRANDS[brand_key]})")
    print(f"Максимум страниц: {'все' if max_pages == 0 else max_pages}")
    print("=" * 60)

    # Генерируем имя файла автоматически
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{brand_key}_data_{timestamp}.json"

    # Preset brand для перевода
    preset_brand = brand_key.capitalize()

    # Создаем парсер
    parser = EncarParser(
        headless=True,  # Всегда headless для автоматического режима
        enable_translation=True,
        preset_brand=preset_brand,
    )

    # Запускаем парсинг
    # max_cars можно тоже добавить в CATALOG_CONFIG
    parser.parse_catalog(
        brand_key=brand_key,
        max_cars=1000,  # или из конфига
        max_pages=max_pages,
        filename=filename,
    )


parser = argparse.ArgumentParser()
parser.add_argument("--mode", type=int, choices=range(0, 4), help="Режим работы: 0-3")
args = parser.parse_args()

def run_mode(choice):
    try:
        if choice == "0":
            print("Выход из программы")
            exit(0)
        elif choice == "1":
            mode_standard_run()
        elif choice == "2":
            mode_single_car()
        elif choice == "3":
            mode_full_run()
        else:
            print("Неверный выбор. Попробуйте снова.")
    except KeyboardInterrupt:
        print("\n\nПрервано пользователем")
        exit(1)
    except Exception as e:
        print(f"\nОшибка: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Главная функция"""

    if args.mode is not None:
        choice = str(args.mode)
        run_mode(choice)
    else:
        while True:
            print_menu()
            choice = input("\nВведите номер (0-3): ").strip()
            run_mode(choice)


if __name__ == "__main__":
    main()
