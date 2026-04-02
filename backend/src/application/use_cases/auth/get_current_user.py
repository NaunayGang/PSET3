"""Get current user use case."""

from typing import Optional

from ....domain.entities.user import User
from ....domain.repositories.user_repository import UserRepository
from ....infrastructure.auth.jwt_handler import decode_access_token


class GetCurrentUserUseCase:
    """Use case for retrieving current authenticated user."""

    def __init__(self, user_repository: UserRepository):
        """
        Initialize get current user use case.

        Args:
            user_repository: User repository for data access
        """
        self.user_repository = user_repository

    def execute(self, token: str) -> Optional[User]:
        """
        Get current user from JWT token.

        Args:
            token: JWT access token

        Returns:
            User entity if token is valid, None otherwise
        """
        # Decode token
        payload = decode_access_token(token)
        if not payload:
            return None

        # Extract user ID
        user_id = payload.get("user_id")
        if not user_id:
            return None

        # Get user from repository
        user = self.user_repository.find_by_id(user_id)
        return user
