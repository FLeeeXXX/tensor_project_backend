from fastapi_cache.decorator import cache
from app.openweather.service import OpenWeatherHTTPClient
from app.config import settings
from app.openweather.schemas import SWeather, SWeatherClothes
from datetime import datetime
from app.clothes.service import ClothesService
from app.users.enum import GenderEnum
from app.database import engine


def add_period_data(periods, item):
    time = datetime.strptime(item['dt_txt'], "%Y-%m-%d %H:%M:%S")
    period = get_period(time.hour)

    if period:
        period_data = next((p for p in periods if p['period'] == period), None)
        if not period_data:
            period_data = create_period_data(item, period)
            periods.append(period_data)
        else:
            update_period_data(period_data, item)
    


def get_period(hour):
    if 6 <= hour < 12:
        return 'Утром'
    elif 12 <= hour < 18:
        return 'Днем'
    elif 18 <= hour < 24:
        return 'Вечером'
    return ''



def create_period_data(item, period):
    return {
        'period': period,
        'wind_speed': round(item['wind']['speed'], 0),
        'humidity': round(item['main']['humidity'], 0),
        'feels_like': round(item['main']['feels_like'], 0),
        'temp_min': round(item['main']['temp_min'], 0),
        'temp_max': round(item['main']['temp_max'], 0),
        'weather': item['weather'][0]['description'],
        'weather_id': item['weather'][0]['id'],
        'count': 1,
        'weather_counts': {item['weather'][0]['description']: 1},
        'weather_counts_id': {item['weather'][0]['id']: 1}
    }



def update_period_data(period_data, item):
    period_data['wind_speed'] += round(item['wind']['speed'], 0)
    period_data['humidity'] += round(item['main']['humidity'], 0)
    period_data['feels_like'] += round(item['main']['feels_like'], 0)
    period_data['temp_min'] = round(min(period_data['temp_min'], item['main']['temp_min']), 0)
    period_data['temp_max'] = round(max(period_data['temp_max'], item['main']['temp_max']), 0)
    period_data['count'] += 1

    weather_desc = item['weather'][0]['description']
    weather_id = item['weather'][0]['id']
    period_data['weather_counts'][weather_desc] = period_data['weather_counts'].get(weather_desc, 0) + 1
    period_data['weather_counts_id'][weather_id] = period_data['weather_counts_id'].get(weather_id, 0) + 1

    most_common_weather = max(period_data['weather_counts'].items(), key=lambda x: x[1])[0]
    most_common_weather_id = max(period_data['weather_counts_id'].items(), key=lambda x: x[1])[0]
    period_data['weather'] = most_common_weather
    period_data['weather_id'] = most_common_weather_id



def finalize_period_data(period_data):
    period_data['wind_speed'] = round(period_data['wind_speed'] / period_data['count'], 0)
    period_data['humidity'] = round(period_data['humidity'] / period_data['count'], 0)
    period_data['feels_like'] = round(period_data['feels_like'] / period_data['count'], 0)
    del period_data['count']
    del period_data['weather_counts']
    del period_data['weather_counts_id']



@cache(expire=120)
async def get_clothes(weather_id: int, feels_like: int, month: int) -> SWeatherClothes:
    clothes = await ClothesService.get_clothes_for_weather(weather_id=weather_id, feels_like=feels_like, month=month)
    
    clothes_dict = {
        "male": {"head": [], "body": [], "legs": [], "feet": []},
        "female": {"head": [], "body": [], "legs": [], "feet": []}
    }

    clothes_types_dict = {
        1: "head",
        2: "body",
        3: "legs",
        4: "feet"
    }

    for clothe in clothes:
        gender_key = 'male' if clothe.gender.value == GenderEnum.MALE.value else 'female'
        body_part_key = clothes_types_dict[clothe.type]
        
        if clothe.name not in clothes_dict[gender_key][body_part_key]:
            clothes_dict[gender_key][body_part_key].append(clothe.name)

    return clothes_dict



@cache(expire=120)
async def filter_weather(data: object) -> list[SWeather]:
    result = []
    date_index = {}

    for item in data['list']:
        date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
        if date not in date_index:
            date_index[date] = {
                "date": date,
                "temp_min": round(item['main']['temp_min'], 0),
                "temp_max": round(item['main']['temp_max'], 0),
                "weather": item['weather'][0]['description'],
                "periods": []
            }
            result.append(date_index[date])
        else:
            date_entry = date_index[date]
            date_entry['temp_min'] = round(min(date_entry['temp_min'], item['main']['temp_min']), 0)
            date_entry['temp_max'] = round(max(date_entry['temp_max'], item['main']['temp_max']), 0)

        add_period_data(date_index[date]['periods'], item)

    for entry in result:
        for period_data in entry['periods']:
            finalize_period_data(period_data)
            weather_id = int(period_data['weather_id'])
            feels_like = int(period_data['feels_like'])
            month = int(datetime.strptime(entry['date'], '%Y-%m-%d').month)
            period_data['clothes'] = await get_clothes(weather_id, feels_like, month)

    return result



# Может быть можно обыграть зависимостями, если нет, то файл переименовать
@cache(expire=120)
async def get_weather_city(lat: str, lon: str) -> list[SWeather]:
    open_weather_client = OpenWeatherHTTPClient(base_url="https://api.openweathermap.org",
                                                api_key=settings.OW_KEY)
    data = await open_weather_client.get_weather(lat=lat, lon=lon)
    return await filter_weather(data)
