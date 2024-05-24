from app.database import Base
from app.users.enum import GenderEnum
from sqlalchemy import Column, Integer, String, Enum

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    gender = Column(Enum(GenderEnum), default=GenderEnum.male, nullable=False)
    password = Column(String, nullable=False)
    city = Column(String, nullable=False, default="Москва")
