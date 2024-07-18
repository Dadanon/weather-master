import os
import re

import requests
import datetime
import locale
from dotenv import load_dotenv

from geopy.geocoders import Nominatim


os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')


humidity_dict = {
    0: 'Ясно',
    0.125: 'Частичная облачность',
    0.25: 'Частичная облачность',
    0.375: 'Значительная облачность',
    0.5: 'Значительная облачность',
    0.625: 'Облачно',
    0.75: 'Облачно',
    0.875: 'Облачно',
    1: 'Пасмурно'
}

months_dict = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря'
}


class WeatherMaster:
    __headers: dict

    def __init__(self):
        load_dotenv(".env")
        self.__headers = {'X-Yandex-Weather-Key': os.getenv("YANDEX_API_KEY")}

    @staticmethod
    def _get_city_coords(city: str) -> dict:
        geolocator = Nominatim(user_agent="weather-master")
        location = geolocator.geocode(city)
        return {'lon': float(location.longitude), 'lat': float(location.latitude)}

    def get_city_forecast(self, city: str) -> str:
        coords = self._get_city_coords(city)
        response = requests.get(
            f'https://api.weather.yandex.ru/v2/forecast?lat={coords["lat"]}&lon={coords["lon"]}',
            headers=self.__headers
        )
        json = response.json()
        return self._normalize_weather(city, json)

    def get_own_forecast(self) -> str:
        ip_info = requests.get('https://ipinfo.io').json()
        loc, city = ip_info['loc'], ip_info['city']
        lat, lon = map(lambda coord: float(coord), loc.split(','))
        response = requests.get(
            f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}',
            headers=self.__headers
        )
        json = response.json()
        return self._normalize_weather(city, json)

    @staticmethod
    def _get_date_str(cur_date_str: str) -> str:
        """Принимает дату из API в формате '2024-07-19',
        возвращает в формате: 19 июля"""
        locale.setlocale(locale.LC_TIME, 'ru_RU.utf8')
        current_date = datetime.datetime.strptime(cur_date_str, '%Y-%m-%d')
        day, month = current_date.day, months_dict[current_date.month]
        return f"{day} {month}"

    def _normalize_weather(self, city: str, json) -> str:
        forecasts = []
        json_fact = json['fact']
        current_date = self._get_date_str(json['forecasts'][0]['date'])

        fact = f"""
        Город: {city},
        дата: {current_date},
        температура: {json_fact['temp']} градусов по Цельсию,
        влажность: {json_fact['humidity']} процентов,
        облачность: {humidity_dict[json_fact['cloudness']]},
        скорость ветра: {json_fact['wind_speed']} метров в секунду
        """
        forecasts.append(re.sub(r'\s{2,}', ' ', fact).strip())

        for forecast in json['forecasts'][1:4]:
            next_date = self._get_date_str(forecast['date'])
            next_temp = forecast['parts']['day']['temp_avg']
            next_humidity = forecast['parts']['day']['humidity']
            next_cloudiness = forecast['parts']['day']['cloudness']
            next_wind_speed = forecast['parts']['day']['wind_speed']
            next_forecast = f"""
            дата: {next_date},
            температура: {next_temp} градусов по Цельсию,
            влажность: {next_humidity} процентов,
            облачность: {humidity_dict[next_cloudiness]},
            скорость ветра: {next_wind_speed} метров в секунду
            """
            forecasts.append(re.sub(r'\s{2,}', ' ', next_forecast).strip())
        return ', '.join(forecasts)


weather_master = WeatherMaster()
print(weather_master.get_own_forecast())
print(weather_master.get_city_forecast("Рим"))
