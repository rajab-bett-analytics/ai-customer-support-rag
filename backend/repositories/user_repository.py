from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.user import User
from backend.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for User-specific database operations.
    """

    def __init__(self):
        super().__init__(User)

    async def get_by_email(
        self,
        db: AsyncSession,
        email: str,
    ) -> User | None:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def email_exists(
        self,
        db: AsyncSession,
        email: str,
    ) -> bool:
        return await self.get_by_email(db, email) is not None