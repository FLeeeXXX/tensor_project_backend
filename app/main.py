import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.users.router import router as users_router
from app.cities.router import router as cities_router
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from app.config import settings


app = FastAPI()
app.include_router(users_router)
app.include_router(cities_router)


origins = [
    "https://tensor-project-frontend.onrender.com",
    "https://tenzorprojectfront-syl7.onrender.com"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# alembic init migrations - создать миграции
# alembic revision --autogenerate -m "Initial"
# alembic upgrade head || "version"


# потом main:app поменять на app и удалить reload (если нужно)
# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)
