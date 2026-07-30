"""
Authentication service.

This module contains the business logic for user registration,
authentication, and user profile management.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from fastapi import HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.security import create_access_token
from backend.models.user import User
from backend.repositories.user_repository import UserRepository
from backend.schemas.token import Token
from backend.schemas.user import (
    UserCreate,
    UserLogin,
)

password_hash = PasswordHash.recommended()


class AuthService:
    """
    Handles authentication and user profile operations.
    """

    def __init__(self) -> None:
        self.user_repository = UserRepository()

    def hash_password(
        self,
        password: str,
    ) -> str:
        """
        Hash a plain-text password.
        """
        return password_hash.hash(password)

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """
        Verify a plain-text password.
        """
        return password_hash.verify(
            plain_password,
            hashed_password,
        )

    async def register_user(
        self,
        db: AsyncSession,
        user_data: UserCreate,
    ) -> User:
        """
        Register a new user.
        """

        existing_user = (
            await self.user_repository.get_by_email(
                db,
                user_data.email,
            )
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered.",
            )

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=self.hash_password(
                user_data.password,
            ),
            is_active=True,
        )

        return await self.user_repository.create(
            db,
            user,
        )

    async def login_user(
        self,
        db: AsyncSession,
        user_data: UserLogin,
    ) -> Token:
        """
        Authenticate a user.
        """

        user = (
            await self.user_repository.get_by_email(
                db,
                user_data.email,
            )
        )

        if (
            user is None
            or not self.verify_password(
                user_data.password,
                user.hashed_password,
            )
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        access_token = create_access_token(
            subject=user.email,
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )

    async def get_profile(
        self,
        current_user: User,
    ) -> User:
        """
        Return the authenticated user.
        """

        return current_user

    async def update_profile(
        self,
        db: AsyncSession,
        current_user: User,
        *,
        full_name: str,
        email: str,
    ) -> User:
        """
        Update the user's profile.
        """

        if email != current_user.email:

            existing = (
                await self.user_repository.get_by_email(
                    db,
                    email,
                )
            )

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered.",
                )

        current_user.full_name = full_name
        current_user.email = email

        return await self.user_repository.update(
            db,
            current_user,
        )

    async def change_password(
        self,
        db: AsyncSession,
        current_user: User,
        current_password: str,
        new_password: str,
    ) -> None:
        """
        Change the user's password.
        """

        if not self.verify_password(
            current_password,
            current_user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect.",
            )

        current_user.hashed_password = (
            self.hash_password(new_password)
        )

        await self.user_repository.update(
            db,
            current_user,
        )