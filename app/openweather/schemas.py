from pydantic import BaseModel, Field


class SWeatherPeriod(BaseModel):
    wind_speed: float
    humidity: int
    feels_like: float
    temp_min: int
    temp_max: int
    weather: str


class SWeather(BaseModel):
    date: str
    temp_min: int
    temp_max: int
    weather: str
    periods: dict[str, SWeatherPeriod]
    