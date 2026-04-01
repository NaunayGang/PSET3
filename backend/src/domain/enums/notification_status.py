"""Notification status enumeration."""

from enum import Enum


class NotificationStatus(str, Enum):
    """Notification delivery statuses."""

    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"

    def __str__(self) -> str:
        return self.value
