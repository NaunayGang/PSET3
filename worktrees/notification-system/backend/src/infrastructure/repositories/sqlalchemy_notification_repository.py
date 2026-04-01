"""SQLAlchemy implementation of NotificationRepository."""

from typing import List, Optional
from sqlalchemy.orm import Session

from ...domain.entities.notification import Notification
from ...domain.enums.notification_status import NotificationStatus
from ...domain.repositories.notification_repository import NotificationRepository
from ..database.models.notification_model import NotificationModel


class SQLAlchemyNotificationRepository(NotificationRepository):
    """SQLAlchemy implementation of notification repository."""

    def __init__(self, session: Session):
        """
        Initialize repository with database session.

        Args:
            session: SQLAlchemy session
        """
        self.session = session

    def _to_entity(self, model: NotificationModel) -> Notification:
        """
        Convert ORM model to domain entity.

        Args:
            model: NotificationModel ORM instance

        Returns:
            Notification domain entity
        """
        return Notification(
            id=model.id,
            recipient_id=model.recipient_id,
            channel=model.channel,
            message=model.message,
            event_type=model.event_type,
            status=NotificationStatus(model.status),
            created_at=model.created_at,
        )

    def _to_model(self, entity: Notification) -> NotificationModel:
        """
        Convert domain entity to ORM model.

        Args:
            entity: Notification domain entity

        Returns:
            NotificationModel ORM instance
        """
        return NotificationModel(
            id=entity.id,
            recipient_id=entity.recipient_id,
            channel=entity.channel.value,
            message=entity.message,
            event_type=entity.event_type.value,
            status=entity.status.value,
            created_at=entity.created_at,
        )

    def find_by_id(self, notification_id: int) -> Optional[Notification]:
        """Find notification by ID."""
        model = self.session.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
        return self._to_entity(model) if model else None

    def save(self, notification: Notification) -> Notification:
        """Save notification (create or update)."""
        if notification.id:
            # Update existing
            model = self.session.query(NotificationModel).filter(NotificationModel.id == notification.id).first()
            if model:
                model.recipient_id = notification.recipient_id
                model.channel = notification.channel.value
                model.message = notification.message
                model.event_type = notification.event_type.value
                model.status = notification.status.value
            else:
                raise ValueError(f"Notification with ID {notification.id} not found")
        else:
            # Create new
            model = self._to_model(notification)
            self.session.add(model)

        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def list_by_recipient(self, user_id: int) -> List[Notification]:
        """List notifications for a specific recipient."""
        models = (
            self.session.query(NotificationModel)
            .filter(NotificationModel.recipient_id == user_id)
            .order_by(NotificationModel.created_at.desc())
            .all()
        )
        return [self._to_entity(m) for m in models]

    def list_by_status(self, status: NotificationStatus) -> List[Notification]:
        """List notifications by status."""
        models = (
            self.session.query(NotificationModel)
            .filter(NotificationModel.status == status.value)
            .order_by(NotificationModel.created_at.desc())
            .all()
        )
        return [self._to_entity(m) for m in models]

    def update_status(self, notification_id: int, status: NotificationStatus) -> Optional[Notification]:
        """Update notification status."""
        model = self.session.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
        if model:
            model.status = status.value
            self.session.commit()
            self.session.refresh(model)
            return self._to_entity(model)
        return None

    def delete(self, notification_id: int) -> bool:
        """Delete notification by ID."""
        model = self.session.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False
