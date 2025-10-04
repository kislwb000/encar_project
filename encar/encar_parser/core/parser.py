"""
Main parser class for Encar website
Основной класс парсера сайта Encar
"""

import re
import time
from datetime import datetime

from encar_parser.config.catalog_settings import (
    BRANDS,
    CATALOG_CONFIG,
    build_catalog_url,
)
from encar_parser.config.field_mappings import CAR_DATA, FIELD_MAPPING, FIELDS_TRANSLATE
from encar_parser.config.selectors import (
    CAR_LINK_SELECTORS,
    EXTRA_BUTTON_SELECTORS,
    MODAL_SELECTORS,
)
from encar_parser.config.settings import SETTINGS
from encar_parser.services.image_extractor import ImageExtractor
from encar_parser.services.options_extractor import OptionsExtractor
from encar_parser.services.translator import translate_text
from encar_parser.utils.captcha_handler import CaptchaHandler
from encar_parser.utils.file_handler import save_to_json
from encar_parser.utils.logger import ParserLogger

from .driver_setup import setup_chrome_driver
from .scraper import Scraper


class EncarParser:
    """Основной класс парсера Encar"""

    def __init__(self, headless=True, enable_translation=True, preset_brand=None):
        """
        Инициализация парсера

        Args:
            headless: Запуск браузера в headless режиме
            enable_translation: Включить перевод данных
            preset_brand: Предустановленная марка автомобиля
        """
        print("Инициализация парсера...")

        # Настройка драйвера
        self.driver, self.wait = setup_chrome_driver(headless=headless)

        # Инициализация вспомогательных классов
        self.scraper = Scraper(self.driver, self.wait)
        self.image_extractor = ImageExtractor(self.scraper)
        self.options_extractor = OptionsExtractor(self.scraper)
        self.captcha_handler = CaptchaHandler(self.scraper)
        self.logger = ParserLogger()

        # Настройки
        self.enable_translation = enable_translation
        self.preset_brand = preset_brand
        self.settings = SETTINGS

        # Данные
        self.cars_data = []
        self.processed_urls = set()

        if preset_brand:
            print(f"Предустановленная марка: {preset_brand}")

    def close(self):
        """Закрытие драйвера"""
        if self.driver:
            self.driver.quit()
            print("Драйвер закрыт")

    def get_catalog_params(self, brand_key=None, start_page=None, max_pages=None):
        """
        Получение параметров каталога

        Args:
            brand_key: Ключ марки из config
            start_page: Стартовая страница (None = из конфига)
            max_pages: Максимум страниц (None = из конфига)
        """
        # Используем настройки из конфига
        if brand_key is None:
            brand_key = CATALOG_CONFIG["default_brand"]

        if start_page is None:
            start_page = CATALOG_CONFIG["start_page"]

        if max_pages is None:
            max_pages = CATALOG_CONFIG["max_pages"]

        # Строим URL со стартовой страницей
        catalog_url = build_catalog_url(brand_key, page=start_page)

        self.scraper.open_url(catalog_url, wait_time=5)
        self.scraper.scroll_page(
            max_scrolls=self.settings.get("max_scrolls", 2),
            pause=self.settings.get("scroll_pause", 2),
        )

        # Получаем общее количество автомобилей
        cars_count_text = self.scraper.get_text_by_selector(".allcount")
        cars_count = int(re.sub(r"\D", "", cars_count_text)) if cars_count_text else 0

        if cars_count == 0:
            print("Не удалось определить количество автомобилей")
            return 0, start_page

        # Вычисляем количество страниц
        items_per_page = CATALOG_CONFIG["items_per_page"]
        total_pages = cars_count // items_per_page
        if cars_count % items_per_page != 0:
            total_pages += 1

        # Применяем ограничение
        if max_pages and max_pages > 0:
            pages_to_parse = min(max_pages, total_pages - start_page + 1)
        else:
            pages_to_parse = total_pages - start_page + 1

        print(f"Всего автомобилей: {cars_count}")
        print(f"Всего страниц: {total_pages}")
        print(f"Начало с страницы: {start_page}")
        print(f"Страниц для парсинга: {pages_to_parse}")

        return pages_to_parse, start_page

    def get_car_links(self, brand_key=None, start_page=None, max_pages=None):
        """
        Получение ссылок на автомобили

        Args:
            brand_key: Ключ марки
            start_page: Стартовая страница
            max_pages: Максимум страниц
        """
        if brand_key is None:
            brand_key = CATALOG_CONFIG["default_brand"]

        pages_count, start_page = self.get_catalog_params(
            brand_key, start_page=start_page, max_pages=max_pages
        )

        if pages_count == 0:
            print("Не удалось получить информацию о страницах")
            return []

        car_links = []

        for i in range(pages_count):
            page = start_page + i

            page_url = build_catalog_url(brand_key, page=page)

            print(f"Открыта страница: {page} ({i + 1}/{pages_count})")
            self.scraper.open_url(page_url, wait_time=5)
            self.scraper.scroll_page(
                max_scrolls=self.settings.get("max_scrolls", 2),
                pause=self.settings.get("scroll_pause", 2),
            )

            # Ищем ссылки
            for selector in CAR_LINK_SELECTORS:
                elements = self.scraper.find_elements(selector)
                print(f"  Селектор '{selector}': найдено {len(elements)} элементов")

                for element in elements:
                    try:
                        data_impression = element.get_attribute("data-impression")
                        if data_impression:
                            car_id = data_impression.partition("|")[0]
                            full_url = f"https://fem.encar.com/cars/detail/{car_id}?carid={car_id}"
                            if full_url not in car_links:
                                car_links.append(full_url)
                    except Exception:
                        continue

        print(f"Найдено {len(car_links)} уникальных ссылок")
        return car_links

    def extract_car_data(self, car_url, modal=None):
        """
        Извлечение основных данных автомобиля

        Args:
            car_url: URL страницы автомобиля
            modal: Модальное окно с дополнительными данными

        Returns:
            dict: Данные автомобиля
        """
        print("Извлекаем данные автомобиля...")

        car_data = CAR_DATA.copy()

        try:
            # ID автомобиля из URL
            match = re.search(r"/detail/(\d+)", car_url)
            if match:
                car_data["id"] = match.group(1)
                print(f"ID: {car_data['id']}")
            else:
                # КРИТИЧНАЯ ОШИБКА
                print("ОШИБКА: не удалось извлечь ID")
                self._save_debug_info(car_url, "no_car_id")
                return car_data

            # Марка
            if self.preset_brand:
                car_data["brand"] = self.preset_brand
                print(f"Марка (предустановлена): {self.preset_brand}")
            else:
                car_data["brand"] = "Unknown brand"
                print("Марка не определена")

            # Модель
            car_data["model"] = self.scraper.get_text_by_selector(
                ".DetailSummary_tit_car__0OEVh > span", 0
            )

            if not car_data["model"]:
                print("ВНИМАНИЕ: модель не найдена")
                # СОХРАНЯЕМ debug
                if self.settings.get("debug_on_error_only", True):
                    self._save_debug_info(car_url, "no_model")
            else:
                print(f"Модель: {car_data['model']}")

            # Цена
            price_text = self.scraper.get_text_by_selector(
                ".DetailLeadCase_point__vdG4b", 0
            )
            if price_text:
                car_data["price"] = price_text.replace(",", "")
                try:
                    car_data["price"] = str(int(car_data["price"]) * 10000)
                    print(f"Цена: {car_data['price']}")
                except ValueError:
                    print(f"Ошибка преобразования цены: {price_text}")

            # Конфигурация
            conf_1 = self.scraper.get_text_by_selector(
                ".DetailSummary_tit_car__0OEVh > span", 1
            )
            conf_2 = self.scraper.get_text_by_selector(
                ".DetailSummary_tit_car__0OEVh > span", 2
            )
            car_data["configuration"] = (
                f"{conf_1} {conf_2}".strip() if conf_2 else conf_1
            )
            print(f"Конфигурация: {car_data['configuration']}")

            # Год
            year_text = self.scraper.get_text_by_selector(
                ".DetailSummary_define_summary__NOYid > dd", 0
            )
            if year_text and len(year_text) >= 2:
                try:
                    year_short = year_text[:2]
                    car_data["year"] = str(int(year_short) + 2000)
                    print(f"Год: {car_data['year']}")
                except ValueError:
                    print(f"Ошибка преобразования года: {year_text}")

            # Пробег
            mileage_text = self.scraper.get_text_by_selector(
                ".DetailSummary_define_summary__NOYid > dd", 1
            )
            if mileage_text:
                car_data["mileage"] = re.sub(r"\D", "", mileage_text.replace(",", ""))
                print(f"Пробег: {car_data['mileage']}")

            # Топливо
            car_data["fuel"] = self.scraper.get_text_by_selector(
                ".DetailSummary_define_summary__NOYid > dd", 2
            ).strip()
            print(f"Топливо: {car_data['fuel']}")

            # Гос номер
            car_data["vehnumber"] = self.scraper.get_text_by_selector(
                ".DetailSummary_define_summary__NOYid > dd", 3
            ).strip()
            print(f"Гос номер: {car_data['vehnumber']}")

            # Данные из модального окна
            if modal:
                print("Извлекаем данные из модального окна...")
                extracted_fields = self.extract_fields_from_modal(modal)
                car_data.update(extracted_fields)

        except Exception as e:
            print(f"Ошибка извлечения данных: {e}")
            self._save_debug_info(car_url, "extract_error")
            self.logger.log_error("extract_car_data", str(e))

        return car_data

    def extract_fields_from_modal(self, modal):
        """
        Извлечение полей из модального окна

        Args:
            modal: WebElement модального окна

        Returns:
            dict: Извлеченные поля
        """
        extracted_data = {}

        try:
            list_items = self.scraper.find_elements(
                MODAL_SELECTORS["list_items"], parent=modal
            )
            print(f"  Найдено {len(list_items)} элементов в модальном окне")

            for item in list_items:
                try:
                    title_elements = self.scraper.find_elements(
                        MODAL_SELECTORS["title"], parent=item
                    )
                    value_elements = self.scraper.find_elements(
                        MODAL_SELECTORS["value"], parent=item
                    )

                    if not title_elements or not value_elements:
                        continue

                    title_text = title_elements[0].text.strip().lower()
                    value_text = value_elements[0].text.strip().lower()

                    # Проверяем есть ли это поле в маппинге
                    if title_text in FIELD_MAPPING:
                        field_key = FIELD_MAPPING[title_text]

                        # Специальная обработка для некоторых полей
                        if field_key == "displacement":
                            value_cc = re.sub(r"[^0-9]", "", value_text)
                            if value_cc:
                                try:
                                    value_l = round(int(value_cc) / 1000, 1)
                                    value_text = f"{value_l}l. ({value_cc}cm³)"
                                except ValueError:
                                    pass
                        elif field_key == "seating":
                            value_text = re.sub(r"[^0-9]", "", value_text)

                        extracted_data[field_key] = value_text
                        print(f"    {field_key}: {value_text}")

                except Exception:
                    continue

        except Exception as e:
            print(f"Ошибка извлечения полей из модального окна: {e}")
            self.logger.log_error("extract_fields_from_modal", str(e))

        return extracted_data

    def translate_car_data(self, car_data):
        """
        Перевод данных автомобиля

        Args:
            car_data: Словарь с данными автомобиля

        Returns:
            dict: Переведенные данные
        """
        if not self.enable_translation:
            print("Перевод отключен")
            return car_data

        print("Переводим данные...")
        translated_data = car_data.copy()

        for field in FIELDS_TRANSLATE:
            if field in car_data and car_data[field]:
                try:
                    original_text = car_data[field]
                    translated_text = translate_text(original_text)
                    translated_data[field] = translated_text
                except Exception as e:
                    print(f"Ошибка перевода поля {field}: {e}")
                    self.logger.increment("translation_errors")
                    translated_data[field] = car_data[field]

        return translated_data

    def check_page_loaded(self, timeout=10):
        """
        Проверка полной загрузки страницы

        Args:
            timeout: Максимальное время ожидания

        Returns:
            bool: True если страница загружена
        """
        try:
            from selenium.common.exceptions import TimeoutException
            from selenium.webdriver.support.wait import WebDriverWait

            # Ждем, пока document.readyState станет 'complete'
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            # Дополнительная пауза для AJAX запросов
            time.sleep(2)

            return True
        except TimeoutException:
            print("Таймаут загрузки страницы")
            return False
        except Exception as e:
            print(f"Ошибка проверки загрузки страницы: {e}")
            return False

    def click_details_button(self):
        """
        Нажатие на кнопку "Детали" для открытия модального окна
        Расширенная версия с несколькими стратегиями клика

        Returns:
            bool: True если успешно, False иначе
        """
        print("Ищем кнопку 'Детали'...")

        # Проверяем загрузку страницы
        self.check_page_loaded()

        for i, selector in enumerate(EXTRA_BUTTON_SELECTORS):
            try:
                print(f"Проверяем селектор {i + 1}: {selector}")

                # Ищем элементы
                elements = self.scraper.find_elements(selector)
                print(f"  Найдено элементов: {len(elements)}")

                if not elements:
                    continue

                # Пробуем кликнуть по каждому найденному элементу
                for idx, elem in enumerate(elements):
                    try:
                        is_displayed = elem.is_displayed()
                        print(f"  Элемент {idx + 1} видим: {is_displayed}")

                        if not is_displayed:
                            continue

                        # Прокручиваем к элементу
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center'});", elem
                        )
                        time.sleep(1)

                        # Кликаем через JavaScript (самый надежный для headless)
                        self.driver.execute_script("arguments[0].click();", elem)
                        time.sleep(3)

                        print(f"Кнопка нажата успешно: {selector}")
                        return True

                    except Exception as e:
                        print(f"  Ошибка с элементом {idx + 1}: {e}")
                        continue

            except Exception as e:
                print(f"Ошибка с селектором {selector}: {e}")
                continue

        print("Кнопка 'Детали' не найдена - продолжаем без модального окна")
        return False

    def parse_car_page(self, car_url):
        """
        Парсинг страницы отдельного автомобиля

        Args:
            car_url: URL страницы автомобиля

        Returns:
            dict или None: Данные автомобиля или None при ошибке
        """
        if car_url in self.processed_urls:
            print(f"URL уже обработан: {car_url}")
            return None

        print(f"\n{'=' * 60}")
        print(f"Парсим автомобиль: {car_url}")
        print("=" * 60)

        self.logger.increment("total_processed")

        try:
            # Открываем страницу
            self.scraper.open_url(car_url, wait_time=3)

            # ДОБАВЛЕНО: Проверка капчи
            if self.captcha_handler.check_captcha():
                print("ОБНАРУЖЕНА КАПЧА!")
                self.captcha_handler.save_captcha_debug()

                if not self.captcha_handler.handle_captcha():
                    print("Не удалось пройти капчу, пропускаем автомобиль")
                    self.logger.increment("failed")
                    return None

            # Открываем модальное окно
            modal = None
            modal_opened = self.click_details_button()

            if modal_opened:
                modal = self.scraper.wait_for_element(
                    MODAL_SELECTORS["container"], condition="visible"
                )
                if modal:
                    print("Модальное окно найдено")
                else:
                    print("Модальное окно не найдено")
                    if self.settings.get("debug_on_error_only", True):
                        print("Сохраняем debug: модальное окно не найдено")
                        self._save_debug_info(car_url, "modal_not_found")

            # Извлекаем основные данные
            car_data = self.extract_car_data(car_url, modal)

            # ПРОВЕРЯЕМ критичные поля
            if not car_data.get("id") or not car_data.get("model"):
                print("ОШИБКА: не удалось извлечь критичные данные")
                # СОХРАНЯЕМ debug
                self._save_debug_info(car_url, "missing_critical_data")
                self.logger.increment("failed")
                return None

            car_data["url"] = car_url
            car_data["parsed_at"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            # Извлекаем изображения
            car_data["images"] = self.image_extractor.extract_images(
                max_images=self.settings.get("max_images", 10)
            )

            # Извлекаем опции
            car_data["options"] = self.options_extractor.extract_options(car_data["id"])

            # Переводим данные
            car_data = self.translate_car_data(car_data)

            self.processed_urls.add(car_url)
            self.logger.increment("successful")

            return car_data

        except Exception as e:
            print(f"Ошибка при парсинге {car_url}: {e}")

            # СОХРАНЯЕМ debug при любой ошибке
            print("Сохраняем HTML и скриншот при ошибке...")
            self._save_debug_info(car_url, "exception")

            self.logger.increment("failed")
            self.logger.log_error("parse_car_page", str(e))
            return None

    def _save_debug_info(self, car_url, reason="error"):
        """
        Внутренний метод для сохранения debug информации

        Args:
            car_url: URL автомобиля
            reason: Причина сохранения
        """
        try:
            car_id_match = re.search(r"/detail/(\d+)", car_url)
            car_id = car_id_match.group(1) if car_id_match else "unknown"

            prefix = f"{reason}_{car_id}"
            self.scraper.save_page_debug_info(prefix=prefix)

        except Exception as e:
            print(f"Ошибка сохранения debug информации: {e}")

    def parse_catalog(
        self,
        brand_key=None,
        max_cars=None,
        start_page=None,
        max_pages=None,
        filename=None,
    ):
        """
        Основной метод парсинга каталога

        Args:
            brand_key: Ключ марки
            max_cars: Максимум автомобилей
            start_page: Стартовая страница
            max_pages: Максимум страниц
            filename: Имя файла
        """
        start_time = time.time()
        self.logger.start()

        try:
            if brand_key is None:
                brand_key = CATALOG_CONFIG["default_brand"]

            if max_cars is None:
                max_cars = CATALOG_CONFIG.get("max_cars", 1000)

            print("\n" + "=" * 60)
            print("НАЧАЛО ПАРСИНГА КАТАЛОГА")
            print(f"Марка: {brand_key.upper()} ({BRANDS[brand_key]})")
            print("=" * 60)

            # Получаем ссылки на автомобили
            car_links = self.get_car_links(
                brand_key=brand_key, start_page=start_page, max_pages=max_pages
            )

            if not car_links:
                print("Не найдено ссылок на автомобили")
                return

            total_to_parse = min(len(car_links), max_cars)
            print(f"\nНачинаем парсинг {total_to_parse} автомобилей...")

            # Парсим каждый автомобиль
            for i, car_url in enumerate(car_links[:max_cars]):
                print(f"\nПрогресс: {i + 1}/{total_to_parse}")

                car_data = self.parse_car_page(car_url)

                if car_data:
                    self.cars_data.append(car_data)
                    brand = car_data.get("brand", "Unknown")
                    model = car_data.get("model", "Unknown")
                    img_count = len(car_data.get("images", []))
                    print(f"Успешно: {brand} {model} ({img_count} фото)")

                # Пауза между запросами
                time.sleep(self.settings.get("request_delay", 2))

            # Сохраняем данные
            if self.cars_data:
                save_to_json(self.cars_data, filename)
            else:
                print("Нет данных для сохранения")

            # Показываем статистику
            elapsed_time = time.time() - start_time
            self.logger.print_statistics(elapsed_time, self.cars_data)

        except Exception as e:
            print(f"Ошибка в основном процессе парсинга: {e}")
            self.logger.log_error("parse_catalog", str(e))
        finally:
            self.close()
