"""
CSS selectors for page elements
CSS селекторы для элементов страниц
"""

# Селекторы для поиска ссылок на автомобили в каталоге
CAR_LINK_SELECTORS = [
    '[id="sr_normal"] tr',
    # '[class*="ItemBigImage_link_item_"]',  # Альтернативный селектор (закомментирован)
]

# Селекторы для кнопки "Детали" (открытие модального окна)
EXTRA_BUTTON_SELECTORS = [
    ".DetailSummary_btn_detail__msm-h",
]

# Селекторы основных данных автомобиля
CAR_DETAIL_SELECTORS = {
    "model": ".DetailSummary_tit_car__0OEVh > span",
    "price": ".DetailLeadCase_point__vdG4b",
    "configuration": ".DetailSummary_tit_car__0OEVh > span",
    "summary_data": ".DetailSummary_define_summary__NOYid > dd",
}

# Селекторы для модального окна с деталями
MODAL_SELECTORS = {
    "container": ".BottomSheet-module_bottom_sheet__LeljN",
    "list_items": "li",
    "title": "strong",
    "value": "span.DetailSpec_txt__NGapF",
}

# Селекторы для слайдера изображений
IMAGE_SELECTORS = {
    "slider_container": ".swiper-wrapper",
    "images": "img[class*=DetailCarPhotoPc_thumb__]",
}

# Селекторы для страницы опций
OPTION_SELECTORS = {
    "option_items": '[class*="PeerIntoCarOptions_"] > a',
}

# Селекторы для каталога
CATALOG_SELECTORS = {
    "car_count": ".allcount",
    "car_item": '[id="sr_normal"] tr',
}
