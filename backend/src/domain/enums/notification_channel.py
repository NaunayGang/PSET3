"""Notification channel enumeration."""

from enum import Enum


class NotificationChannel(str, Enum):
    """Notification delivery channels."""

    EMAIL = "EMAIL"
    SLACK = "SLACK"

    def __str__(self) -> str:
        return self.value
