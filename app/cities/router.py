from fastapi import APIRouter, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from app.config import settings
from app.cities.schemas import SCity
from app.openweather.schemas import SWeather
from app.openweather.weather import get_weather_city
from app.exceptions import ServerNetworkException
import json


router = APIRouter(
    prefix="/api/cities",
    tags=["Cities"]
)


async def get_cache_backend() -> RedisBackend:
    return FastAPICache.get_backend()


# Декомпозировать или спрятать сложную логику
@router.get("/get_cities")
@cache(expire=120)
async def get_cities(city: str, redis_cities: RedisBackend = Depends(get_cache_backend)) -> list[SCity]:
    cities_str = await redis_cities.get("cities")
    if not cities_str:
        raise ServerNetworkException
    cities = json.loads(cities_str)
    search_results = [_city for _city in cities if city.lower() in _city["city_name"].lower()]
    return search_results


@router.get("/get_weather")
@cache(expire=120)
async def get_weather(lat: str, lon: str) -> list[SWeather]:
    return await get_weather_city(lat=lat, lon=lon)


# Загрузка redis и городов при старте сервера
@router.on_event("startup")
async def load_cities():
    redis = aioredis.from_url(settings.REDIS_URL)
    cache_backend = RedisBackend(redis)
    FastAPICache.init(cache_backend, prefix="fastapi-cache")
    with open('./cities.json', 'r', encoding='utf-8-sig') as f:
        city_data = json.load(f)
        cities = city_data if isinstance(city_data, list) else city_data.get("city", [])
        await cache_backend.set("cities", json.dumps(cities))
