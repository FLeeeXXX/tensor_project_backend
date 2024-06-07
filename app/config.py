from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    MONGO_USER: str
    MONGO_PASS: str
    REDIS_HOST: str
    REDIS_PORT: int
    SECRET_KEY: str
    HASH_ALGORITHM: str
    OW_KEY: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
    
    @property
    def MONGO_URL(self):
        return f"mongodb+srv://{self.MONGO_USER}:{self.MONGO_PASS}@cluster0.r949jks.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


    class Config:
        env_file = ".env"


settings = Settings()