from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class BuildingDTO:
    id: int
    address: str
    latitude: Decimal
    longitude: Decimal

    @classmethod
    def from_entity(cls, entity) -> "BuildingDTO":
        return cls(
            id=entity.id,
            address=entity.address,
            latitude=entity.latitude,
            longitude=entity.longitude,
        )
