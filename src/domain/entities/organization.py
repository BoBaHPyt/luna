from dataclasses import dataclass
from typing import Optional


@dataclass
class OrganizationEntity:
    id: int
    name: str
    building_id: int
    phones: list[str]
    activity_ids: list[int]
