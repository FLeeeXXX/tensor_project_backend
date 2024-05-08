from pydantic import BaseModel

class SWeather(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode: True
        