from typing import Optional
from src.domain.repositories.organization_repo import OrganizationRepository
from src.domain.repositories.activity_repo import ActivityRepository
from src.domain.repositories.building_repo import BuildingRepository
from src.application.dto.organization import OrganizationDTO, OrganizationDetailDTO


class OrganizationService:

    def __init__(
        self,
        org_repo: OrganizationRepository,
        activity_repo: ActivityRepository,
        building_repo: BuildingRepository
    ):
        self.org_repo = org_repo
        self.activity_repo = activity_repo
        self.building_repo = building_repo

    async def get_by_id(self, org_id: int) -> Optional[OrganizationDetailDTO]:
        entity = await self.org_repo.get_by_id(org_id)
        if entity is None:
            return None

        building = await self.building_repo.get_by_id(entity.building_id)
        if building is None:
            return None

        activity_names = []
        for activity_id in entity.activity_ids:
            activity = await self.activity_repo.get_by_id(activity_id)
            if activity:
                activity_names.append(activity.name)

        return OrganizationDetailDTO.from_entity(
            entity,
            building_address=building.address,
            building_lat=float(building.latitude),
            building_lon=float(building.longitude),
            activity_names=activity_names,
        )

    async def get_all(self) -> list[OrganizationDTO]:
        entities = await self.org_repo.get_all()
        return [OrganizationDTO.from_entity(e) for e in entities]

    async def get_by_building_id(self, building_id: int) -> list[OrganizationDTO]:
        entities = await self.org_repo.get_by_building_id(building_id)
        return [OrganizationDTO.from_entity(e) for e in entities]

    async def get_by_activity_id(self, activity_id: int) -> list[OrganizationDTO]:
        entities = await self.org_repo.get_by_activity_id(activity_id)
        return [OrganizationDTO.from_entity(e) for e in entities]

    async def search_by_name(self, search_term: str) -> list[OrganizationDTO]:
        entities = await self.org_repo.search_by_name(search_term)
        return [OrganizationDTO.from_entity(e) for e in entities]

    async def get_in_radius(
        self,
        latitude: float,
        longitude: float,
        radius_m: float
    ) -> list[OrganizationDTO]:
        entities = await self.org_repo.get_in_radius(latitude, longitude, radius_m)
        return [OrganizationDTO.from_entity(e) for e in entities]

    async def get_in_box(
        self,
        center_lat: float,
        center_lon: float,
        radius_m: float
    ) -> list[OrganizationDTO]:
        entities = await self.org_repo.get_in_box(center_lat, center_lon, radius_m)
        return [OrganizationDTO.from_entity(e) for e in entities]
