from pydantic import BaseModel

class SClothes(BaseModel):
    id: int
    name: str
    type: int
    weather: int

    class Config:
        orm_mode: True
        