from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class OrganizationResponse(BaseModel):
    id: int
    name: str
    building_id: int

    class Config:
        from_attributes = True


class OrganizationDetailResponse(BaseModel):
    """Полная информация об организации"""
    id: int
    name: str
    building_address: str
    building_latitude: float
    building_longitude: float
    phones: list[str]
    activities: list[str]


class OrganizationListResponse(BaseModel):
    organizations: list[OrganizationResponse]


class OrganizationSearchResponse(BaseModel):
    organizations: list[OrganizationDetailResponse]
