from pydantic import BaseModel, EmailStr
from app.users.enum import GenderEnum


class SUsersRegister(BaseModel):
    login: str
    email: EmailStr
    password: str


    class Config:
        orm_mode: True


class SUsersAuth(BaseModel):
    email: EmailStr
    password: str


    class Config:
        orm_mode: True


class SUsersRead(BaseModel):
    email: EmailStr
    login: str
    city: str
    gender: GenderEnum


    class Config:
        from_attributes = True
