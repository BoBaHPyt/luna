from dataclasses import dataclass
from typing import Optional


@dataclass
class OrganizationDTO:
    id: int
    name: str
    building_id: int
    phones: list[str]
    activity_ids: list[int]

    @classmethod
    def from_entity(cls, entity) -> "OrganizationDTO":
        return cls(
            id=entity.id,
            name=entity.name,
            building_id=entity.building_id,
            phones=entity.phones,
            activity_ids=entity.activity_ids,
        )


@dataclass
class OrganizationDetailDTO:
    """Расширенный DTO с полной информацией о здании и деятельностях"""
    id: int
    name: str
    building_address: str
    building_latitude: float
    building_longitude: float
    phones: list[str]
    activities: list[str]  # Названия деятельностей

    @classmethod
    def from_entity(
        cls,
        entity,
        building_address: str,
        building_lat: float,
        building_lon: float,
        activity_names: list[str]
    ) -> "OrganizationDetailDTO":
        return cls(
            id=entity.id,
            name=entity.name,
            building_address=building_address,
            building_latitude=float(building_lat),
            building_longitude=float(building_lon),
            phones=entity.phones,
            activities=activity_names,
        )
