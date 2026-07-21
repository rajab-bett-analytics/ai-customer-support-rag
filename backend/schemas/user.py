from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """
    Schema for user registration.
    """

    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """
    Schema for user login.
    """

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Schema returned to clients.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime