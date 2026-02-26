from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.building import BuildingEntity


class BuildingRepository(ABC):

    @abstractmethod
    async def get_by_id(self, building_id: int) -> Optional[BuildingEntity]:
        """Получить здание по ID"""
        pass

    @abstractmethod
    async def get_all(self) -> list[BuildingEntity]:
        """Получить все здания"""
        pass

    @abstractmethod
    async def get_in_radius(
        self,
        latitude: float,
        longitude: float,
        radius_m: float
    ) -> list[BuildingEntity]:
        """Получить здания в радиусе от точки (радиус в метрах)"""
        pass

    @abstractmethod
    async def get_in_box(
        self,
        center_lat: float,
        center_lon: float,
        radius_m: float
    ) -> list[BuildingEntity]:
        """Получить здания в квадратной области (центр + радиус в метрах)"""
        pass
