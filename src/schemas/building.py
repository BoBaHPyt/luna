from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class BuildingResponse(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    class Config:
        from_attributes = True


class BuildingListResponse(BaseModel):
    buildings: list[BuildingResponse]
