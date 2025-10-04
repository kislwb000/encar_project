"""
WebDriver setup and configuration with anti-captcha measures
Настройка WebDriver с мерами против капчи
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


def setup_chrome_driver(headless=True, window_size="1920,1080"):
    """
    Настройка и создание Chrome WebDriver с анти-детекцией

    Args:
        headless: Запуск в headless режиме
        window_size: Размер окна браузера

    Returns:
        tuple: (driver, wait) - экземпляры WebDriver и WebDriverWait

    Raises:
        Exception: При ошибке инициализации драйвера
    """
    chrome_options = Options()

    # Headless режим (новая версия)
    if headless:
        chrome_options.add_argument("--headless=new")

    # Основные настройки для стабильности
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"--window-size={window_size}")

    # АНТИ-ДЕТЕКЦИЯ: Скрытие признаков автоматизации
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # SSL настройки
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--ignore-certificate-errors")

    # Отключаем лишнее для стабильности
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")

    # Логи
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--silent")

    # Реалистичный User Agent
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # Дополнительные параметры для обхода детекции
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")

    # Языковые настройки
    chrome_options.add_argument("--lang=ko-KR")
    chrome_options.add_experimental_option(
        "prefs", {"intl.accept_languages": "ko,ko-KR,en-US,en"}
    )

    try:
        driver = webdriver.Chrome(options=chrome_options)

        # КРИТИЧНО: Скрываем webdriver property через JavaScript
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });

                // Дополнительная маскировка
                window.navigator.chrome = {
                    runtime: {}
                };

                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });

                Object.defineProperty(navigator, 'languages', {
                    get: () => ['ko-KR', 'ko', 'en-US', 'en']
                });
            """
            },
        )

        wait = WebDriverWait(driver, 15)
        print("Chrome WebDriver инициализирован (anti-captcha режим)")
        return driver, wait

    except Exception as e:
        print(f"Ошибка инициализации WebDriver: {e}")
        raise


def test_chromedriver():
    """
    Тестирование ChromeDriver

    Returns:
        bool: True если тест успешен, False иначе
    """
    try:
        print("Тестируем ChromeDriver...")
        driver, wait = setup_chrome_driver(headless=True)
        driver.get("https://www.google.com")
        title = driver.title
        print(f"Заголовок страницы: {title}")

        # Проверяем, скрыт ли webdriver
        is_webdriver = driver.execute_script("return navigator.webdriver")
        print(f"navigator.webdriver: {is_webdriver}")

        driver.quit()
        print("Тест успешен! ChromeDriver работает корректно.")
        return True
    except Exception as e:
        print(f"Ошибка при тестировании ChromeDriver: {e}")
        return False


def manual_chromedriver_setup():
    """
    Вывод инструкций по ручной установке ChromeDriver
    """
    print("\nРУЧНАЯ УСТАНОВКА CHROMEDRIVER:")
    print("1. Откройте Chrome и перейдите на: chrome://version/")
    print("2. Запомните версию Chrome (например: 120.0.6099.109)")
    print("3. Перейдите на: https://chromedriver.chromium.org/downloads")
    print("4. Скачайте ChromeDriver для вашей версии Chrome")
    print("5. Распакуйте chromedriver.exe в папку с проектом")
    print("6. В коде укажите путь к chromedriver.exe")


if __name__ == "__main__":
    print("Настройка ChromeDriver для парсера")
    print("=" * 50)

    success = test_chromedriver()

    if not success:
        manual_chromedriver_setup()
