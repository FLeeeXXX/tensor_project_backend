from app.database import async_session_maker
from sqlalchemy import select, insert

class BaseService:
    model = None

    @classmethod
    async def find_by_id(cls, model_id) -> object:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings().first()

    @classmethod
    async def find_one_or_none(cls, **filter_by) -> object:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().first()
            

    @classmethod
    async def find_all(cls, **filter_by) -> object:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def add(cls, **data) -> None:
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
        