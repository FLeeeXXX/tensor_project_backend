from fastapi import APIRouter
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from openweather.service import OpenWeatherHTTPClient
from config import settings
import json


router = APIRouter(
    prefix="/api/cities",
    tags=["Cities"]
)


# Декомпозировать или спрятать сложную логику
@router.get("/get_cities")
@cache(expire=120)
async def get_cities(city: str):
    cities_str = await cache_backend.get("cities")
    cities = json.loads(cities_str) if cities_str else []
    search_results = [_city for _city in cities if city.lower() in _city["city_name"].lower()]
    return search_results


@router.get("/get_weather")
@cache(expire=120)
async def get_weather(lat: str, lon: str):
    open_weather_client = OpenWeatherHTTPClient(base_url="https://api.openweathermap.org",
                                                api_key=settings.OW_KEY)
    return await open_weather_client.get_weather(lat=lat, lon=lon)


# Загрузка redis и городов при старте сервера
# Возможно сделано через костыли, но пока не знаю как сделать по другому
@router.on_event("startup")
async def load_cities():
    global cache_backend
    redis = aioredis.from_url("redis://localhost")
    cache_backend = RedisBackend(redis)
    FastAPICache.init(cache_backend, prefix="fastapi-cache")
    with open('../cities.json', 'r', encoding='utf-8-sig') as f:
        city_data = json.load(f)
        cities = city_data if isinstance(city_data, list) else city_data.get("city", [])
        await cache_backend.set("cities", json.dumps(cities))
