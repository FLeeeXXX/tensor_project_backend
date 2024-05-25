from app.database import Base
from app.users.enum import GenderEnum
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    gender = Column(
        PgEnum(
            GenderEnum, 
            name="users_gender_enum", 
            create_type=False,
            values_callable=lambda e: [field.value for field in e],
            ), 
            nullable=False, 
            default=GenderEnum.MALE
        )
    password = Column(String, nullable=False)
    city = Column(String, nullable=False, default="Москва")
