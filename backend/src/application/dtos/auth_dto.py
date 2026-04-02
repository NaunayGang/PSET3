"""Authentication DTOs."""

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Login request DTO."""

    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response DTO."""

    access_token: str
    token_type: str = "bearer"
    user_id: int
    name: str
    email: str
    role: str


class TokenData(BaseModel):
    """JWT token payload DTO."""

    user_id: int
    email: str
    role: str
