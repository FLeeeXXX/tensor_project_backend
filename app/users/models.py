from app.database import Base
from sqlalchemy import Column, Integer, String

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    city = Column(String, nullable=False, default="Москва")
