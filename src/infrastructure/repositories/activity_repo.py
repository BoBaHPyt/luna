from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.entities.activity import ActivityEntity
from src.domain.repositories.activity_repo import ActivityRepository
from src.infrastructure.models import Activity


class ActivityRepositoryImpl(ActivityRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, activity_id: int) -> Optional[ActivityEntity]:
        result = await self.session.execute(
            select(Activity).where(Activity.id == activity_id)
        )
        activity = result.scalar_one_or_none()
        if activity is None:
            return None
        return ActivityEntity(
            id=activity.id,
            name=activity.name,
            level=activity.level,
            parent_id=activity.parent_id,
        )

    async def get_all(self) -> list[ActivityEntity]:
        result = await self.session.execute(select(Activity))
        activities = result.scalars().all()
        return [
            ActivityEntity(
                id=a.id,
                name=a.name,
                level=a.level,
                parent_id=a.parent_id,
            )
            for a in activities
        ]

    async def get_by_name(self, name: str) -> Optional[ActivityEntity]:
        result = await self.session.execute(
            select(Activity).where(Activity.name == name)
        )
        activity = result.scalar_one_or_none()
        if activity is None:
            return None
        return ActivityEntity(
            id=activity.id,
            name=activity.name,
            level=activity.level,
            parent_id=activity.parent_id,
        )

    async def get_with_children(self, activity_id: int) -> list[ActivityEntity]:
        """Рекурсивно получает деятельность и все вложенные"""
        result = []
        await self._collect_children(activity_id, result)
        return result

    async def get_by_level(self, level: int) -> list[ActivityEntity]:
        result = await self.session.execute(
            select(Activity).where(Activity.level == level)
        )
        activities = result.scalars().all()
        return [
            ActivityEntity(
                id=a.id,
                name=a.name,
                level=a.level,
                parent_id=a.parent_id,
            )
            for a in activities
        ]

    async def _collect_children(self, parent_id: int, result: list):
        """Рекурсивный сбор всех дочерних элементов"""
        stmt = select(Activity).where(Activity.parent_id == parent_id)
        result_query = await self.session.execute(stmt)
        children = result_query.scalars().all()
        
        for child in children:
            entity = ActivityEntity(
                id=child.id,
                name=child.name,
                level=child.level,
                parent_id=child.parent_id,
            )
            result.append(entity)
            await self._collect_children(child.id, result)
