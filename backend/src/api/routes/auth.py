"""Authentication routes."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ...application.dtos.auth_dto import LoginResponse
from ...application.dtos.user_dto import UserResponse
from ...application.use_cases.auth.login import LoginUseCase
from ...domain.repositories.user_repository import UserRepository
from ..dependencies import get_user_repository, get_current_user
from ...domain.entities.user import User

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    """
    Authenticate user and return access token.

    Args:
        form_data: OAuth2 form with username (email) and password
        user_repository: User repository dependency

    Returns:
        LoginResponse with access token

    Raises:
        HTTPException: If credentials are invalid
    """
    from ...application.dtos.auth_dto import LoginRequest

    # OAuth2PasswordRequestForm uses 'username' field, but we use email
    request = LoginRequest(email=form_data.username, password=form_data.password)

    use_case = LoginUseCase(user_repository)
    response = use_case.execute(request)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return response


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Get current authenticated user information.

    Args:
        current_user: Current user from JWT token

    Returns:
        User information
    """
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role.value,
        created_at=current_user.created_at,
    )
