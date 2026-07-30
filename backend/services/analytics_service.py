from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.analytics_repository import (
    AnalyticsRepository,
)
from backend.schemas.analytics import AnalyticsSummary


class AnalyticsService:
    def __init__(self) -> None:
        self.repository = AnalyticsRepository()

    async def get_summary(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> AnalyticsSummary:
        data = await self.repository.get_summary(
            db=db,
            user_id=user_id,
        )

        return AnalyticsSummary(**data)