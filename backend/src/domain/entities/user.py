"""User domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..enums.role import Role


@dataclass
class User:
    """User entity representing a system user."""

    id: Optional[int]
    name: str
    email: str
    role: Role
    hashed_password: str
    created_at: datetime

    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == Role.ADMIN

    def is_supervisor(self) -> bool:
        """Check if user has supervisor role."""
        return self.role == Role.SUPERVISOR

    def is_operator(self) -> bool:
        """Check if user has operator role."""
        return self.role == Role.OPERATOR

    def can_assign_incidents(self) -> bool:
        """Check if user can assign incidents to others."""
        return self.role in [Role.ADMIN, Role.SUPERVISOR]

    def can_manage_users(self) -> bool:
        """Check if user can manage other users."""
        return self.role == Role.ADMIN
