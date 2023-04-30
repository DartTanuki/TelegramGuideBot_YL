import requests
from bot.data.config import GEOCODER_TOKEN

# ---------------------------YANDEX GEOCODER CONFIG-------------------------------

# Ключ доступа Геокодера.
geocoder_api_key = GEOCODER_TOKEN
# Сервер для получения результата.
geocoder_server = 'http://geocode-maps.yandex.ru/1.x/'


# Функция получения координат введенного пользователем города.
async def get_city_cords(city: str) -> list:
    geocoder_params = {
        "apikey": geocoder_api_key,
        "format": "json",
        "geocode": city
    }
    response = requests.get(geocoder_server, params=geocoder_params).json()
    toponym = response["response"]["GeoObjectCollection"]["featureMember"][0]
    cords = toponym["GeoObject"]["Point"]["pos"].split()
    return cords
