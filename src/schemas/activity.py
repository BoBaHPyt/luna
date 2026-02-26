from pydantic import BaseModel, Field
from typing import Optional


class ActivityResponse(BaseModel):
    id: int
    name: str
    level: int
    parent_id: Optional[int] = None

    class Config:
        from_attributes = True


class ActivityTreeResponse(ActivityResponse):
    """Дерево деятельностей с дочерними элементами"""
    children: list["ActivityTreeResponse"] = []


class ActivityListResponse(BaseModel):
    activities: list[ActivityResponse]
