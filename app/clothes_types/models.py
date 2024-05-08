from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class ClothesTypes(Base):
    __tablename__ = "clothes_types"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, unique=True)
