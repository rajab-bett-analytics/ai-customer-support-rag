from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_current_user
from backend.db.database import get_db
from backend.models.user import User
from backend.schemas.analytics import AnalyticsSummary
from backend.services.analytics_service import (
    AnalyticsService,
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)

service = AnalyticsService()

DatabaseSession = Annotated[
    AsyncSession,
    Depends(get_db),
]

CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]


@router.get(
    "",
    response_model=AnalyticsSummary,
)
async def get_analytics(
    db: DatabaseSession,
    current_user: CurrentUser,
) -> AnalyticsSummary:
    return await service.get_summary(
        db=db,
        user_id=current_user.id,
    )