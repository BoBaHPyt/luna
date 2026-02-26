from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_session
from src.infrastructure.repositories.organization_repo import OrganizationRepositoryImpl
from src.infrastructure.repositories.activity_repo import ActivityRepositoryImpl
from src.infrastructure.repositories.building_repo import BuildingRepositoryImpl
from src.application.services.organization_service import OrganizationService
from src.application.services.activity_service import ActivityService
from src.schemas.organization import (
    OrganizationResponse,
    OrganizationDetailResponse,
    OrganizationListResponse,
    OrganizationSearchResponse,
)

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get("", response_model=OrganizationListResponse)
async def get_all_organizations(
    db: AsyncSession = Depends(get_session),
):
    """Получить список всех организаций"""
    org_repo = OrganizationRepositoryImpl(db)
    activity_repo = ActivityRepositoryImpl(db)
    building_repo = BuildingRepositoryImpl(db)
    service = OrganizationService(org_repo, activity_repo, building_repo)
    organizations = await service.get_all()
    return {"organizations": organizations}


@router.get("/{org_id}", response_model=OrganizationDetailResponse)
async def get_organization(
    org_id: int,
    db: AsyncSession = Depends(get_session),
):
    """Получить полную информацию об организации по ID"""
    org_repo = OrganizationRepositoryImpl(db)
    activity_repo = ActivityRepositoryImpl(db)
    building_repo = BuildingRepositoryImpl(db)
    service = OrganizationService(org_repo, activity_repo, building_repo)
    organization = await service.get_by_id(org_id)
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@router.get("/building/{building_id}", response_model=OrganizationListResponse)
async def get_organizations_by_building(
    building_id: int,
    db: AsyncSession = Depends(get_session),
):
    """Получить все организации в здании"""
    org_repo = OrganizationRepositoryImpl(db)
    activity_repo = ActivityRepositoryImpl(db)
    building_repo = BuildingRepositoryImpl(db)
    service = OrganizationService(org_repo, activity_repo, building_repo)
    organizations = await service.get_by_building_id(building_id)
    return {"organizations": organizations}


@router.get("/activity/{activity_id}", response_model=OrganizationListResponse)
async def get_organizations_by_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_session),
):
    """Получить организации по виду деятельности (включая вложенные)"""
    org_repo = OrganizationRepositoryImpl(db)
    activity_repo = ActivityRepositoryImpl(db)
    building_repo = BuildingRepositoryImpl(db)
    service = OrganizationService(org_repo, activity_repo, building_repo)
    organizations = await service.get_by_activity_id(activity_id)
    return {"organizations": organizations}


@router.get("/search/name", response_model=OrganizationListResponse)
async def search_organizations_by_name(
    q: str = Query(..., min_length=1, description="Поисковый запрос"),
    db: AsyncSession = Depends(get_session),
):
    """Поиск организаций по названию (частичное совпадение)"""
    org_repo = OrganizationRepositoryImpl(db)
    activity_repo = ActivityRepositoryImpl(db)
    building_repo = BuildingRepositoryImpl(db)
    service = OrganizationService(org_repo, activity_repo, building_repo)
    organizations = await service.search_by_name(q)
    return {"organizations": organizations}


@router.get("/search/radius", response_model=OrganizationListResponse)
async def get_organizations_in_radius(
    lat: float = Query(..., description="Широта центра"),
    lon: float = Query(..., description="Долгота центра"),
    radius: float = Query(..., description="Радиус в метрах"),
    db: AsyncSession = Depends(get_session),
):
    """Получить организации в радиусе от точки"""
    org_repo = OrganizationRepositoryImpl(db)
    activity_repo = ActivityRepositoryImpl(db)
    building_repo = BuildingRepositoryImpl(db)
    service = OrganizationService(org_repo, activity_repo, building_repo)
    organizations = await service.get_in_radius(lat, lon, radius)
    return {"organizations": organizations}


@router.get("/search/box", response_model=OrganizationListResponse)
async def get_organizations_in_box(
    lat: float = Query(..., description="Широта центра"),
    lon: float = Query(..., description="Долгота центра"),
    radius: float = Query(..., description="Радиус в метрах (полусторона квадрата)"),
    db: AsyncSession = Depends(get_session),
):
    """Получить организации в квадратной области (центр + радиус в метрах)"""
    org_repo = OrganizationRepositoryImpl(db)
    activity_repo = ActivityRepositoryImpl(db)
    building_repo = BuildingRepositoryImpl(db)
    service = OrganizationService(org_repo, activity_repo, building_repo)
    organizations = await service.get_in_box(lat, lon, radius)
    return {"organizations": organizations}
