from app.mongo.mongo import mongodb

class MongoBaseService:
    collection_name: str = ""


    @classmethod
    def get_collection(cls):
        return mongodb.database[cls.collection_name]


    @classmethod
    async def find_all(cls, **filter_by) -> list:
        collection = cls.get_collection()
        cursor = collection.find(filter_by, {'_id': 0})
        documents = await cursor.to_list(length=1000)
        return documents

