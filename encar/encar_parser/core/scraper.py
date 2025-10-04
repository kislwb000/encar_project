"""
Low-level scraping methods for interacting with web pages
"""
import random
import time
from datetime import datetime
from pathlib import Path

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
    """
    Класс для низкоуровневых операций с Selenium
    Предоставляет удобные методы для работы со страницами
    """
    
    def __init__(self, driver, wait):
        """
        Инициализация Scraper
        
        Args:
            driver: Экземпляр Selenium WebDriver
            wait: Экземпляр WebDriverWait
        """
        self.driver = driver
        self.wait = wait
    
    def scroll_page(self, max_scrolls=10, pause=2):
        """
        Прокрутка страницы для загрузки динамического контента
        С человекоподобными случайными паузами
        
        Args:
            max_scrolls: Максимальное количество прокруток
            pause: Базовая пауза между прокрутками (секунды)
        """
        print(f"Прокручиваем страницу (макс. {max_scrolls} раз)...")
        
        for i in range(max_scrolls):
            # Случайная высота прокрутки для имитации человека
            scroll_height = random.randint(300, 800)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_height});")
            
            # Случайная пауза
            actual_pause = pause + random.uniform(-0.5, 1.5)
            time.sleep(max(actual_pause, 0.5))
            print(f"   Прокрутка {i + 1}/{max_scrolls}")
    
    def get_text_by_selector(self, selector, index=0, parent=None):
        """
        Получение текста элемента по CSS селектору
        
        Args:
            selector: CSS селектор
            index: Индекс элемента (если найдено несколько)
            parent: Родительский элемент (для поиска внутри него)
            
        Returns:
            str: Текст элемента или пустая строка
        """
        try:
            if parent:
                elements = parent.find_elements(By.CSS_SELECTOR, selector)
            else:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            
            if elements and len(elements) > index:
                text = elements[index].text.strip()
                return text if text else ""
        except Exception:
            pass
        return ""
    
    def click_element(self, selector, scroll_to_element=True, wait_after=2):
        """
        Клик по элементу с опциональной прокруткой
        
        Args:
            selector: CSS селектор элемента
            scroll_to_element: Прокрутить к элементу перед кликом
            wait_after: Пауза после клика (секунды)
            
        Returns:
            bool: True если клик успешен, False иначе
        """
        try:
            element = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            
            if scroll_to_element:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                    element
                )
                time.sleep(1)
            
            ActionChains(self.driver).move_to_element(element).click().perform()
            time.sleep(wait_after)
            return True
            
        except Exception as e:
            print(f"Ошибка клика по {selector}: {e}")
            return False
    
    def wait_for_element(self, selector, timeout=None, condition="presence"):
        """
        Ожидание появления элемента на странице
        
        Args:
            selector: CSS селектор
            timeout: Таймаут ожидания (если None, используется стандартный)
            condition: Тип условия ("presence", "visible", "clickable")
            
        Returns:
            WebElement или None: Элемент если найден, иначе None
        """
        try:
            wait = self.wait if timeout is None else self.driver
            
            conditions = {
                "presence": EC.presence_of_element_located,
                "visible": EC.visibility_of_element_located,
                "clickable": EC.element_to_be_clickable
            }
            
            condition_func = conditions.get(condition, EC.presence_of_element_located)
            element = wait.until(condition_func((By.CSS_SELECTOR, selector)))
            return element
            
        except TimeoutException:
            print(f"Таймаут ожидания элемента: {selector}")
            return None
        except Exception as e:
            print(f"Ошибка ожидания элемента {selector}: {e}")
            return None
    
    def find_elements(self, selector, parent=None):
        """
        Поиск всех элементов по селектору
        
        Args:
            selector: CSS селектор
            parent: Родительский элемент (для поиска внутри него)
            
        Returns:
            list: Список найденных WebElement
        """
        try:
            if parent:
                return parent.find_elements(By.CSS_SELECTOR, selector)
            else:
                return self.driver.find_elements(By.CSS_SELECTOR, selector)
        except Exception as e:
            print(f"Ошибка поиска элементов {selector}: {e}")
            return []
    
    def open_url(self, url, wait_time=3):
        """
        Открытие URL с ожиданием загрузки
        Добавлена случайная задержка для имитации человека
        
        Args:
            url: URL для открытия
            wait_time: Базовое время ожидания после загрузки
        """
        self.driver.get(url)
        # Добавляем случайность к задержке
        actual_wait = wait_time + random.uniform(0.5, 2.0)
        time.sleep(actual_wait)
    
    def open_new_tab(self, url, wait_time=3):
        """
        Открытие URL в новой вкладке
        
        Args:
            url: URL для открытия
            wait_time: Время ожидания после загрузки (секунды)
            
        Returns:
            str: ID новой вкладки
        """
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(url)
        time.sleep(wait_time)
        return self.driver.current_window_handle
    
    def close_tab_and_switch(self, target_index=0):
        """
        Закрытие текущей вкладки и переключение на другую
        
        Args:
            target_index: Индекс вкладки для переключения
        """
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[target_index])
    
    def get_attribute(self, selector, attribute, index=0):
        """
        Получение атрибута элемента
        
        Args:
            selector: CSS селектор
            attribute: Название атрибута
            index: Индекс элемента (если найдено несколько)
            
        Returns:
            str или None: Значение атрибута или None
        """
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            if elements and len(elements) > index:
                return elements[index].get_attribute(attribute)
        except Exception:
            pass
        return None
    
    def execute_script(self, script, *args):
        """
        Выполнение JavaScript кода
        
        Args:
            script: JavaScript код
            *args: Аргументы для передачи в скрипт
            
        Returns:
            Any: Результат выполнения скрипта
        """
        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            print(f"Ошибка выполнения скрипта: {e}")
            return None
    
    def get_current_url(self):
        """
        Получение текущего URL
        
        Returns:
            str: Текущий URL
        """
        return self.driver.current_url
    
    def refresh_page(self, wait_time=3):
        """
        Обновление страницы
        
        Args:
            wait_time: Время ожидания после обновления (секунды)
        """
        self.driver.refresh()
        time.sleep(wait_time)
    
    def save_page_source(self, filename=None, output_dir="debug"):
        """
        Сохранение HTML исходного кода страницы
        
        Args:
            filename: Имя файла (если None, генерируется автоматически)
            output_dir: Директория для сохранения
            
        Returns:
            str: Путь к сохраненному файлу
        """
        # Создаем директорию
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Генерируем имя файла
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"page_source_{timestamp}.html"
        
        filepath = Path(output_dir) / filename
        
        try:
            # Получаем HTML страницы
            page_source = self.driver.page_source
            
            # Сохраняем в файл
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(page_source)
            
            print(f"HTML сохранен: {filepath}")
            return str(filepath)
        
        except Exception as e:
            print(f"Ошибка сохранения HTML: {e}")
            return None
    
    def save_screenshot(self, filename=None, output_dir="debug"):
        """
        Сохранение скриншота страницы
        
        Args:
            filename: Имя файла (если None, генерируется автоматически)
            output_dir: Директория для сохранения
            
        Returns:
            str: Путь к сохраненному файлу
        """
        # Создаем директорию
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Генерируем имя файла
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        filepath = Path(output_dir) / filename
        
        try:
            # Делаем скриншот
            self.driver.save_screenshot(str(filepath))
            print(f"Скриншот сохранен: {filepath}")
            return str(filepath)
        
        except Exception as e:
            print(f"Ошибка сохранения скриншота: {e}")
            return None
    
    def save_page_debug_info(self, prefix="debug"):
        """
        Сохранение полной отладочной информации (HTML + скриншот)
        
        Args:
            prefix: Префикс для имен файлов
            
        Returns:
            dict: Пути к сохраненным файлам
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        html_file = self.save_page_source(
            filename=f"{prefix}_{timestamp}.html"
        )
        
        screenshot_file = self.save_screenshot(
            filename=f"{prefix}_{timestamp}.png"
        )
        
        # Сохраняем текущий URL
        current_url = self.get_current_url()
        info_file = f"debug/{prefix}_{timestamp}_info.txt"
        
        try:
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write(f"URL: {current_url}\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"HTML file: {html_file}\n")
                f.write(f"Screenshot: {screenshot_file}\n")
            
            print(f"Отладочная информация сохранена в директории debug/")
        except Exception as e:
            print(f"Ошибка сохранения info файла: {e}")
            info_file = None
        
        return {
            "html": html_file,
            "screenshot": screenshot_file,
            "info": info_file,
            "url": current_url
        }