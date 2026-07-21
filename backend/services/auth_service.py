from sqlalchemy.ext.asyncio import AsyncSession
from pwdlib import PasswordHash

from backend.models.user import User
from backend.repositories.user_repository import UserRepository
from backend.schemas.user import UserCreate


password_hash = PasswordHash.recommended()


class AuthService:
    """
    Handles authentication and user management business logic.
    """

    def __init__(self):
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

        # Check if the email is already registered
        existing_user = await self.user_repository.get_by_email(
            db,
            user_data.email,
        )

        if existing_user is not None:
            raise ValueError("Email already registered.")

        # Hash the user's password
        hashed_password = self.hash_password(
            user_data.password,
        )

        # Create a new User object
        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hashed_password,
            is_active=True,
        )

        # Save the user
        return await self.user_repository.create(
            db,
            user,
        )