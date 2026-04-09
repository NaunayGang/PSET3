"""Event system initialization.

This module sets up the event bus with all observers on application startup.
"""

from .event_bus import EventBus
from ...domain.patterns.factory import CommandFactory
from ...domain.patterns.concrete_observers import NotificationObserver
from ...domain.repositories.notification_repository import NotificationRepository
from ...domain.repositories.user_repository import UserRepository
from ...domain.repositories.incident_repository import IncidentRepository
from ...domain.repositories.task_repository import TaskRepository


def initialize_event_system(
    notification_repo: NotificationRepository,
    user_repo: UserRepository,
    incident_repo: IncidentRepository,
    task_repo: TaskRepository,
    event_bus: EventBus | None = None,
) -> EventBus:
    """
    Initialize event system with all observers and commands.

    Args:
        notification_repo: Notification repository
        user_repo: User repository
        incident_repo: Incident repository
        task_repo: Task repository
        event_bus: Optional existing event bus (creates new if None)

    Returns:
        Configured EventBus instance
    """
    if event_bus is None:
        event_bus = EventBus()

    # Create command factory
    command_factory = CommandFactory()

    # Register email and slack commands with factory
    # (concrete command classes will be added to factory in notifications module)

    # Create and register observers
    notification_observer = NotificationObserver(
        notification_repo=notification_repo,
        user_repo=user_repo,
        incident_repo=incident_repo,
        task_repo=task_repo,
        command_factory=command_factory,
    )
    event_bus.attach(notification_observer)

    # Could add AuditLogObserver here if implemented

    return event_bus
