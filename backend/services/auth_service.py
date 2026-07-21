"""
Authentication service.

This module contains the business logic for user registration
and authentication.

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
from backend.schemas.user import UserCreate, UserLogin

# ---------------------------------------------------------
# Password Hasher
#
# Create a single password hasher instance that can be reused
# throughout the application.
# ---------------------------------------------------------

password_hash = PasswordHash.recommended()


class AuthService:
    """
    Handles user registration and authentication.
    """

    def __init__(self) -> None:
        self.user_repository = UserRepository()

    def hash_password(self, password: str) -> str:
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
        Verify a plain-text password against its hash.
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

        # Check whether the email already exists
        existing_user = await self.user_repository.get_by_email(
            db,
            user_data.email,
        )

        if existing_user is not None:
            raise ValueError("Email already registered.")

        # Hash the password
        hashed_password = self.hash_password(
            user_data.password,
        )

        # Create the user model
        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hashed_password,
            is_active=True,
        )

        # Save to the database
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
        Authenticate a user and generate an access token.
        """

        # Find the user by email
        user = await self.user_repository.get_by_email(
            db,
            user_data.email,
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        # Verify the password
        if not self.verify_password(
            user_data.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        # Generate a JWT access token
        access_token = create_access_token(
            subject=user.email,
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )