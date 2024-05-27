from pydantic import BaseModel, Field


class SWeatherPartsOfBody(BaseModel):
    head: list[str]
    body: list[str]
    legs: list[str]
    feet: list[str]

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
    clothes: SWeatherClothes


class SWeather(BaseModel):
    date: str
    temp_min: int
    temp_max: int
    weather: str
    periods: list[SWeatherPeriod]
