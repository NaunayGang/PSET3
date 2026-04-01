"""Incident severity enumeration."""

from enum import Enum


class IncidentSeverity(str, Enum):
    """Incident severity levels."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    def __str__(self) -> str:
        return self.value
