"""Login use case."""

from typing import Optional

from ...dtos.auth_dto import LoginRequest, LoginResponse
from ....domain.repositories.user_repository import UserRepository
from ....infrastructure.auth.password_handler import verify_password
from ....infrastructure.auth.jwt_handler import create_access_token


class LoginUseCase:
    """Use case for user authentication."""

    def __init__(self, user_repository: UserRepository):
        """
        Initialize login use case.

        Args:
            user_repository: User repository for data access
        """
        self.user_repository = user_repository

    def execute(self, request: LoginRequest) -> Optional[LoginResponse]:
        """
        Authenticate user and generate access token.

        Args:
            request: Login request with email and password

        Returns:
            LoginResponse with access token if successful, None otherwise
        """
        # Find user by email
        user = self.user_repository.find_by_email(request.email)
        if not user:
            return None

        # Verify password
        if not verify_password(request.password, user.hashed_password):
            return None

        # Create access token
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role.value,
        }
        access_token = create_access_token(token_data)

        # Return response
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            name=user.name,
            email=user.email,
            role=user.role.value,
        )
