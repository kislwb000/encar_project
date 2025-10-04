"""
Options extraction service
Сервис извлечения опций автомобиля
"""

from encar_parser.config.field_mappings import CAR_OPTIONS

from .translator import translate_text


class OptionsExtractor:
    """
    Класс для извлечения опций автомобиля
    """

    def __init__(self, scraper):
        """
        Args:
            scraper: Экземпляр класса Scraper
        """
        self.scraper = scraper

    def extract_options(self, car_id):
        """
        Извлечение опций автомобиля со страницы опций

        Args:
            car_id: ID автомобиля

        Returns:
            dict: Словарь опций (ключ: название опции, значение: True/False)
        """
        car_option_url = f"https://fem.encar.com/cars/option/{car_id}"
        car_options = CAR_OPTIONS.copy()

        try:
            print(f"Открываем страницу опций: {car_option_url}")

            # Открываем страницу опций в новой вкладке
            self.scraper.open_new_tab(car_option_url, wait_time=5)

            # Получаем элементы опций
            elements = self.scraper.find_elements('[class*="PeerIntoCarOptions_"] > a')
            print(f"Найдено {len(elements)} элементов опций")

            # Обрабатываем первые 53 элемента (стандартное количество опций)
            for element in elements[:53]:
                try:
                    # Получаем текст опции
                    option_text = element.text.strip()

                    # Переводим и нормализуем название опции
                    translated_text = translate_text(option_text, view_log=False)
                    normalized_text = translated_text.replace(" ", "_").lower()

                    # Если опция есть в нашем словаре, отмечаем её как True
                    if normalized_text in car_options:
                        car_options[normalized_text] = True

                except Exception as e:
                    print(f"Ошибка обработки опции: {e}")
                    continue

            # Закрываем вкладку и возвращаемся к основной
            self.scraper.close_tab_and_switch(target_index=0)

            # Подсчитываем количество активных опций
            active_count = sum(1 for value in car_options.values() if value)
            print(f"{active_count} опций автомобиля успешно получены")

        except Exception as e:
            print(f"Не удалось открыть страницу опций: {e}")
            # Если что-то пошло не так, закрываем вкладку если она открыта
            try:
                if len(self.scraper.driver.window_handles) > 1:
                    self.scraper.close_tab_and_switch(target_index=0)
            except:
                pass

        return car_options
