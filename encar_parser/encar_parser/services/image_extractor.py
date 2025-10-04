"""
Image extraction service
Сервис извлечения изображений из слайдера
"""


class ImageExtractor:
    """
    Класс для извлечения изображений автомобилей из слайдера
    """

    def __init__(self, scraper):
        """
        Args:
            scraper: Экземпляр класса Scraper
        """
        self.scraper = scraper

    def extract_images(self, max_images=10):
        """
        Извлечение всех изображений из открытого слайдера

        Args:
            max_images: Максимальное количество изображений

        Returns:
            list: Список URL изображений
        """
        images = []

        try:
            print("Извлекаем изображения из слайдера...")

            # Селектор контейнера слайдера
            slider_container = ".swiper-wrapper"

            # Ждем появления слайдера
            slider = self.scraper.wait_for_element(slider_container)

            if not slider:
                print("Слайдер не найден")
                return images

            print("Слайдер найден")

            # Селектор изображений в слайдере
            image_selector = "img[class*=DetailCarPhotoPc_thumb__]"

            # Ищем все изображения в слайдере
            image_elements = self.scraper.find_elements(image_selector, parent=slider)
            print(f"Найдено {len(image_elements)} изображений в слайдере")

            for i, img_element in enumerate(image_elements):
                if len(images) >= max_images:
                    break

                try:
                    # Для первых 3 изображений используем src
                    if i < 3:
                        img_src = img_element.get_attribute("src")
                        if self._is_valid_image_url(img_src):
                            img_src = self._clean_image_url(img_src)
                            images.append(img_src)
                    # Для остальных используем data-src (ленивая загрузка)
                    else:
                        img_src = img_element.get_attribute("data-src")
                        if self._is_valid_image_url(img_src):
                            img_src = self._clean_image_url(img_src)
                            images.append(img_src)

                except Exception as e:
                    print(f"Ошибка получения изображения {i + 1}: {e}")
                    continue

        except Exception as e:
            print(f"Ошибка извлечения изображений: {e}")

        print(f"Итого извлечено {len(images)} изображений")
        return images

    def _is_valid_image_url(self, url):
        """
        Проверка валидности URL изображения

        Args:
            url: URL для проверки

        Returns:
            bool: True если URL валидный
        """
        if not url:
            return False
        if not url.startswith("http"):
            return False
        if url.lower().endswith(".gif"):
            return False
        return True

    def _clean_image_url(self, url):
        """
        Очистка URL изображения от лишних параметров

        Args:
            url: URL для очистки

        Returns:
            str: Очищенный URL
        """
        # Удаляем параметр центрирования
        if "&cg=Center" in url:
            url = url.split("&cg=Center")[0]
        return url
