# from fastapi_cache.decorator import cache
from app.openweather.service import OpenWeatherHTTPClient
from app.config import settings
from app.openweather.schemas import SWeather
from datetime import datetime

# Может быть можно обыграть зависимостями, если нет, то файл переименовать
# @cache(expire=120)
async def get_weather_city(lat: str, lon: str) -> list[SWeather]:
    open_weather_client = OpenWeatherHTTPClient(base_url="https://api.openweathermap.org",
                                                api_key=settings.OW_KEY)
    data = await open_weather_client.get_weather(lat=lat, lon=lon)
    return filter_weather(data)


def filter_weather(data: object) -> list[SWeather]:
    result = []

    for item in data['list']:
        date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
        found_date = False

        for idx, r in enumerate(result):
            if r['date'] == date:
                found_date = True
                r['temp_min'] = round(min(r['temp_min'], item['main']['temp_min']), 0)
                r['temp_max'] = round(max(r['temp_max'], item['main']['temp_max']), 0)
                break

        if not found_date:
            result.append({
                "date": date,
                "temp_min": round(item['main']['temp_min'], 0),
                "temp_max": round(item['main']['temp_max'], 0),
                "weather": item['weather'][0]['description'],
                "periods": {}
            })

        time = datetime.strptime(item['dt_txt'], "%Y-%m-%d %H:%M:%S")

        if int(time.hour) == 0:
            time = time.replace(hour=23)

        period = ''

        if 6 <= time.hour < 12:
            period = 'Утром'
        elif 12 <= time.hour < 18:
            period = 'Днем'
        elif 18 <= time.hour < 24:
            period = 'Вечером'

        if period and period not in result[-1]['periods']:
            result[-1]['periods'][period] = {
                'wind_speed': round(item['wind']['speed'], 0),
                'humidity': round(item['main']['humidity'], 0),
                'feels_like': round(item['main']['feels_like'], 0),
                'temp_min': round(item['main']['temp_min'], 0),
                'temp_max': round(item['main']['temp_max'], 0),
                'weather': item['weather'][0]['description'],
                'weather_counts': {item['weather'][0]['description']: 1},
                'count': 1
            }
        elif period:
            result[-1]['periods'][period]['wind_speed'] += round(item['wind']['speed'], 0)
            result[-1]['periods'][period]['humidity'] += round(item['main']['humidity'], 0)
            result[-1]['periods'][period]['feels_like'] += round(item['main']['feels_like'], 0)
            result[-1]['periods'][period]['temp_min'] = round(min(result[-1]['periods'][period]['temp_min'], item['main']['temp_min']), 0)
            result[-1]['periods'][period]['temp_max'] = round(max(result[-1]['periods'][period]['temp_max'], item['main']['temp_max']), 0)
            result[-1]['periods'][period]['count'] += 1

            weather_counts = result[-1]['periods'][period]['weather_counts']
            weather_counts[item['weather'][0]['description']] = weather_counts.get(item['weather'][0]['description'], 0) + 1
            most_common_weather = max(weather_counts.items(), key=lambda x: x[1])[0]
            result[-1]['periods'][period]['weather'] = most_common_weather

    for idx, value in enumerate(result):
        for period, data in value['periods'].items():
            data['wind_speed'] = round(data['wind_speed'] / data['count'], 0)
            data['humidity'] = round(data['humidity'] / data['count'], 0)
            data['feels_like'] = round(data['feels_like'] / data['count'], 0)
            del data['count']
            del data['weather_counts']

    return result
