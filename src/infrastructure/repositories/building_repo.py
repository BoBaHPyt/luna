from typing import Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.entities.building import BuildingEntity
from src.domain.repositories.building_repo import BuildingRepository
from src.infrastructure.models import Building
import math


class BuildingRepositoryImpl(BuildingRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, building_id: int) -> Optional[BuildingEntity]:
        result = await self.session.execute(
            select(Building).where(Building.id == building_id)
        )
        building = result.scalar_one_or_none()
        if building is None:
            return None
        return BuildingEntity(
            id=building.id,
            address=building.address,
            latitude=Decimal(str(building.latitude)),
            longitude=Decimal(str(building.longitude)),
        )

    async def get_all(self) -> list[BuildingEntity]:
        result = await self.session.execute(select(Building))
        buildings = result.scalars().all()
        return [
            BuildingEntity(
                id=b.id,
                address=b.address,
                latitude=Decimal(str(b.latitude)),
                longitude=Decimal(str(b.longitude)),
            )
            for b in buildings
        ]

    async def get_in_radius(
        self,
        latitude: float,
        longitude: float,
        radius_m: float
    ) -> list[BuildingEntity]:
        """
        TODO: Оптимизация: полная фильтрация на стороне базы
        """
        buildings = await self._get_buildings_in_box_sql(latitude, longitude, radius_m)
        
        result = []
        for b in buildings:
            lat1, lon1 = float(b.latitude), float(b.longitude)
            distance = self._haversine_distance(latitude, longitude, lat1, lon1)
            if distance <= radius_m:
                result.append(BuildingEntity(
                    id=b.id,
                    address=b.address,
                    latitude=Decimal(str(b.latitude)),
                    longitude=Decimal(str(b.longitude)),
                ))

        return result

    async def _get_buildings_in_box_sql(
        self,
        center_lat: float,
        center_lon: float,
        radius_m: float
    ) -> list[Building]:
        """Быстрый SQL-запрос для получения зданий в bounding box"""
        lat_deg = radius_m / 111320.0
        lon_deg = radius_m / (111320.0 * abs(math.cos(center_lat * math.pi / 180))) if center_lat != 0 else radius_m / 111320.0

        min_lat = center_lat - lat_deg
        max_lat = center_lat + lat_deg
        min_lon = center_lon - lon_deg
        max_lon = center_lon + lon_deg

        result = await self.session.execute(
            select(Building).where(
                Building.latitude >= min_lat,
                Building.latitude <= max_lat,
                Building.longitude >= min_lon,
                Building.longitude <= max_lon,
            )
        )
        return result.scalars().all()

    async def get_in_box(
        self,
        center_lat: float,
        center_lon: float,
        radius_m: float
    ) -> list[BuildingEntity]:
        buildings = await self._get_buildings_in_box_sql(center_lat, center_lon, radius_m)

        return [
            BuildingEntity(
                id=b.id,
                address=b.address,
                latitude=Decimal(str(b.latitude)),
                longitude=Decimal(str(b.longitude)),
            )
            for b in buildings
        ]

    @staticmethod
    def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Вычисляет расстояние между двумя точками в метрах (формула гаверсинуса)"""
        R = 6371000.0

        lat1_rad = lat1 * math.pi / 180
        lat2_rad = lat2 * math.pi / 180
        delta_lat = (lat2 - lat1) * math.pi / 180
        delta_lon = (lon2 - lon1) * math.pi / 180

        a = math.sin(delta_lat / 2) ** 2 + \
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c
