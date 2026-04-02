"""Template Method pattern for notification message construction.

The Template Method pattern defines the skeleton of an algorithm in a base class,
letting subclasses override specific steps without changing the algorithm's structure.
"""

from abc import ABC, abstractmethod
from typing import Any


class NotificationBuilder(ABC):
    """Abstract base class for building notification messages.

    This class implements the Template Method pattern. The build_notification()
    method defines the algorithm skeleton, while subclasses implement specific steps.
    """

    def __init__(self, data: dict[str, Any]):
        self.data = data

    def build_notification(self) -> str:
        """
        Template method that defines the notification building algorithm.

        This method orchestrates the steps to build a complete notification message.
        Subclasses should NOT override this method.

        Returns:
            The complete formatted notification message
        """
        # Validate first
        self.validate()

        # Build components
        header = self.build_header()
        body = self.build_body()
        footer = self.build_footer()

        # Format the final message
        message = self.format_message(header, body, footer)

        return message

    @abstractmethod
    def build_subject(self) -> str:
        """
        Build the notification subject/title.

        This is a required step that subclasses must implement.

        Returns:
            The notification subject
        """
        pass

    @abstractmethod
    def build_body(self) -> str:
        """
        Build the notification body content.

        This is a required step that subclasses must implement.

        Returns:
            The notification body text
        """
        pass

    def build_header(self) -> str:
        """Build message header using the subject."""
        return f"Subject: {self.build_subject()}"

    def build_footer(self) -> str:
        """Build a common notification footer."""
        return "Please review this notification in OpsCenter."

    def format_message(self, header: str, body: str, footer: str) -> str:
        """
        Format the complete notification message.

        This is a concrete method with default implementation that subclasses
        can optionally override.

        Args:
            subject: The notification subject
            body: The notification body

        Returns:
            The formatted complete message
        """
        return f"{header}\n\n{body}\n\n{footer}"

    def validate(self) -> None:
        """
        Validate the notification data.

        This is a hook method with default implementation. Subclasses can
        override to add validation logic.

        Raises:
            ValueError: If validation fails
        """
        # Default: no validation required
        pass


class IncidentCreatedNotificationBuilder(NotificationBuilder):
    """Builder for incident created notifications."""

    def __init__(self, data: dict[str, Any]):
        super().__init__(data)

    def build_subject(self) -> str:
        title = self.data.get("title", "Unknown Incident")
        return f"New Incident: {title}"

    def build_body(self) -> str:
        incident_id = self.data.get("id", "N/A")
        title = self.data.get("title", "Unknown")
        severity = self.data.get("severity", "Unknown")
        creator = self.data.get("creator_name", "System")
        return (
            f"Incident #{incident_id}: {title}\n"
            f"Severity: {severity}\n"
            f"Created by: {creator}\n\n"
            f"Please log in to the OpsCenter dashboard for details."
        )


class IncidentAssignedNotificationBuilder(NotificationBuilder):
    """Builder for incident assigned notifications."""

    def __init__(self, incident_data: dict[str, Any], assigner_name: str = "System"):
        super().__init__(incident_data)
        self.assigner_name = assigner_name

    def build_subject(self) -> str:
        title = self.data.get("title", "Unknown")
        return f"Incident Assigned: {title}"

    def build_header(self) -> str:
        return f"Incident Assigned - {self.build_subject()}"

    def build_body(self) -> str:
        incident_id = self.data.get("id", "N/A")
        title = self.data.get("title", "Unknown")
        severity = self.data.get("severity", "Unknown")
        return (
            f"Incident #{incident_id}: {title}\n"
            f"Severity: {severity}\n"
            f"Assigned by: {self.assigner_name}\n\n"
            f"Please review and take action in the OpsCenter dashboard."
        )


class IncidentStatusChangedNotificationBuilder(NotificationBuilder):
    """Builder for incident status change notifications."""

    def __init__(self, incident_data: dict[str, Any], new_status: str, changed_by_name: str = "System"):
        super().__init__(incident_data)
        self.new_status = new_status
        self.changed_by_name = changed_by_name

    def build_subject(self) -> str:
        incident_id = self.data.get("id", "N/A")
        return f"Status Updated: Incident #{incident_id} -> {self.new_status}"

    def build_body(self) -> str:
        incident_id = self.data.get("id", "N/A")
        title = self.data.get("title", "Unknown")
        return (
            f"Incident #{incident_id}: {title}\n"
            f"New Status: {self.new_status}\n"
            f"Changed by: {self.changed_by_name}\n\n"
            f"View the incident details in the OpsCenter dashboard."
        )


class TaskAssignedNotificationBuilder(NotificationBuilder):
    """Builder for task assigned notifications."""

    def __init__(self, data: dict[str, Any], assigner_name: str = "System"):
        super().__init__(data)
        self.assigner_name = assigner_name

    def build_subject(self) -> str:
        title = self.data.get("title", "Unknown Task")
        return f"Task Assigned: {title}"

    def build_body(self) -> str:
        task_id = self.data.get("id", "N/A")
        title = self.data.get("title", "Unknown")
        incident_id = self.data.get("incident_id", "N/A")
        return (
            f"Task #{task_id}: {title}\n"
            f"Related Incident: #{incident_id}\n"
            f"Assigned by: {self.assigner_name}\n\n"
            f"Please complete this task in the OpsCenter dashboard."
        )
