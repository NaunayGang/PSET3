"""User DTOs."""

from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    """User response DTO."""

    id: int
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """User creation DTO."""

    name: str
    email: EmailStr
    password: str
    role: str
