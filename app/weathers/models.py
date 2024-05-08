from database import Base
from sqlalchemy import Column, Integer, String

class Weathers(Base):
    __tablename__ = "weathers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
