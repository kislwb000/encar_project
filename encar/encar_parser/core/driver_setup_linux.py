"""
WebDriver setup and configuration for Ubuntu Server
Настройка WebDriver для Ubuntu сервера с анти-капча мерами
"""
import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait


def setup_chrome_driver(headless=True, window_size="1920,1080"):
    """
    Настройка Chrome WebDriver для Ubuntu сервера
    
    Args:
        headless: Запуск в headless режиме (обязательно True для сервера)
        window_size: Размер окна браузера
        
    Returns:
        tuple: (driver, wait) - экземпляры WebDriver и WebDriverWait
        
    Raises:
        Exception: При ошибке инициализации драйвера
    """
    chrome_options = Options()
    
    # КРИТИЧНО для Ubuntu сервера без GUI
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Дополнительные настройки для серверной среды
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument(f"--window-size={window_size}")
    
    # Для работы в Docker/контейнерах
    chrome_options.add_argument("--disable-setuid-sandbox")
    
    # АНТИ-ДЕТЕКЦИЯ
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # SSL и безопасность
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    
    # Отключаем лишнее
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-infobars")
    
    # Производительность
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("--dns-prefetch-disable")
    
    # Логи
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--silent")
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"]
    )
    
    # User Agent
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    
    # Языковые настройки
    chrome_options.add_argument("--lang=ko-KR")
    chrome_options.add_experimental_option(
        "prefs", {
            "intl.accept_languages": "ko,ko-KR,en-US,en",
            "profile.default_content_setting_values.notifications": 2,
            "profile.managed_default_content_settings.images": 1
        }
    )
    
    # Дополнительная маскировка
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    
    try:
        # Определяем путь к chromedriver
        service = None
        
        # Попытка использовать системный chromedriver
        if os.path.exists("/usr/bin/chromedriver"):
            service = Service("/usr/bin/chromedriver")
            print("Используется системный ChromeDriver: /usr/bin/chromedriver")
        elif os.path.exists("/usr/local/bin/chromedriver"):
            service = Service("/usr/local/bin/chromedriver")
            print("Используется ChromeDriver: /usr/local/bin/chromedriver")
        else:
            # Используем webdriver-manager для автоустановки
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                print("ChromeDriver установлен через webdriver-manager")
            except ImportError:
                print("⚠️ webdriver-manager не найден, используется системный driver")
        
        # Создаем драйвер
        if service:
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            driver = webdriver.Chrome(options=chrome_options)
        
        # Маскировка webdriver property
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                
                window.navigator.chrome = {
                    runtime: {}
                };
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['ko-KR', 'ko', 'en-US', 'en']
                });
                
                // Дополнительная маскировка для Ubuntu
                Object.defineProperty(navigator, 'platform', {
                    get: () => 'Linux x86_64'
                });
            """
            },
        )
        
        wait = WebDriverWait(driver, 15)
        print("✅ Chrome WebDriver успешно инициализирован (Ubuntu Server)")
        return driver, wait
        
    except Exception as e:
        print(f"❌ Ошибка инициализации WebDriver: {e}")
        print("\n📋 Убедитесь что установлены:")
        print("   - Google Chrome или Chromium")
        print("   - ChromeDriver")
        print("\nКоманды для установки на Ubuntu:")
        print_ubuntu_install_instructions()
        raise


def print_ubuntu_install_instructions():
    """Инструкции по установке Chrome и ChromeDriver на Ubuntu"""
    print("\n" + "="*60)
    print("УСТАНОВКА CHROME И CHROMEDRIVER НА UBUNTU")
    print("="*60)
    print("""
# 1. Обновление системы
sudo apt update && sudo apt upgrade -y

# 2. Установка зависимостей
sudo apt install -y wget curl unzip xvfb libxi6 libgconf-2-4

# 3. Установка Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb

# 4. Проверка версии Chrome
google-chrome --version

# 5. Установка ChromeDriver (автоматически)
# Используется через webdriver-manager в коде

