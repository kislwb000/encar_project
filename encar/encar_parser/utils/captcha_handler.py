"""
Captcha detection and handling
Обнаружение и обработка капчи
"""
import time


class CaptchaHandler:
    """
    Класс для обнаружения и обработки капчи
    """
    
    def __init__(self, scraper):
        """
        Args:
            scraper: Экземпляр класса Scraper
        """
        self.scraper = scraper
        
        # Селекторы различных типов капчи
        self.captcha_selectors = [
            # Google reCAPTCHA
            "iframe[src*='recaptcha']",
            "iframe[title*='reCAPTCHA']",
            ".g-recaptcha",
            
            # hCaptcha
            "iframe[src*='hcaptcha']",
            ".h-captcha",
            
            # Общие селекторы
            "iframe[src*='captcha']",
            ".captcha-container",
            "#captcha",
            "[id*='captcha']",
            "[class*='captcha']",
            
            # Encar специфичные (если есть)
            ".verify-container",
            "#verify",
        ]
    
    def check_captcha(self):
        """
        Проверка наличия капчи на странице
        
        Returns:
            bool: True если капча обнаружена
        """
        for selector in self.captcha_selectors:
            elements = self.scraper.find_elements(selector)
            if elements and len(elements) > 0:
                # Проверяем, видим ли элемент
                try:
                    if elements[0].is_displayed():
                        print(f"Обнаружена капча: {selector}")
                        return True
                except:
                    # Если не можем проверить видимость, считаем что капча есть
                    print(f"Возможно обнаружена капча: {selector}")
                    return True
        
        # Дополнительная проверка через URL
        current_url = self.scraper.get_current_url()
        if 'captcha' in current_url.lower() or 'verify' in current_url.lower():
            print(f"Обнаружена капча в URL: {current_url}")
            return True
        
        return False
    
    def wait_for_manual_solve(self, timeout=120):
        """
        Ожидание ручного решения капчи пользователем
        
        Args:
            timeout: Максимальное время ожидания (секунды)
            
        Returns:
            bool: True если капча решена, False если истекло время
        """
        print("\n" + "="*60)
        print("ОБНАРУЖЕНА КАПЧА!")
        print("Пожалуйста, решите капчу вручную в браузере.")
        print(f"Ожидание: {timeout} секунд")
        print("="*60)
        
        start_time = time.time()
        check_interval = 2  # Проверяем каждые 2 секунды
        
        while time.time() - start_time < timeout:
            elapsed = int(time.time() - start_time)
            remaining = timeout - elapsed
            
            # Показываем прогресс
            if elapsed % 10 == 0:
                print(f"Осталось времени: {remaining} секунд...")
            
            # Проверяем, исчезла ли капча
            if not self.check_captcha():
                print("Капча решена! Продолжаем парсинг.")
                time.sleep(2)  # Небольшая пауза после решения
                return True
            
            time.sleep(check_interval)
        
        print("Время ожидания истекло!")
        return False
    
    def handle_captcha(self, auto_solve=False, timeout=120):
        """
        Обработка капчи
        
        Args:
            auto_solve: Попытка автоматического решения (не реализовано)
            timeout: Время ожидания ручного решения
            
        Returns:
            bool: True если капча решена успешно
        """
        if not self.check_captcha():
            # Капчи нет
            return True
        
        if auto_solve:
            # Здесь можно интегрировать сервисы типа 2captcha, anti-captcha
            print("Автоматическое решение капчи не реализовано")
            print("Переключаемся на ручной режим...")
        
        # Ручное решение
        return self.wait_for_manual_solve(timeout=timeout)
    
    def check_and_handle(self, timeout=120):
        """
        Проверить и обработать капчу (удобный метод)
        
        Args:
            timeout: Время ожидания ручного решения
            
        Returns:
            bool: True если капчи нет или она решена
        """
        if self.check_captcha():
            return self.handle_captcha(timeout=timeout)
        return True
    
    def save_captcha_debug(self):
        """
        Сохранение отладочной информации при обнаружении капчи
        
        Returns:
            dict: Информация о сохраненных файлах
        """
        print("Сохраняем отладочную информацию о капче...")
        
        # Сохраняем HTML и скриншот
        debug_info = self.scraper.save_page_debug_info(prefix="captcha")
        
        # Пробуем найти элементы капчи
        captcha_found = []
        for selector in self.captcha_selectors:
            elements = self.scraper.find_elements(selector)
            if elements:
                captcha_found.append({
                    "selector": selector,
                    "count": len(elements)
                })
        
        if captcha_found:
            print(f"Найдено элементов капчи: {captcha_found}")
            debug_info["captcha_elements"] = captcha_found
        
        return debug_info