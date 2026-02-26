import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_KEY: str = "secret-api-key"
    # По умолчанию SQLite async, для PostgreSQL: postgresql+asyncpg://user:pass@localhost/db
    DATABASE_URL: str = "sqlite+aiosqlite:///./luna.db"
    
    class Config:
        env_file = ".env"


settings = Settings()
