from fastapi import APIRouter, Depends, Query, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_session
from src.infrastructure.repositories.activity_repo import ActivityRepositoryImpl
from src.application.services.activity_service import ActivityService
from src.schemas.activity import ActivityResponse, ActivityListResponse, ActivityTreeResponse

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("", response_model=ActivityListResponse)
async def get_all_activities(
    db: AsyncSession = Depends(get_session),
):
    """Получить список всех деятельностей"""
    repo = ActivityRepositoryImpl(db)
    service = ActivityService(repo)
    activities = await service.get_all()
    return {"activities": activities}


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_session),
):
    """Получить информацию о деятельности по ID"""
    repo = ActivityRepositoryImpl(db)
    service = ActivityService(repo)
    activity = await service.get_by_id(activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.get("/search/name", response_model=ActivityResponse)
async def get_activity_by_name(
    name: str = Query(..., description="Название деятельности"),
    db: AsyncSession = Depends(get_session),
):
    """Получить деятельность по названию (точное совпадение)"""
    repo = ActivityRepositoryImpl(db)
    service = ActivityService(repo)
    activity = await service.get_by_name(name)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.get("/level/{level}", response_model=ActivityListResponse)
async def get_activities_by_level(
    level: int = Path(..., ge=1, le=3, description="Уровень вложенности (1-3)"),
    db: AsyncSession = Depends(get_session),
):
    """Получить все деятельности указанного уровня"""
    repo = ActivityRepositoryImpl(db)
    service = ActivityService(repo)
    activities = await service.get_by_level(level)
    return {"activities": activities}
