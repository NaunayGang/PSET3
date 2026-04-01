"""Template Method pattern for notification building.

Template Method defines the skeleton of an algorithm in a base class,
letting subclasses override specific steps without changing the algorithm's structure.
"""

from abc import ABC, abstractmethod


class NotificationBuilder(ABC):
    """
    Template Method base class for building notifications.

    Defines the template for building notifications while allowing subclasses
    to customize specific parts.
    """

    def __init__(self, data: dict):
        """
        Initialize builder with event data.

        Args:
            data: Dictionary with event-specific data
        """
        self.data = data

    def build_notification(self) -> str:
        """
        Build the notification message (Template Method).

        This method defines the skeleton of the notification building process.
        Subclasses override specific methods to customize content.

        Returns:
            Complete notification message
        """
        message = []
        message.append(self.build_header())
        message.append(self.build_body())
        message.append(self.build_footer())
        return "\n".join(filter(None, message))

    @abstractmethod
    def build_header(self) -> str:
        """Build notification header. Override in subclass."""
        pass

    @abstractmethod
    def build_body(self) -> str:
        """Build notification body. Override in subclass."""
        pass

    @abstractmethod
    def build_footer(self) -> str:
        """Build notification footer. Override in subclass."""
        pass

    @abstractmethod
    def build_subject(self) -> str:
        """Build email subject line. Override in subclass."""
        pass


class IncidentCreatedNotificationBuilder(NotificationBuilder):
    """Builder for incident created notification."""

    def build_header(self) -> str:
        return "New Incident Created"

    def build_body(self) -> str:
        incident_id = self.data.get("id")
        title = self.data.get("title")
        severity = self.data.get("severity")
        return f"Incident #{incident_id}: {title}\nSeverity: {severity}"

    def build_footer(self) -> str:
        return "Please log in to the OpsCenter dashboard for details."

    def build_subject(self) -> str:
        return f"New Incident: {self.data.get('title')}"


class IncidentAssignedNotificationBuilder(NotificationBuilder):
    """Builder for incident assigned notification."""

    def __init__(self, incident_data: dict, assigner_name: str = "System"):
        self.incident_data = incident_data
        self.assigner_name = assigner_name
        super().__init__(incident_data)

    def build_header(self) -> str:
        return "Incident Assigned to You"

    def build_body(self) -> str:
        title = self.incident_data.get("title")
        severity = self.incident_data.get("severity")
        return (
            f"An incident has been assigned to you:\n"
            f"Title: {title}\n"
            f"Severity: {severity}\n"
            f"Assigned by: {self.assigner_name}"
        )

    def build_footer(self) -> str:
        return "Click here to view and update the incident."

    def build_subject(self) -> str:
        return f"Incident Assigned: {self.incident_data.get('title')}"


class IncidentStatusChangedNotificationBuilder(NotificationBuilder):
    """Builder for incident status change notification."""

    def __init__(
        self,
        incident_data: dict,
        new_status: str,
        changed_by_name: str = "System",
    ):
        self.incident_data = incident_data
        self.new_status = new_status
        self.changed_by_name = changed_by_name
        super().__init__(incident_data)

    def build_header(self) -> str:
        return "Incident Status Updated"

    def build_body(self) -> str:
        title = self.incident_data.get("title")
        incident_id = self.incident_data.get("id")
        return (
            f"Incident #{incident_id}: {title}\n"
            f"New Status: {self.new_status}\n"
            f"Changed by: {self.changed_by_name}"
        )

    def build_footer(self) -> str:
        return "View incident details in the OpsCenter dashboard."

    def build_subject(self) -> str:
        return f"Incident #{self.incident_data.get('id')} Status Changed to {self.new_status}"


class TaskAssignedNotificationBuilder(NotificationBuilder):
    """Builder for task assigned notification."""

    def __init__(self, task_data: dict, assigner_name: str = "System"):
        self.task_data = task_data
        self.assigner_name = assigner_name
        super().__init__(task_data)

    def build_header(self) -> str:
        return "Task Assigned to You"

    def build_body(self) -> str:
        title = self.task_data.get("title")
        incident_id = self.task_data.get("incident_id")
        return (
            f"A task has been assigned to you:\n"
            f"Task: {title}\n"
            f"Related Incident: #{incident_id}\n"
            f"Assigned by: {self.assigner_name}"
        )

    def build_footer(self) -> str:
        return "View task details in the OpsCenter dashboard."

    def build_subject(self) -> str:
        return f"Task Assigned: {self.task_data.get('title')}"
