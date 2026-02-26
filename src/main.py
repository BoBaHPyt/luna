from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, Security
from fastapi.security import APIKeyHeader
from src.api.router import api_router
from src.api.deps import get_api_key
from src.infrastructure.database import engine, Base, close_db
from src.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager для подключения к БД"""
    yield
    # При остановке закрываем соединение
    await close_db()


app = FastAPI(
    title="Luna API",
    description="Справочник организаций",
    version="1.0.0",
    lifespan=lifespan,
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = FastAPI.openapi(app)
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKey": {
            "type": "apiKey",
            "name": "X-API-Key",
            "in": "header",
            "description": "API ключ для доступа к Luna API",
        }
    }
    # Добавляем security по умолчанию для всех endpoints
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"ApiKey": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Включаем роутер с глобальной зависимостью
app.include_router(api_router, prefix="/api/v1", dependencies=[Security(get_api_key)])
