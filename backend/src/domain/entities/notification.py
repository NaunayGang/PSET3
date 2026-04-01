"""Notification domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..enums.event_type import EventType
from ..enums.notification_channel import NotificationChannel
from ..enums.notification_status import NotificationStatus


@dataclass
class Notification:
    """Notification entity representing a user notification."""

    id: Optional[int]
    recipient_id: int
    channel: NotificationChannel
    message: str
    event_type: EventType
    status: NotificationStatus
    created_at: datetime

    def is_pending(self) -> bool:
        """Check if notification is pending delivery."""
        return self.status == NotificationStatus.PENDING

    def is_sent(self) -> bool:
        """Check if notification was sent successfully."""
        return self.status == NotificationStatus.SENT

    def is_failed(self) -> bool:
        """Check if notification delivery failed."""
        return self.status == NotificationStatus.FAILED

    def mark_as_sent(self) -> None:
        """Mark notification as sent."""
        self.status = NotificationStatus.SENT

    def mark_as_failed(self) -> None:
        """Mark notification as failed."""
        self.status = NotificationStatus.FAILED
