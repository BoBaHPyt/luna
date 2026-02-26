from dataclasses import dataclass
from typing import Optional


@dataclass
class ActivityDTO:
    id: int
    name: str
    level: int
    parent_id: Optional[int] = None

    @classmethod
    def from_entity(cls, entity) -> "ActivityDTO":
        return cls(
            id=entity.id,
            name=entity.name,
            level=entity.level,
            parent_id=entity.parent_id,
        )
