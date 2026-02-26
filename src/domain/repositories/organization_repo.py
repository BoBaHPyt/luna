from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.organization import OrganizationEntity


class OrganizationRepository(ABC):

    @abstractmethod
    async def get_by_id(self, org_id: int) -> Optional[OrganizationEntity]:
        """Получить организацию по ID"""
        pass

    @abstractmethod
    async def get_all(self) -> list[OrganizationEntity]:
        """Получить все организации"""
        pass

    @abstractmethod
    async def get_by_building_id(self, building_id: int) -> list[OrganizationEntity]:
        """Получить все организации в здании"""
        pass

    @abstractmethod
    async def get_by_activity_id(self, activity_id: int) -> list[OrganizationEntity]:
        """Получить организации по виду деятельности (включая вложенные)"""
        pass

    @abstractmethod
    async def get_by_activity_ids(
        self,
        activity_ids: list[int]
    ) -> list[OrganizationEntity]:
        """Получить организации по списку activity_id"""
        pass

    @abstractmethod
    async def search_by_name(self, search_term: str) -> list[OrganizationEntity]:
        """Поиск организации по названию (частичное совпадение)"""
        pass

    @abstractmethod
    async def get_in_radius(
        self,
        latitude: float,
        longitude: float,
        radius_m: float
    ) -> list[OrganizationEntity]:
        """Получить организации в радиусе от точки (через здание)"""
        pass

    @abstractmethod
    async def get_in_box(
        self,
        center_lat: float,
        center_lon: float,
        radius_m: float
    ) -> list[OrganizationEntity]:
        """Получить организации в квадратной области (через здание)"""
        pass
