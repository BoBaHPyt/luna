from dataclasses import dataclass
from decimal import Decimal


@dataclass
class BuildingEntity:
    id: int
    address: str
    latitude: Decimal
    longitude: Decimal
