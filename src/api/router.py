from fastapi import APIRouter
from src.api.v1 import buildings_router, activities_router, organizations_router

api_router = APIRouter()

api_router.include_router(buildings_router)
api_router.include_router(activities_router)
api_router.include_router(organizations_router)
