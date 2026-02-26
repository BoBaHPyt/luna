from dataclasses import dataclass
from typing import Optional


@dataclass
class ActivityEntity:
    id: int
    name: str
    level: int
    parent_id: Optional[int] = None
