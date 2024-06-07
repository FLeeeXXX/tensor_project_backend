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
from app.cities.service import CityService


router = APIRouter(
    prefix="/api/cities",
    tags=["Cities"]
)


@router.get('/get_cities')
@cache(expire=120)
async def get_cities(city: str) -> list[SCity]:
    return await CityService.find_cities(city)



@router.get("/get_weather")
@cache(expire=120)
async def get_weather(lat: str, lon: str) -> list[SWeather]:
    return await get_weather_city(lat=lat, lon=lon)
