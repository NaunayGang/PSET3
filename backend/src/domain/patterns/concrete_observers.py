"""Concrete Observer implementations for notification system.

These observers react to domain events and perform actions like creating notifications.
"""

from typing import Optional
from ...domain.patterns.observer import Observer, DomainEvent
from ...domain.patterns.factory import EntityFactory, CommandFactory
from ...domain.enums.event_type import EventType
from ...domain.repositories.notification_repository import NotificationRepository
from ...domain.repositories.user_repository import UserRepository
from ...domain.repositories.incident_repository import IncidentRepository
from ...domain.entities.notification import Notification
from ...domain.enums.notification_channel import NotificationChannel
from ...domain.enums.notification_status import NotificationStatus
from ...domain.patterns.template_method import NotificationBuilder
from ...infrastructure.notifications.email_sender import EmailNotificationCommand
from ...infrastructure.notifications.slack_sender import SlackNotificationCommand
import logging

logger = logging.getLogger(__name__)


class NotificationObserver(Observer):
    """
    Observer that creates notifications for relevant domain events.

    When an event occurs, this observer:
    1. Determines who should be notified
    2. Creates a notification entity
    3. Builds message using Template Method pattern
    4. Creates and executes command for delivery
    """

    def __init__(
        self,
        notification_repo: NotificationRepository,
        user_repo: UserRepository,
        incident_repo: IncidentRepository,
        command_factory: CommandFactory,
    ):
        """
        Initialize observer.

        Args:
            notification_repo: Repository for persisting notifications
            user_repo: User repository (to get recipient info)
            incident_repo: Incident repository (to get incident details)
            command_factory: Factory for creating delivery commands
        """
        self.notification_repo = notification_repo
        self.user_repo = user_repo
        self.incident_repo = incident_repo
        self.command_factory = command_factory

        # Register command types with factory
        self.command_factory.create_email_command = self._create_email_command
        self.command_factory.create_slack_command = self._create_slack_command

    def update(self, event: DomainEvent) -> None:
        """
        React to a domain event.

        Args:
            event: The domain event to process
        """
        logger.debug(f"NotificationObserver received event: {event.event_type}")

        try:
            if event.event_type == EventType.INCIDENT_CREATED:
                self._handle_incident_created(event)
            elif event.event_type == EventType.INCIDENT_ASSIGNED:
                self._handle_incident_assigned(event)
            elif event.event_type == EventType.INCIDENT_STATUS_CHANGED:
                self._handle_incident_status_changed(event)
            elif event.event_type == EventType.TASK_CREATED:
                self._handle_task_created(event)
            elif event.event_type == EventType.TASK_DONE:
                self._handle_task_done(event)
        except Exception as e:
            logger.error(f"Error processing event {event.event_type}: {e}", exc_info=True)

    def _handle_incident_created(self, event: DomainEvent) -> None:
        """Handle incident created event."""
        incident_id = event.data["incident_id"]
        incident = self.incident_repo.find_by_id(incident_id)
        if not incident:
            logger.warning(f"Incident {incident_id} not found for notification")
            return

        # Notify incident creator (and maybe supervisors)
        # For now, notify the creator
        recipient = self.user_repo.find_by_id(incident.created_by)
        if not recipient:
            return

        # Build notification using Template Method
        builder = IncidentCreatedNotificationBuilder({
            "id": incident.id,
            "title": incident.title,
            "severity": incident.severity.value,
            "creator_name": recipient.name,
        })
        message = builder.build_notification()

        # Create notification entity
        notification = self._create_notification(
            recipient_id=recipient.id,
            channel=NotificationChannel.EMAIL,
            message=message,
            event_type=EventType.INCIDENT_CREATED,
        )

        # Send via command
        command = self._create_email_command(
            recipient=recipient.email,
            subject=builder.build_subject(),
            body=builder.build_body(),
        )
        command.execute()

    def _handle_incident_assigned(self, event: DomainEvent) -> None:
        """Handle incident assigned event."""
        incident_id = event.data["incident_id"]
        incident = self.incident_repo.find_by_id(incident_id)
        if not incident or not incident.assigned_to:
            return

        # Notify assigned user
        recipient = self.user_repo.find_by_id(incident.assigned_to)
        assigner = self.user_repo.find_by_id(event.data["assigner_id"])

        if not recipient:
            return

        builder = IncidentAssignedNotificationBuilder(
            incident_data={
                "id": incident.id,
                "title": incident.title,
                "severity": incident.severity.value,
            },
            assigner_name=assigner.name if assigner else "System",
        )
        message = builder.build_notification()

        notification = self._create_notification(
            recipient_id=recipient.id,
            channel=NotificationChannel.EMAIL,
            message=message,
            event_type=EventType.INCIDENT_ASSIGNED,
        )

        command = self._create_email_command(
            recipient=recipient.email,
            subject=builder.build_subject(),
            body=builder.build_body(),
        )
        command.execute()

    def _handle_incident_status_changed(self, event: DomainEvent) -> None:
        """Handle incident status changed event."""
        incident_id = event.data["incident_id"]
        incident = self.incident_repo.find_by_id(incident_id)
        if not incident:
            return

        # Notify incident creator and assignee
        recipients = []
        if incident.created_by:
            creator = self.user_repo.find_by_id(incident.created_by)
            if creator:
                recipients.append(creator)
        if incident.assigned_to and incident.assigned_to != incident.created_by:
            assignee = self.user_repo.find_by_id(incident.assigned_to)
            if assignee:
                recipients.append(assignee)

        changer = self.user_repo.find_by_id(event.data["changer_id"])

        for recipient in recipients:
            builder = IncidentStatusChangedNotificationBuilder(
                incident_data={
                    "id": incident.id,
                    "title": incident.title,
                },
                new_status=event.data["new_status"],
                changed_by_name=changer.name if changer else "System",
            )
            message = builder.build_notification()

            self._create_notification(
                recipient_id=recipient.id,
                channel=NotificationChannel.EMAIL,
                message=message,
                event_type=EventType.INCIDENT_STATUS_CHANGED,
            )

            command = self._create_email_command(
                recipient=recipient.email,
                subject=builder.build_subject(),
                body=builder.build_body(),
            )
            command.execute()

    def _handle_task_created(self, event: DomainEvent) -> None:
        """Handle task created event."""
        task_id = event.data["task_id"]
        # Need task repository to get task details - not implemented yet
        # For now, minimal implementation
        logger.info(f"Task {task_id} created - notification would be sent")

    def _handle_task_done(self, event: DomainEvent) -> None:
        """Handle task done event."""
        task_id = event.data["task_id"]
        logger.info(f"Task {task_id} marked done - notification would be sent")

    def _create_notification(
        self,
        recipient_id: int,
        channel: NotificationChannel,
        message: str,
        event_type: EventType,
    ) -> Notification:
        """
        Create and persist a notification entity.

        Args:
            recipient_id: User ID to receive notification
            channel: Delivery channel
            message: Notification message
            event_type: Type of event

        Returns:
            Created notification entity
        """
        from ...domain.patterns.factory import EntityFactory

        factory = EntityFactory()
        notification = factory.create_notification(
            id=None,
            recipient_id=recipient_id,
            channel=channel,
            message=message,
            event_type=event_type,
            status=NotificationStatus.PENDING,
        )
        return self.notification_repo.save(notification)

    def _create_email_command(self, recipient: str, subject: str, body: str) -> EmailNotificationCommand:
        """Create an email command."""
        return EmailNotificationCommand(recipient, subject, body)

    def _create_slack_command(self, webhook_url: str, message: str) -> SlackNotificationCommand:
        """Create a Slack command."""
        return SlackNotificationCommand(webhook_url, message)


class AuditLogObserver(Observer):
    """Observer that logs all domain events for audit purposes."""

    def update(self, event: DomainEvent) -> None:
        """
        Log event for audit trail.

        Args:
            event: The domain event to log
        """
        logger.info(
            f"[AUDIT] Event: {event.event_type} | "
            f"Data: {event.data} | "
            f"Timestamp: {event.timestamp}"
        )
