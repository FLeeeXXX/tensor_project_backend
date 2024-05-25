from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.users.enum import GenderEnum
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

clothes_weatherLabels_association = Table(
    'clothes_weatherLabels_association',
    Base.metadata,
    Column('clothes_id', ForeignKey('clothes.id')),
    Column('weather_labels_id', ForeignKey('weather_labels.id')),
    Column('weathers_id', ForeignKey('weathers.id')),
)

class Clothes(Base):
    __tablename__ = "clothes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(Integer, ForeignKey("clothes_types.id"), nullable=False)
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
    temp_min = Column(Integer, nullable=False)
    temp_max = Column(Integer, nullable=False)
    weather_lable = relationship("WeatherLabels", secondary=clothes_weatherLabels_association)
