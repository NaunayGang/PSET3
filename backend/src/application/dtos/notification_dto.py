"""Notification DTOs."""

from datetime import datetime
from pydantic import BaseModel

from ...domain.enums.event_type import EventType
from ...domain.enums.notification_channel import NotificationChannel
from ...domain.enums.notification_status import NotificationStatus


class NotificationStatusUpdate(BaseModel):
    """Update notification status request DTO."""

    status: NotificationStatus


class NotificationResponse(BaseModel):
    """Notification response DTO."""

    id: int
    recipient_id: int
    channel: NotificationChannel
    message: str
    event_type: EventType
    status: NotificationStatus
    created_at: datetime

    class Config:
        from_attributes = True
