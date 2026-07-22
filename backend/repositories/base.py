from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing reusable CRUD operations.

    Specific repositories (UserRepository, DocumentRepository, etc.)
    inherit from this class.
    """

    def __init__(self, model: type[ModelType]):
        self.model = model

    async def create(
        self,
        db: AsyncSession,
        obj: ModelType,
    ) -> ModelType:
        """
        Persist a new database object.
        """
        try:
            db.add(obj)
            await db.commit()
            await db.refresh(obj)
            return obj
        except Exception:
            await db.rollback()
            raise

    async def get_by_id(
        self,
        db: AsyncSession,
        obj_id: int,
    ) -> ModelType | None:
        """
        Retrieve an object by its primary key.
        """
        result = await db.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        db: AsyncSession,
    ) -> list[ModelType]:
        """
        Retrieve all objects.
        """
        result = await db.execute(select(self.model))
        return list(result.scalars().all())

    async def update(
        self,
        db: AsyncSession,
        obj: ModelType,
    ) -> ModelType:
        """
        Persist changes to an existing object.
        """
        try:
            await db.commit()
            await db.refresh(obj)
            return obj
        except Exception:
            await db.rollback()
            raise

    async def delete(
        self,
        db: AsyncSession,
        obj: ModelType,
    ) -> None:
        """
        Delete an object.
        """
        try:
            await db.delete(obj)
            await db.commit()
        except Exception:
            await db.rollback()
            raise