from typing import Optional
from src.domain.repositories.activity_repo import ActivityRepository
from src.application.dto.activity import ActivityDTO


class ActivityService:

    def __init__(self, repo: ActivityRepository):
        self.repo = repo

    async def get_by_id(self, activity_id: int) -> Optional[ActivityDTO]:
        entity = await self.repo.get_by_id(activity_id)
        if entity is None:
            return None
        return ActivityDTO.from_entity(entity)

    async def get_all(self) -> list[ActivityDTO]:
        entities = await self.repo.get_all()
        return [ActivityDTO.from_entity(e) for e in entities]

    async def get_by_name(self, name: str) -> Optional[ActivityDTO]:
        entity = await self.repo.get_by_name(name)
        if entity is None:
            return None
        return ActivityDTO.from_entity(entity)

    async def get_with_children(self, activity_id: int) -> list[ActivityDTO]:
        entities = await self.repo.get_with_children(activity_id)
        return [ActivityDTO.from_entity(e) for e in entities]

    async def get_by_level(self, level: int) -> list[ActivityDTO]:
        entities = await self.repo.get_by_level(level)
        return [ActivityDTO.from_entity(e) for e in entities]

    async def get_all_ids_with_children(self, activity_id: int) -> list[int]:
        entities = await self.repo.get_with_children(activity_id)
        return [e.id for e in entities]
