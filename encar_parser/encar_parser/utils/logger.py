"""
Logging and statistics utilities
Утилиты для логирования и статистики
"""

from datetime import datetime


class ParserLogger:
    """
    Класс для логирования и сбора статистики парсинга
    """

    def __init__(self):
        """Инициализация логгера"""
        self.stats = {
            "total_processed": 0,
            "successful": 0,
            "failed": 0,
            "translation_errors": 0,
            "image_errors": 0,
            "option_errors": 0,
        }

        self.errors = []
        self.start_time = None

    def start(self):
        """Начало отсчета времени"""
        self.start_time = datetime.now()

    def increment(self, counter_name):
        """
        Увеличение счетчика

        Args:
            counter_name: Название счетчика
        """
        if counter_name in self.stats:
            self.stats[counter_name] += 1

    def log_error(self, location, error_message):
        """
        Логирование ошибки

        Args:
            location: Место возникновения ошибки
            error_message: Сообщение об ошибке
        """
        error_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "location": location,
            "message": error_message,
        }
        self.errors.append(error_entry)

    def get_stats(self):
        """
        Получение статистики

        Returns:
            dict: Словарь со статистикой
        """
        return self.stats.copy()

    def get_errors(self):
        """
        Получение списка ошибок

        Returns:
            list: Список ошибок
        """
        return self.errors.copy()

    def print_statistics(self, elapsed_time=None, cars_data=None):
        """
        Вывод статистики парсинга

        Args:
            elapsed_time: Время выполнения (секунды)
            cars_data: Список данных автомобилей для дополнительной статистики
        """
        print("\n" + "=" * 60)
        print("СТАТИСТИКА ПАРСИНГА")
        print("=" * 60)

        # Основная статистика
        if elapsed_time:
            print(f"Время выполнения: {elapsed_time:.1f} сек")

        print(f"Всего обработано: {self.stats['total_processed']}")
        print(f"Успешно: {self.stats['successful']}")
        print(f"Ошибок: {self.stats['failed']}")

        # Детальная статистика ошибок
        if self.stats["translation_errors"] > 0:
            print(f"Ошибок перевода: {self.stats['translation_errors']}")

        if self.stats["image_errors"] > 0:
            print(f"Ошибок изображений: {self.stats['image_errors']}")

        if self.stats["option_errors"] > 0:
            print(f"Ошибок опций: {self.stats['option_errors']}")

        # Статистика по изображениям
        if cars_data:
            total_images = sum(len(car.get("images", [])) for car in cars_data)
            avg_images = total_images / len(cars_data) if cars_data else 0
            print(f"Среднее изображений на авто: {avg_images:.1f}")

            # Статистика по опциям
            total_options = 0
            for car in cars_data:
                options = car.get("options", {})
                if isinstance(options, dict):
                    total_options += sum(1 for v in options.values() if v)

            avg_options = total_options / len(cars_data) if cars_data else 0
            print(f"Среднее опций на авто: {avg_options:.1f}")

        # Процент успешности
        if self.stats["total_processed"] > 0:
            success_rate = (
                self.stats["successful"] / self.stats["total_processed"]
            ) * 100
            print(f"Успешность: {success_rate:.1f}%")

        print("=" * 60)

        # Вывод критических ошибок
        if self.errors:
            print(f"\nЗафиксировано ошибок: {len(self.errors)}")

            # Показываем последние 5 ошибок
            recent_errors = self.errors[-5:]
            if recent_errors:
                print("\nПоследние ошибки:")
                for error in recent_errors:
                    print(
                        f"  [{error['timestamp']}] {error['location']}: {error['message']}"
                    )

    def reset(self):
        """Сброс статистики"""
        self.stats = {
            "total_processed": 0,
            "successful": 0,
            "failed": 0,
            "translation_errors": 0,
            "image_errors": 0,
            "option_errors": 0,
        }
        self.errors = []
        self.start_time = None

    def save_log(self, filename=None, output_dir="logs"):
        """
        Сохранение лога в файл

        Args:
            filename: Имя файла (опционально)
            output_dir: Директория для сохранения

        Returns:
            str: Путь к файлу лога
        """
        import json
        from pathlib import Path

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"parser_log_{timestamp}.json"

        filepath = Path(output_dir) / filename

        log_data = {
            "statistics": self.stats,
            "errors": self.errors,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2)

            print(f"Лог сохранен: {filepath}")
            return str(filepath)

        except Exception as e:
            print(f"Ошибка сохранения лога: {e}")
            return None
