from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct
from src.domain.entities.organization import OrganizationEntity
from src.domain.repositories.organization_repo import OrganizationRepository
from src.infrastructure.models import Organization, OrganizationPhone, OrganizationActivity


class OrganizationRepositoryImpl(OrganizationRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, org_id: int) -> Optional[OrganizationEntity]:
        result = await self.session.execute(
            select(Organization).where(Organization.id == org_id)
        )
        org = result.scalar_one_or_none()
        if org is None:
            return None
        return await self._to_entity(org)

    async def get_all(self) -> list[OrganizationEntity]:
        result = await self.session.execute(select(Organization))
        organizations = result.scalars().all()
        return [await self._to_entity(org) for org in organizations]

    async def get_by_building_id(self, building_id: int) -> list[OrganizationEntity]:
        result = await self.session.execute(
            select(Organization).where(Organization.building_id == building_id)
        )
        organizations = result.scalars().all()
        return [await self._to_entity(org) for org in organizations]

    async def get_by_activity_id(self, activity_id: int) -> list[OrganizationEntity]:
        result = await self.session.execute(
            select(distinct(OrganizationActivity.organization_id)).where(
                OrganizationActivity.activity_id == activity_id
            )
        )
        org_ids = [row[0] for row in result.all()]
        
        result = await self.session.execute(
            select(Organization).where(Organization.id.in_(org_ids))
        )
        organizations = result.scalars().all()
        return [await self._to_entity(org) for org in organizations]

    async def get_by_activity_ids(self, activity_ids: list[int]) -> list[OrganizationEntity]:
        if not activity_ids:
            return []
        
        result = await self.session.execute(
            select(distinct(OrganizationActivity.organization_id)).where(
                OrganizationActivity.activity_id.in_(activity_ids)
            )
        )
        org_ids = [row[0] for row in result.all()]
        
        result = await self.session.execute(
            select(Organization).where(Organization.id.in_(org_ids))
        )
        organizations = result.scalars().all()
        return [await self._to_entity(org) for org in organizations]

    async def search_by_name(self, search_term: str) -> list[OrganizationEntity]:
        result = await self.session.execute(
            select(Organization).where(Organization.name.ilike(f"%{search_term}%"))
        )
        organizations = result.scalars().all()
        return [await self._to_entity(org) for org in organizations]

    async def get_in_radius(
        self,
        latitude: float,
        longitude: float,
        radius_m: float
    ) -> list[OrganizationEntity]:
        from src.infrastructure.repositories.building_repo import BuildingRepositoryImpl

        building_repo = BuildingRepositoryImpl(self.session)
        buildings = await building_repo.get_in_radius(latitude, longitude, radius_m)
        building_ids = [b.id for b in buildings]

        if not building_ids:
            return []

        result = await self.session.execute(
            select(Organization).where(Organization.building_id.in_(building_ids))
        )
        organizations = result.scalars().all()
        return [await self._to_entity(org) for org in organizations]

    async def get_in_box(
        self,
        center_lat: float,
        center_lon: float,
        radius_m: float
    ) -> list[OrganizationEntity]:
        from src.infrastructure.repositories.building_repo import BuildingRepositoryImpl

        building_repo = BuildingRepositoryImpl(self.session)
        buildings = await building_repo.get_in_box(center_lat, center_lon, radius_m)
        building_ids = [b.id for b in buildings]

        if not building_ids:
            return []

        result = await self.session.execute(
            select(Organization).where(Organization.building_id.in_(building_ids))
        )
        organizations = result.scalars().all()
        return [await self._to_entity(org) for org in organizations]

    async def _to_entity(self, org: Organization) -> OrganizationEntity:
        phones_result = await self.session.execute(
            select(OrganizationPhone.phone).where(OrganizationPhone.organization_id == org.id)
        )
        phones = [row[0] for row in phones_result.all()]
        
        activities_result = await self.session.execute(
            select(OrganizationActivity.activity_id).where(OrganizationActivity.organization_id == org.id)
        )
        activity_ids = [row[0] for row in activities_result.all()]
        
        return OrganizationEntity(
            id=org.id,
            name=org.name,
            building_id=org.building_id,
            phones=phones,
            activity_ids=activity_ids,
        )
