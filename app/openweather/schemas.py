from pydantic import BaseModel, Field


class SWeatherPeriod(BaseModel):
    period: str
    wind_speed: float
    humidity: int
    feels_like: float
    temp_min: int
    temp_max: int
    weather: str
    weather_id: int


class SWeather(BaseModel):
    date: str
    temp_min: int
    temp_max: int
    weather: str
    periods: list[SWeatherPeriod]
