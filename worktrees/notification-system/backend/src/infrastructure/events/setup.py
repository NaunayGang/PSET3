"""Event system initialization.

This module sets up the event bus with all observers on application startup.
"""

from ...domain.patterns.observer import Observer
from .event_bus import EventBus
from ...infrastructure.notifications.email_sender import EmailNotificationCommand
from ...infrastructure.notifications.slack_sender import SlackNotificationCommand
from ...domain.patterns.factory import CommandFactory
from ...infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from ...infrastructure.repositories.sqlalchemy_notification_repository import SQLAlchemyNotificationRepository
from ...infrastructure.repositories.sqlalchemy_incident_repository import SQLAlchemyIncidentRepository
from ...domain.patterns.concrete_observers import NotificationObserver
from sqlalchemy.orm import Session


def initialize_event_system(
    db: Session,
    event_bus: EventBus | None = None,
) -> EventBus:
    """
    Initialize event system with all observers and commands.

    Args:
        db: Database session for repositories
        event_bus: Optional existing event bus (creates new if None)

    Returns:
        Configured EventBus instance
    """
    if event_bus is None:
        event_bus = EventBus()

    # Create repositories
    user_repo = SQLAlchemyUserRepository(db)
    notification_repo = SQLAlchemyNotificationRepository(db)
    incident_repo = SQLAlchemyIncidentRepository(db)

    # Create command factory
    command_factory = CommandFactory()

    # Register email and slack commands with factory
    # (concrete command classes will be added to factory in notifications module)

    # Create and register observers
    notification_observer = NotificationObserver(
        notification_repo=notification_repo,
        user_repo=user_repo,
        incident_repo=incident_repo,
        command_factory=command_factory,
    )
    event_bus.attach(notification_observer)

    # Could add AuditLogObserver here if implemented

    return event_bus
