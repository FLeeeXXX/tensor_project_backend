from pydantic import BaseModel, Field


class SWeatherPartsOfBody(BaseModel):
    head: list
    body: list
    legs: list
    feet: list

class SWeatherClothes(BaseModel):
    male: SWeatherPartsOfBody
    female: SWeatherPartsOfBody

class SWeatherPeriod(BaseModel):
    period: str
    wind_speed: float
    humidity: int
    feels_like: float
    temp_min: int
    temp_max: int
    weather: str
    weather_id: int
    clothes: list[SWeatherClothes]


class SWeather(BaseModel):
    date: str
    temp_min: int
    temp_max: int
    weather: str
    periods: list[SWeatherPeriod]
