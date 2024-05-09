from pydantic import BaseModel


class SCity(BaseModel):
    index: int
    region_type: str
    region_name: str
    city_name: str
    lat: str
    lon: str
    