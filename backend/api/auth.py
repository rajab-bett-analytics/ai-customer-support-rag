"""
Authentication API.

Provides endpoints for user registration, authentication,
retrieval of the currently authenticated user's profile,
and password management.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_current_user
from backend.db.database import get_db
from backend.models.user import User
from backend.schemas.token import Token
from backend.schemas.user import (
    PasswordChange,
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

DatabaseSession = Annotated[
    AsyncSession,
    Depends(get_db),
]

CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register",
    description="Create a new user account.",
)
async def register(
    user_data: UserCreate,
    db: DatabaseSession,
) -> UserResponse:
    """
    Register a new user.
    """

    return await auth_service.register_user(
        db=db,
        user_data=user_data,
    )


@router.post(
    "/login",
    response_model=Token,
    summary="Login",
    description="Authenticate a user and return an access token.",
)
async def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    db: DatabaseSession,
) -> Token:
    """
    Authenticate a user.
    """

    user_data = UserLogin(
        email=form_data.username,
        password=form_data.password,
    )

    return await auth_service.login_user(
        db=db,
        user_data=user_data,
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get Profile",
    description="Return the authenticated user's profile.",
)
async def get_profile(
    current_user: CurrentUser,
) -> UserResponse:
    """
    Retrieve the authenticated user's profile.
    """

    return await auth_service.get_profile(
        current_user,
    )


@router.patch(
    "/change-password",
    status_code=status.HTTP_200_OK,
    summary="Change Password",
    description="Change the authenticated user's password.",
)
async def change_password(
    password_data: PasswordChange,
    db: DatabaseSession,
    current_user: CurrentUser,
) -> dict[str, str]:
    """
    Change the authenticated user's password.
    """

    await auth_service.change_password(
        db=db,
        current_user=current_user,
        current_password=password_data.current_password,
        new_password=password_data.new_password,
    )

    return {
        "message": "Password updated successfully."
    }