"""
Authentication API routes.

This module exposes endpoints for user registration
and authentication.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.database import get_db
from backend.schemas.token import Token
from backend.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
)
from backend.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

auth_service = AuthService()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """
    Register a new user.
    """

    user = await auth_service.register_user(
        db,
        user_data,
    )

    return user


@router.post(
    "/login",
    response_model=Token,
)
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """
    Authenticate a user.
    """

    return await auth_service.login_user(
        db,
        user_data,
    )