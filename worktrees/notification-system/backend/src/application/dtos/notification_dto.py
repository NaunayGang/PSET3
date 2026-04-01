"""Notification DTOs."""

from pydantic import BaseModel
from datetime import datetime
from ...domain.enums.notification_channel import NotificationChannel
from ...domain.enums.notification_status import NotificationStatus
from ...domain.enums.event_type import EventType


class NotificationCreate(BaseModel):
    recipient_id: int
    channel: NotificationChannel
    message: str
    event_type: EventType


class NotificationUpdate(BaseModel):
    status: NotificationStatus | None = None


class NotificationResponse(BaseModel):
    id: int
    recipient_id: int
    channel: NotificationChannel
    message: str
    event_type: EventType
    status: NotificationStatus
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationStatusUpdate(BaseModel):
    status: NotificationStatus
