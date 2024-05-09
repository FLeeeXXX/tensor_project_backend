from fastapi_cache.decorator import cache
from openweather.service import OpenWeatherHTTPClient
from config import settings
from openweather.schemas import SWeather
import datetime

# Может быть можно обыграть зависимостями, если нет, то файл переименовать

@cache(expire=120)
async def get_weather_city(lat: str, lon: str):
    open_weather_client = OpenWeatherHTTPClient(base_url="https://api.openweathermap.org",
                                                api_key=settings.OW_KEY)
    data = await open_weather_client.get_weather(lat=lat, lon=lon)
    return filter_weather(data)


def filter_weather(data: object) -> list[SWeather]:
    result = []

    for item in data['list']:
        date = datetime.datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
        result_item = next((x for x in result if x["date"] == date), None)

        if not result_item:
            result_item = {
                "date": date,
                "temp_min": round(item['main']['temp_min'], 0),
                "temp_max": round(item['main']['temp_max'], 0),
                "weather": item['weather'][0]['description'],
                "periods": {
                    "morning": {},
                    "afternoon": {},
                    "evening": {}
                }
            }
            result.append(result_item)
        else:
            result_item["temp_min"] = round(min(result_item["temp_min"], item['main']['temp_min']), 0)
            result_item["temp_max"] = round(max(result_item["temp_max"], item['main']['temp_max']), 0)

        hour = datetime.datetime.fromtimestamp(item['dt']).hour
        if 6 <= hour < 12:
            period = "morning"
        elif 12 <= hour < 18:
            period = "afternoon"
        elif 18 <= hour < 24:
            period = "evening"
        else:
            continue

        period_data = result_item["periods"][period]
        keys = ["wind_speed", "humidity", "feels_like"]
        for key in keys:
            if key not in period_data:
                period_data[key] = []
            period_data[key].append(item['main'][key] if key != "wind_speed" else item["wind"]["speed"])

        period_data["temp_min"] = round(min(period_data.get("temp_min", item['main']['temp_min']), item['main']['temp_min']), 0)
        period_data["temp_max"] = round(max(period_data.get("temp_max", item['main']['temp_max']), item['main']['temp_max']), 0)
        period_data["weather"] = item['weather'][0]['description']

    # Фильтруем результаты, оставляя только те дни, у которых есть данные во всех трех периодах
    result = [item for item in result if all(period for period in item["periods"].values())]

    for item in result:
        for period, data in item["periods"].items():
            for key in ["wind_speed", "humidity", "feels_like"]:
                if key in data and isinstance(data[key], list):
                    data[key] = round(sum(data[key]) / len(data[key]), 0)

    return result

