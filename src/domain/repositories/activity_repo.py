from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.activity import ActivityEntity


class ActivityRepository(ABC):

    @abstractmethod
    async def get_by_id(self, activity_id: int) -> Optional[ActivityEntity]:
        """Получить деятельность по ID"""
        pass

    @abstractmethod
    async def get_all(self) -> list[ActivityEntity]:
        """Получить все деятельности"""
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[ActivityEntity]:
        """Получить деятельность по названию (точное совпадение)"""
        pass

    @abstractmethod
    async def get_with_children(self, activity_id: int) -> list[ActivityEntity]:
        """Получить деятельность и все вложенные (рекурсивно)"""
        pass

    @abstractmethod
    async def get_by_level(self, level: int) -> list[ActivityEntity]:
        """Получить все деятельности указанного уровня"""
        pass
