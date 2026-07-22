from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
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

    return await auth_service.register_user(
        db,
        user_data,
    )


@router.post(
    "/login",
    response_model=Token,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Token:
    """
    Authenticate a user.
    """

    user_data = UserLogin(
        email=form_data.username,
        password=form_data.password,
    )

    return await auth_service.login_user(
        db,
        user_data,
    )