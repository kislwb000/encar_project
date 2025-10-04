"""
Field mappings and data structures
Маппинги полей и структуры данных
"""

# Структура данных автомобиля
CAR_DATA = {
    # Основные данные
    "brand": "",
    "model": "",
    "price": "",
    "configuration": "",
    "year": "",
    "mileage": "",
    "fuel": "",
    "vehnumber": "",
    # Данные из модального окна
    "transmission": "",
    "car_type": "",
    "color": "",
    "seating": "",
    "displacement": "",
    "region": "",
    # Дополнительные данные
    "id": "",
    "url": "",
    "parsed_at": "",
    "images": [],
    "options": {},
}

# Опции автомобиля (по умолчанию все False)
CAR_OPTIONS = {
    # Внешние опции
    "sunroof": False,
    "head_lamp_(hid,_led)": False,
    "power_electric_trunk": False,
    "ghost_door_closing": False,
    "electric_contacts_side_mirror": False,
    "aluminum_wheel": False,
    "roof_rack": False,
    # Рулевое управление
    "thermal_steering_wheel": False,
    "electric_control_steering_wheel": False,
    "paddle_shift": False,
    "steering_wheel_remote_control": False,
    "power_steering_wheel": False,
    # Зеркала и системы
    "ecm_room_mirror": False,
    "high_pass": False,
    # Двери и окна
    "power_door_lock": False,
    "power_windows": False,
    # Безопасность - подушки безопасности
    "airbag_(driver_seat,_passenger_seat)": False,
    "airbag_(side)": False,
    "airbag_(curtain)": False,
    # Безопасность - системы помощи
    "brake_lock_(abs)": False,
    "anti_-slip_(tcs)": False,
    "body_posture_control_device_(esc)": False,
    "tire_air_ap_sensor_(tpms)": False,
    "lane_departure_alarm_system_(ldws)": False,
    "electronic_control_suspension_(ecs)": False,
    # Парковка и камеры
    "parking_detection_sensor_(front,_rear)": False,
    "rear_alarm_system": False,
    "rear_camera": False,
    "360_degree_around_view": False,
    # Системы управления
    "cruise_control_(general,_adaptive)": False,
    "head_-up_display_(hud)": False,
    "electronic_parking_brake_(epb)": False,
    # Климат-контроль
    "automatic_air_conditioner": False,
    # Доступ и удобство
    "smart_key": False,
    "wireless_door_lock": False,
    "rain_sensor": False,
    "auto_light": False,
    "curtain/blind_(back_seat,_rear)": False,
    # Мультимедиа
    "navigation": False,
    "front_seat_av_monitor": False,
    "back_seat_av_monitor": False,
    "bluetooth": False,
    "cd_player": False,
    "usb_terminal": False,
    "aux_terminal": False,
    # Сиденья - материал и тип
    "leather_sheet": False,
    # Сиденья - электрорегулировки
    "electric_seat_(driver_seat,_passenger_seat)": False,
    "electric_sheet_(back_seat)": False,
    # Сиденья - обогрев и вентиляция
    "heated_seats_(front_seats,_rear_seats)": False,
    "memory_sheet_(driver's_seat,_passenger_seat)": False,
    "ventilation_sheet_(driver's_seat,_passenger_seat)": False,
    "ventilation_sheet_(back_seat)": False,
    "massage_sheet": False,
}

# Маппинг корейских названий полей на английские ключи
FIELD_MAPPING = {
    "변속기": "transmission",  # Коробка передач
    "차종": "car_type",  # Тип кузова
    "색상": "color",  # Цвет
    "인승": "seating",  # Количество мест
    "배기량": "displacement",  # Объем двигателя
    "지역": "region",  # Регион
}

# Поля, которые нужно переводить
FIELDS_TRANSLATE = {
    "brand",
    "model",
    "configuration",
    "fuel",
    "vehnumber",
    # Данные из модального окна
    "transmission",
    "car_type",
    "color",
    "seating",
    "displacement",
    "region",
}

# Порядок полей для экспорта в CSV
CSV_FIELD_ORDER = [
    "id",
    "brand",
    "model",
    "year",
    "price",
    "mileage",
    "fuel",
    "transmission",
    "car_type",
    "color",
    "seating",
    "displacement",
    "configuration",
    "region",
    "vehnumber",
    "url",
    "parsed_at",
    "images",
    "options",
]
