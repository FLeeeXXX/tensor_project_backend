from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings


class MongoDB:
	def __init__(self):
		self.client = AsyncIOMotorClient(settings.MONGO_URL)
		self.database = self.client['cities']
		self.collection = self.database['cities']


mongodb = MongoDB()
