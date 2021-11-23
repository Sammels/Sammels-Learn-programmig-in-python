import requests
import settings
"""
Версия № 2.
1. Добавленл исключение raisw_for_status (def weather_by_city)
2. и try:,except
3. Если сервер пришлет некоректный JSON, то будет ошибка значения (ValueError)

"""
# Принять строку город, сформировать запрос -> на сайт погоды.


def weather_by_city(city_name: str) -> str:
    weather_url = "http://api.worldweatheronline.com/premium/v1/weather.ashx"
    params = {
        "key": settings.API_Key,
        "q": city_name,
        "format": "json",
        "num_of_days": 1,
        "lang": "ru"
    }
    try:
        result = requests.get(weather_url, params=params)
        result.raise_for_status()
        weather = result.json()
        if 'data' in weather:
            if 'current_condition' in weather['data']:
                try:
                    return weather['data']['current_condition'][0]
                except(IndexError, TypeError):
                    return False

    except(requests.RequestException, ValueError):
        return False
    return False

    return result


if __name__ == "__main__":
    weather = weather_by_city("Bryansk,Russia")
    print(weather)
