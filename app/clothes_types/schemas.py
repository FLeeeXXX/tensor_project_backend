from pydantic import BaseModel

class SClothesTypes(BaseModel):
    id: int
    type: str

    class Config:
        orm_mode: True
        