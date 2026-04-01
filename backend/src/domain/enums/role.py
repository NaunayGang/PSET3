"""User role enumeration."""

from enum import Enum


class Role(str, Enum):
    """User roles in the system."""

    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"
    OPERATOR = "OPERATOR"

    def __str__(self) -> str:
        return self.value
