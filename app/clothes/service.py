from app.service.base import BaseService
from app.clothes.models import Clothes, clothes_weatherLabels_association
from app.database import async_session_maker
from sqlalchemy import select
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
                .filter(clothes_weatherLabels_association.weather_labels_id == weather_id)
				.filter(clothes_weatherLabels_association.weathers_id == (int(month%12/3) + 1))
                .filter(Clothes.temp_min <= feels_like)
                .filter(Clothes.temp_max >= feels_like)
            )

			result = await session.execute(query)
            return result.mappings().all()
