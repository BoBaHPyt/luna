from typing import Optional
from src.domain.repositories.building_repo import BuildingRepository
from src.application.dto.building import BuildingDTO


class BuildingService:

    def __init__(self, repo: BuildingRepository):
        self.repo = repo

    async def get_by_id(self, building_id: int) -> Optional[BuildingDTO]:
        entity = await self.repo.get_by_id(building_id)
        if entity is None:
            return None
        return BuildingDTO.from_entity(entity)

    async def get_all(self) -> list[BuildingDTO]:
        entities = await self.repo.get_all()
        return [BuildingDTO.from_entity(e) for e in entities]

    async def get_in_radius(
        self,
        latitude: float,
        longitude: float,
        radius_m: float
    ) -> list[BuildingDTO]:
        entities = await self.repo.get_in_radius(latitude, longitude, radius_m)
        return [BuildingDTO.from_entity(e) for e in entities]

    async def get_in_box(
        self,
        center_lat: float,
        center_lon: float,
        radius_m: float
    ) -> list[BuildingDTO]:
        entities = await self.repo.get_in_box(center_lat, center_lon, radius_m)
        return [BuildingDTO.from_entity(e) for e in entities]
