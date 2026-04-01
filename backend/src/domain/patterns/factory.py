"""Factory pattern for centralized entity creation and validation.

The Factory pattern provides an interface for creating objects, centralizing
object creation logic and validation in one place.
"""

from datetime import datetime, timezone
from typing import Optional

from ..entities.incident import Incident
from ..entities.notification import Notification
from ..entities.task import Task
from ..entities.user import User
from ..enums.event_type import EventType
from ..enums.incident_severity import IncidentSeverity
from ..enums.incident_status import IncidentStatus
from ..enums.notification_channel import NotificationChannel
from ..enums.notification_status import NotificationStatus
from ..enums.role import Role
from ..enums.task_status import TaskStatus


class EntityFactory:
    """Factory for creating and validating domain entities."""

    @staticmethod
    def create_user(
        id: Optional[int],
        name: str,
        email: str,
        role: Role,
        hashed_password: str,
        created_at: Optional[datetime] = None,
    ) -> User:
        """
        Create a User entity with validation.

        Args:
            id: User ID (None for new users)
            name: User name
            email: User email address
            role: User role
            hashed_password: Hashed password
            created_at: Creation timestamp (defaults to now)

        Returns:
            Validated User entity

        Raises:
            ValueError: If validation fails
        """
        # Validation
        if not name or not name.strip():
            raise ValueError("User name cannot be empty")

        if not email or "@" not in email:
            raise ValueError("Invalid email address")

        if not hashed_password:
            raise ValueError("Password hash cannot be empty")

        if created_at is None:
            created_at = datetime.now(timezone.utc)

        return User(
            id=id,
            name=name.strip(),
            email=email.strip().lower(),
            role=role,
            hashed_password=hashed_password,
            created_at=created_at,
        )

    @staticmethod
    def create_incident(
        id: Optional[int],
        title: str,
        description: str,
        severity: IncidentSeverity,
        status: IncidentStatus,
        created_by: int,
        assigned_to: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> Incident:
        """
        Create an Incident entity with validation.

        Args:
            id: Incident ID (None for new incidents)
            title: Incident title
            description: Incident description
            severity: Incident severity level
            status: Incident status
            created_by: User ID who created the incident
            assigned_to: User ID incident is assigned to (optional)
            created_at: Creation timestamp (defaults to now)
            updated_at: Last update timestamp (defaults to now)

        Returns:
            Validated Incident entity

        Raises:
            ValueError: If validation fails
        """
        # Validation
        if not title or not title.strip():
            raise ValueError("Incident title cannot be empty")

        if not description or not description.strip():
            raise ValueError("Incident description cannot be empty")

        if created_by is None or created_by <= 0:
            raise ValueError("Invalid created_by user ID")

        if created_at is None:
            created_at = datetime.now(timezone.utc)

        if updated_at is None:
            updated_at = created_at

        return Incident(
            id=id,
            title=title.strip(),
            description=description.strip(),
            severity=severity,
            status=status,
            created_by=created_by,
            assigned_to=assigned_to,
            created_at=created_at,
            updated_at=updated_at,
        )

    @staticmethod
    def create_task(
        id: Optional[int],
        incident_id: int,
        title: str,
        description: str,
        status: TaskStatus,
        assigned_to: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> Task:
        """
        Create a Task entity with validation.

        Args:
            id: Task ID (None for new tasks)
            incident_id: ID of the incident this task belongs to
            title: Task title
            description: Task description
            status: Task status
            assigned_to: User ID task is assigned to (optional)
            created_at: Creation timestamp (defaults to now)
            updated_at: Last update timestamp (defaults to now)

        Returns:
            Validated Task entity

        Raises:
            ValueError: If validation fails
        """
        # Validation
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")

        if incident_id is None or incident_id <= 0:
            raise ValueError("Invalid incident_id")

        if created_at is None:
            created_at = datetime.now(timezone.utc)

        if updated_at is None:
            updated_at = created_at

        return Task(
            id=id,
            incident_id=incident_id,
            title=title.strip(),
            description=description.strip(),
            status=status,
            assigned_to=assigned_to,
            created_at=created_at,
            updated_at=updated_at,
        )

    @staticmethod
    def create_notification(
        id: Optional[int],
        recipient_id: int,
        channel: NotificationChannel,
        message: str,
        event_type: EventType,
        status: NotificationStatus = NotificationStatus.PENDING,
        created_at: Optional[datetime] = None,
    ) -> Notification:
        """
        Create a Notification entity with validation.

        Args:
            id: Notification ID (None for new notifications)
            recipient_id: User ID who will receive the notification
            channel: Delivery channel (email, slack, etc.)
            message: Notification message content
            event_type: Type of event that triggered this notification
            status: Notification status (defaults to PENDING)
            created_at: Creation timestamp (defaults to now)

        Returns:
            Validated Notification entity

        Raises:
            ValueError: If validation fails
        """
        # Validation
        if recipient_id is None or recipient_id <= 0:
            raise ValueError("Invalid recipient_id")

        if not message or not message.strip():
            raise ValueError("Notification message cannot be empty")

        if created_at is None:
            created_at = datetime.now(timezone.utc)

        return Notification(
            id=id,
            recipient_id=recipient_id,
            channel=channel,
            message=message.strip(),
            event_type=event_type,
            status=status,
            created_at=created_at,
        )


class CommandFactory:
    """Factory for creating command objects.

    Note: Concrete command classes are defined in the infrastructure layer.
    This factory will be extended there.
    """

    # Will be implemented in infrastructure layer where concrete commands exist
    pass
