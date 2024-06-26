from app.service.base import BaseService
from app.clothes.models import Clothes, clothes_weatherLabels_association
from app.database import async_session_maker
from sqlalchemy import select, and_
from app.weathers.models import Weathers
from app.weather_labels.models import Weather_labels

class ClothesService(BaseService):
    model = Clothes

    @classmethod
    async def get_clothes_for_weather(cls, weather_id: int, feels_like: int, month: int):
        async with async_session_maker() as session:
            query = (
				select(cls.model)
				.join(clothes_weatherLabels_association)
				.join(Weathers)
				.join(Weather_labels)
				.filter(Weathers.id == (int(month%12/3) + 1))
				.filter(Weather_labels.id == weather_id)
				.filter(and_(Clothes.temp_min <= feels_like, Clothes.temp_max >= feels_like))
			)

            result = await session.execute(query)
            return result.scalars().all()
