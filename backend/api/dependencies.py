"""
API dependencies.

Reusable FastAPI dependencies.

Author: Rajab Cheruiyot Bett
Project: AI Customer Support RAG Platform
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.security import decode_access_token
from backend.db.database import get_db
from backend.models.user import User
from backend.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)

user_repository = UserRepository()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Return the authenticated user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except Exception:
        raise credentials_exception

    user = await user_repository.get_by_email(
        db,
        email,
    )

    if user is None:
        raise credentials_exception

    return user