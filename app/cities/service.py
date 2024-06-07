from app.mongo.base import MongoBaseService


class CityService(MongoBaseService):
    collection_name = "cities"

    @classmethod
    async def find_cities(cls, city_name: str = None) -> list:
        query = {}
        if city_name:
            query = {"city_name": {"$regex": city_name, "$options": "i"}}
        return await cls.find_all(**query)
