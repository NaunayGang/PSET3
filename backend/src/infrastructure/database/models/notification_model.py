"""Notification ORM model."""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..base import Base


class NotificationModel(Base):
    """Notification database model."""

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    channel = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    event_type = Column(String(50), nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
