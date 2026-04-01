"""Domain value objects."""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """Email value object with validation."""

    value: str

    def __post_init__(self):
        """Validate email format."""
        if not self.value or "@" not in self.value:
            raise ValueError(f"Invalid email address: {self.value}")

        # Basic email validation pattern
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, self.value):
            raise ValueError(f"Invalid email format: {self.value}")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class UserId:
    """User ID value object."""

    value: int

    def __post_init__(self):
        """Validate user ID."""
        if not isinstance(self.value, int) or self.value <= 0:
            raise ValueError(f"Invalid user ID: {self.value}")

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class IncidentId:
    """Incident ID value object."""

    value: int

    def __post_init__(self):
        """Validate incident ID."""
        if not isinstance(self.value, int) or self.value <= 0:
            raise ValueError(f"Invalid incident ID: {self.value}")

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class TaskId:
    """Task ID value object."""

    value: int

    def __post_init__(self):
        """Validate task ID."""
        if not isinstance(self.value, int) or self.value <= 0:
            raise ValueError(f"Invalid task ID: {self.value}")

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)
