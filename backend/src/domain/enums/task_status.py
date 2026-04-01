"""Task status enumeration."""

from enum import Enum


class TaskStatus(str, Enum):
    """Task lifecycle statuses."""

    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

    def __str__(self) -> str:
        return self.value
