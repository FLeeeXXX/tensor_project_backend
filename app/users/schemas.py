from pydantic import BaseModel, EmailStr


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


    class Config:
        from_attributes = True
