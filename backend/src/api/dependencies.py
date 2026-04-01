"""FastAPI dependencies."""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..domain.entities.user import User
from ..domain.enums.role import Role
from ..domain.repositories.user_repository import UserRepository
from ..domain.repositories.incident_repository import IncidentRepository
from ..infrastructure.database.connection import get_db
from ..infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from ..infrastructure.repositories.sqlalchemy_incident_repository import SQLAlchemyIncidentRepository
from ..application.use_cases.auth.get_current_user import GetCurrentUserUseCase

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """
    Dependency for getting user repository.

    Args:
        db: Database session

    Returns:
        User repository instance
    """
    return SQLAlchemyUserRepository(db)


def get_incident_repository(db: Session = Depends(get_db)) -> IncidentRepository:
    """
    Dependency for getting incident repository.

    Args:
        db: Database session

    Returns:
        Incident repository instance
    """
    return SQLAlchemyIncidentRepository(db)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    """
    Dependency for getting current authenticated user.

    Args:
        token: JWT access token
        user_repository: User repository

    Returns:
        Current user entity

    Raises:
        HTTPException: If token is invalid or user not found
    """
    use_case = GetCurrentUserUseCase(user_repository)
    user = use_case.execute(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def require_role(*allowed_roles: Role):
    """
    Dependency factory for role-based access control.

    Args:
        allowed_roles: Roles that are allowed to access the endpoint

    Returns:
        Dependency function that validates user role
    """

    async def role_checker(current_user: Annotated[User, Depends(get_current_user)]) -> User:
        """
        Check if current user has required role.

        Args:
            current_user: Current authenticated user

        Returns:
            Current user if authorized

        Raises:
            HTTPException: If user doesn't have required role
        """
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {[r.value for r in allowed_roles]}",
            )
        return current_user

    return role_checker
