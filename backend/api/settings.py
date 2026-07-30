"""
Settings API.

Provides endpoints for managing the authenticated
user's application settings.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_current_user
from backend.db.database import get_db
from backend.models.user import User
from backend.schemas.settings import (
    SettingsResponse,
    SettingsUpdate,
)
from backend.services.settings_service import (
    SettingsService,
)

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)

settings_service = SettingsService()

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
    response_model=SettingsResponse,
    summary="Get Settings",
    description="Retrieve the current user's settings.",
)
async def get_settings(
    db: DatabaseSession,
    current_user: CurrentUser,
) -> SettingsResponse:
    """
    Retrieve the authenticated user's settings.
    """

    return await settings_service.get_settings(
        db=db,
        user=current_user,
    )


@router.put(
    "",
    response_model=SettingsResponse,
    summary="Update Settings",
    description="Update the current user's settings.",
)
async def update_settings(
    settings_data: SettingsUpdate,
    db: DatabaseSession,
    current_user: CurrentUser,
) -> SettingsResponse:
    """
    Update the authenticated user's settings.
    """

    return await settings_service.update_settings(
        db=db,
        user=current_user,
        settings_data=settings_data,
    )