# ИЛИ установка вручную:
# Узнайте версию Chrome и скачайте соответствующий ChromeDriver:
# https://chromedriver.chromium.org/downloads

# Пример для ChromeDriver 120:
# wget https://chromedriver.storage.googleapis.com/120.0.6099.109/chromedriver_linux64.zip
# unzip chromedriver_linux64.zip
# sudo mv chromedriver /usr/bin/chromedriver
# sudo chmod +x /usr/bin/chromedriver

# 6. Проверка установки
chromedriver --version

# 7. Для запуска без GUI (если нужно)
# export DISPLAY=:99
# Xvfb :99 -screen 0 1920x1080x24 &
""")
    print("="*60)


def check_chrome_installation():
    """
    Проверка установки Chrome и ChromeDriver
    
    Returns:
        dict: Информация об установке
    """
    result = {
        "chrome_installed": False,
        "chrome_version": None,
        "chromedriver_installed": False,
        "chromedriver_version": None,
        "platform": platform.system(),
    }
    
    # Проверка Chrome
    chrome_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            result["chrome_installed"] = True
            try:
                import subprocess
                version = subprocess.check_output(
                    [path, "--version"], 
                    stderr=subprocess.DEVNULL
                ).decode().strip()
                result["chrome_version"] = version
                break
            except:
                pass
    
    # Проверка ChromeDriver
    chromedriver_paths = [
        "/usr/bin/chromedriver",
        "/usr/local/bin/chromedriver",
    ]
    
    for path in chromedriver_paths:
        if os.path.exists(path):
            result["chromedriver_installed"] = True
            try:
                import subprocess
                version = subprocess.check_output(
                    [path, "--version"],
                    stderr=subprocess.DEVNULL
                ).decode().strip()
                result["chromedriver_version"] = version
                break
            except:
                pass
    
    return result


def test_chromedriver():
    """
    Тестирование ChromeDriver на Ubuntu
    
    Returns:
        bool: True если тест успешен
    """
    try:
        print("\n🧪 Тестирование ChromeDriver на Ubuntu...")
        print("="*60)
        
        # Проверка установки
        info = check_chrome_installation()
        print(f"Платформа: {info['platform']}")
        print(f"Chrome установлен: {info['chrome_installed']}")
        if info['chrome_version']:
            print(f"Версия Chrome: {info['chrome_version']}")
        print(f"ChromeDriver установлен: {info['chromedriver_installed']}")
        if info['chromedriver_version']:
            print(f"Версия ChromeDriver: {info['chromedriver_version']}")
        print()
        
        if not info['chrome_installed']:
            print("❌ Chrome не установлен!")
            print_ubuntu_install_instructions()
            return False
        
        # Тест драйвера
        print("Запуск тестового браузера...")
        driver, wait = setup_chrome_driver(headless=True)
        
        print("Открытие тестовой страницы...")
        driver.get("https://www.google.com")
        
        title = driver.title
        print(f"Заголовок страницы: {title}")
        
        # Проверка маскировки
        is_webdriver = driver.execute_script("return navigator.webdriver")
        print(f"navigator.webdriver скрыт: {is_webdriver is None}")
        
        user_agent = driver.execute_script("return navigator.userAgent")
        print(f"User-Agent: {user_agent[:50]}...")
        
        driver.quit()
        print("\n✅ Тест успешно пройден!")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка при тестировании: {e}")
        print("\n🔧 Рекомендации:")
        print("1. Убедитесь что Chrome установлен")
        print("2. Проверьте права доступа к chromedriver")
        print("3. Проверьте совместимость версий Chrome и ChromeDriver")
        return False


if __name__ == "__main__":
    print("🐧 Настройка ChromeDriver для Ubuntu Server")
    print("="*60)
    
    success = test_chromedriver()
    
    if not success:
        print("\n📖 Для установки запустите:")
        print_ubuntu_install_instructions()