# Прогноз погоды

**_Перед инициализацией мастера прогноза погоды следует создать
в корневой папке проекта файл .env и записать туда свой ключ доступа
в формате:_**
```
YANDEX_API_KEY = '<ваш ключ>'
```

Данные, включаемые в прогноз, разнятся. Определимся с базовыми:
- температура сейчас
- влажность
- облачно, безоблачно, ясно
- скорость ветра
- делаем то же на +3 дня

Инициализируем модуль прогноза погоды:
```
weather_master = WeatherMaster()
```

## Публичные методы

### 1. Получение прогноза погоды автоматически для текущих координат
```
def get_own_forecast() -> str
```
Пример:
```
weather_master.get_own_forecast()
```
Возвращается:
```
Город: Fryazino, дата: 18 июля, температура: 26 градусов по Цельсию, влажность: 66 процентов, облачность: Значительная облачность, скорость ветра: 1.5 метров в секунду, дата: 19 июля, температура: 21 градусов по Цельсию, влажность: 79 процентов, облачность: Пасмурно, скорость ветра: 2.5 метров в секунду, дата: 20 июля, температура: 23 градусов по Цельсию, влажность: 62 процентов, облачность: Пасмурно, скорость ветра: 2.7 метров в секунду, дата: 21 июля, температура: 23 градусов по Цельсию, влажность: 62 процентов, облачность: Пасмурно, скорость ветра: 2.7 метров в секунду
```
Название города возвращается на транслите, т.к. используется сервис ipinfo.io,
возможно привести к виду на русском языке путем установки дополнительной библиотеки
### 2. Получение прогноза погоды для конкретного города
```
def get_city_forecast(city: str) -> str
```
Пример:
```
weather_master.get_city_forecast("Рим")
```
Возвращается:
```
Город: Рим, дата: 18 июля, температура: 34 градусов по Цельсию, влажность: 31 процентов, облачность: Ясно, скорость ветра: 4.6 метров в секунду, дата: 19 июля, температура: 36 градусов по Цельсию, влажность: 33 процентов, облачность: Ясно, скорость ветра: 5.9 метров в секунду, дата: 20 июля, температура: 34 градусов по Цельсию, влажность: 39 процентов, облачность: Ясно, скорость ветра: 5.8 метров в секунду, дата: 21 июля, температура: 34 градусов по Цельсию, влажность: 45 процентов, облачность: Ясно, скорость ветра: 5.6 метров в секунду
```
