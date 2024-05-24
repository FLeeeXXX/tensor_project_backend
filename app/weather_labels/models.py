from app.database import Base
from sqlalchemy import Column, Integer, String

class Weather_labels(Base):
    __tablename__ = "weather_labels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
