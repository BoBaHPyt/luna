from src.api.v1.buildings import router as buildings_router
from src.api.v1.activities import router as activities_router
from src.api.v1.organizations import router as organizations_router

__all__ = [
    "buildings_router",
    "activities_router",
    "organizations_router",
]
