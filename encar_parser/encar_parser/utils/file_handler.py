"""
File handling utilities
Утилиты для работы с файлами
"""

import csv
import json
from datetime import datetime
from pathlib import Path


def save_to_json(data, filename=None, output_dir="output"):
    """
    Сохранение данных в JSON файл

    Args:
        data: Данные для сохранения (list или dict)
        filename: Имя файла (опционально, генерируется автоматически)
        output_dir: Директория для сохранения

    Returns:
        str: Путь к сохраненному файлу
    """
    # Создаем директорию если не существует
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Генерируем имя файла если не указано
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cars_data_{timestamp}.json"

    # Добавляем расширение если отсутствует
    if not filename.endswith(".json"):
        filename += ".json"

    # Полный путь к файлу
    filepath = Path(output_dir) / filename

    try:
        with open(filepath, "w", encoding="utf-8") as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=2)

        print(f"JSON сохранен: {filepath}")
        print(f"Записей: {len(data) if isinstance(data, list) else 1}")

        return str(filepath)

    except Exception as e:
        print(f"Ошибка сохранения JSON: {e}")
        return None


def save_to_csv(data, filename=None, output_dir="output"):
    """
    Сохранение данных в CSV файл

    Args:
        data: Список словарей с данными
        filename: Имя файла (опционально)
        output_dir: Директория для сохранения

    Returns:
        str: Путь к сохраненному файлу
    """
    if not data:
        print("Нет данных для сохранения")
        return None

    # Создаем директорию
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Генерируем имя файла
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cars_data_{timestamp}.csv"

    if not filename.endswith(".csv"):
        filename += ".csv"

    filepath = Path(output_dir) / filename

    try:
        # Получаем все уникальные ключи из всех записей
        fieldnames = set()
        for item in data:
            if isinstance(item, dict):
                fieldnames.update(item.keys())

        fieldnames = sorted(fieldnames)

        with open(filepath, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for item in data:
                # Преобразуем сложные типы в строки
                row = {}
                for key, value in item.items():
                    if isinstance(value, (list, dict)):
                        row[key] = json.dumps(value, ensure_ascii=False)
                    else:
                        row[key] = value
                writer.writerow(row)

        print(f"CSV сохранен: {filepath}")
        print(f"Записей: {len(data)}")

        return str(filepath)

    except Exception as e:
        print(f"Ошибка сохранения CSV: {e}")
        return None


def load_from_json(filepath):
    """
    Загрузка данных из JSON файла

    Args:
        filepath: Путь к файлу

    Returns:
        dict или list: Загруженные данные
    """
    try:
        with open(filepath, "r", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)

        print(f"JSON загружен: {filepath}")
        if isinstance(data, list):
            print(f"Записей: {len(data)}")

        return data

    except FileNotFoundError:
        print(f"Файл не найден: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
        return None
    except Exception as e:
        print(f"Ошибка загрузки JSON: {e}")
        return None


def get_output_files(output_dir="output", extension=".json"):
    """
    Получение списка файлов в директории вывода

    Args:
        output_dir: Директория для поиска
        extension: Расширение файлов

    Returns:
        list: Список путей к файлам
    """
    output_path = Path(output_dir)

    if not output_path.exists():
        return []

    files = list(output_path.glob(f"*{extension}"))
    return [str(f) for f in sorted(files, reverse=True)]
