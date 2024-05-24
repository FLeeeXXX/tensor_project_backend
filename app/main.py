import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.users.router import router as users_router
from app.cities.router import router as cities_router


app = FastAPI()
app.include_router(users_router)
app.include_router(cities_router)


origins = [
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# alembic init migrations - создать миграции
# alembic revision --autogenerate -m "Initial"
# alembic upgrade head || "version"


# потом main:app поменять на app и удалить reload (если нужно)
# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)
