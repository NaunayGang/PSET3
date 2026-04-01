"""Incident status enumeration."""

from enum import Enum


class IncidentStatus(str, Enum):
    """Incident lifecycle statuses."""

    OPEN = "OPEN"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

    def __str__(self) -> str:
        return self.value
