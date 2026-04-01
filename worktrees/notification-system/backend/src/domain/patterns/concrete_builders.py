"""Concrete NotificationBuilder implementations for Template Method pattern.

These builders create formatted notification messages for different event types.
"""

from ...domain.patterns.template_method import NotificationBuilder
from ...domain.enums.event_type import EventType


class IncidentCreatedNotificationBuilder(NotificationBuilder):
    """Builder for incident created notifications."""

    def __init__(self, incident_data: dict):
        """
        Initialize builder.

        Args:
            incident_data: Dictionary with incident info (id, title, severity, creator_name)
        """
        self.incident_data = incident_data

    def build_subject(self) -> str:
        """Build subject: 'New Incident Created: [title]'."""
        title = self.incident_data.get("title", "Unknown")
        return f"New Incident Created: {title}"

    def build_body(self) -> str:
        """Build body with incident details."""
        title = self.incident_data.get("title", "N/A")
        severity = self.incident_data.get("severity", "N/A")
        creator = self.incident_data.get("creator_name", "Unknown")
        incident_id = self.incident_data.get("id", "N/A")

        return f"""A new incident has been created in OpsCenter.

Incident ID: #{incident_id}
Title: {title}
Severity: {severity}
Created by: {creator}

Please review and take appropriate action.
"""


class IncidentAssignedNotificationBuilder(NotificationBuilder):
    """Builder for incident assigned notifications."""

    def __init__(self, incident_data: dict, assigner_name: str):
        """
        Initialize builder.

        Args:
            incident_data: Dictionary with incident info
            assigner_name: Name of user who assigned the incident
        """
        self.incident_data = incident_data
        self.assigner_name = assigner_name

    def build_subject(self) -> str:
        """Build subject: 'Incident Assigned to You'."""
        return "Incident Assigned to You"

    def build_body(self) -> str:
        """Build body with assignment details."""
        title = self.incident_data.get("title", "N/A")
        severity = self.incident_data.get("severity", "N/A")
        incident_id = self.incident_data.get("id", "N/A")

        return f"""An incident has been assigned to you by {self.assigner_name}.

Incident ID: #{incident_id}
Title: {title}
Severity: {severity}

Please review the incident and begin work.
"""


class IncidentStatusChangedNotificationBuilder(NotificationBuilder):
    """Builder for incident status change notifications."""

    def __init__(self, incident_data: dict, new_status: str, changed_by_name: str):
        """
        Initialize builder.

        Args:
            incident_data: Dictionary with incident info
            new_status: New incident status
            changed_by_name: Name of user who changed status
        """
        self.incident_data = incident_data
        self.new_status = new_status
        self.changed_by_name = changed_by_name

    def build_subject(self) -> str:
        """Build subject: 'Incident Status Updated'."""
        return f"Incident Status Updated to {self.new_status}"

    def build_body(self) -> str:
        """Build body with status change details."""
        title = self.incident_data.get("title", "N/A")
        incident_id = self.incident_data.get("id", "N/A")

        return f"""The status of an incident has been changed by {self.changed_by_name}.

Incident ID: #{incident_id}
Title: {title}
New Status: {self.new_status}

Check the OpsCenter for more details.
"""


class TaskCreatedNotificationBuilder(NotificationBuilder):
    """Builder for task created notifications."""

    def __init__(self, task_data: dict, incident_title: str, creator_name: str):
        """
        Initialize builder.

        Args:
            task_data: Dictionary with task info
            incident_title: Title of parent incident
            creator_name: Name of task creator
        """
        self.task_data = task_data
        self.incident_title = incident_title
        self.creator_name = creator_name

    def build_subject(self) -> str:
        """Build subject: 'New Task Created'."""
        title = self.task_data.get("title", "Unknown")
        return f"New Task Created: {title}"

    def build_body(self) -> str:
        """Build body with task details."""
        task_title = self.task_data.get("title", "N/A")
        task_description = self.task_data.get("description", "N/A")
        task_id = self.task_data.get("id", "N/A")

        return f"""A new task has been created for you.

Task ID: #{task_id}
Title: {task_title}
Description: {task_description}
Parent Incident: {self.incident_title}
Created by: {self.creator_name}

Please review and begin work on this task.
"""


class TaskDoneNotificationBuilder(NotificationBuilder):
    """Builder for task completed notifications."""

    def __init__(self, task_data: dict, completed_by_name: str):
        """
        Initialize builder.

        Args:
            task_data: Dictionary with task info
            completed_by_name: Name of user who completed the task
        """
        self.task_data = task_data
        self.completed_by_name = completed_by_name

    def build_subject(self) -> str:
        """Build subject: 'Task Completed'."""
        title = self.task_data.get("title", "Unknown")
        return f"Task Completed: {title}"

    def build_body(self) -> str:
        """Build body with completion details."""
        task_title = self.task_data.get("title", "N/A")
        task_id = self.task_data.get("id", "N/A")

        return f"""A task has been marked as completed.

Task ID: #{task_id}
Title: {task_title}
Completed by: {self.completed_by_name}

Great work!
"""
