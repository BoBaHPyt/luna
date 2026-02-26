from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_session
from src.infrastructure.repositories.building_repo import BuildingRepositoryImpl
from src.application.services.building_service import BuildingService
from src.schemas.building import BuildingResponse, BuildingListResponse

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.get("", response_model=BuildingListResponse)
async def get_all_buildings(
    db: AsyncSession = Depends(get_session),
):
    """Получить список всех зданий"""
    repo = BuildingRepositoryImpl(db)
    service = BuildingService(repo)
    buildings = await service.get_all()
    return {"buildings": buildings}


@router.get("/{building_id}", response_model=BuildingResponse)
async def get_building(
    building_id: int,
    db: AsyncSession = Depends(get_session),
):
    """Получить информацию о здании по ID"""
    repo = BuildingRepositoryImpl(db)
    service = BuildingService(repo)
    building = await service.get_by_id(building_id)
    if building is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Building not found")
    return building


@router.get("/search/radius", response_model=BuildingListResponse)
async def get_buildings_in_radius(
    lat: float = Query(..., description="Широта центра"),
    lon: float = Query(..., description="Долгота центра"),
    radius: float = Query(..., description="Радиус в метрах"),
    db: AsyncSession = Depends(get_session),
):
    """Получить здания в радиусе от точки"""
    repo = BuildingRepositoryImpl(db)
    service = BuildingService(repo)
    buildings = await service.get_in_radius(lat, lon, radius)
    return {"buildings": buildings}


@router.get("/search/box", response_model=BuildingListResponse)
async def get_buildings_in_box(
    lat: float = Query(..., description="Широта центра"),
    lon: float = Query(..., description="Долгота центра"),
    radius: float = Query(..., description="Радиус в метрах (полусторона квадрата)"),
    db: AsyncSession = Depends(get_session),
):
    """Получить здания в квадратной области (центр + радиус в метрах)"""
    repo = BuildingRepositoryImpl(db)
    service = BuildingService(repo)
    buildings = await service.get_in_box(lat, lon, radius)
    return {"buildings": buildings}
