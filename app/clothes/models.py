from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Clothes(Base):
    __tablename__ = "clothes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(Integer, ForeignKey("clothes_types.id"), nullable=False)
    weather = Column(Integer, ForeignKey("weathers.id"), nullable=False)
