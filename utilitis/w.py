import requests
from datetime import datetime

API_KEY = "efa3300b83c778ab44c9a513620b8d0e"
lat = 55.75
lon = 37.62

url = "https://api.openweathermap.org/data/2.5/forecast"
params = {
    "lat": lat,
    "lon": lon,
    "appid": API_KEY,
    "units": "metric",
    "lang": "ru"
}

try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    # Все прогнозы (список с шагом 3 часа)
    forecasts = data.get("list", [])

    # Ограничиваемся первыми 3 днями (24 записи = 3 дня × 8 записей в день)
    three_days = forecasts

    print("Прогноз погоды на 3 дня (с шагом 3 часа):\n")
    for item in three_days:
        dt = datetime.fromtimestamp(item["dt"])
        print(item)
        temp = item["main"]["temp"]
        desc = item["weather"][0]["description"]

except requests.exceptions.RequestException as e:
    print(f"Ошибка: {e}")