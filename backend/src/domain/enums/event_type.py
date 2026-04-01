"""System event type enumeration."""

from enum import Enum


class EventType(str, Enum):
    """Types of system events for the Observer pattern."""

    INCIDENT_CREATED = "INCIDENT_CREATED"
    INCIDENT_ASSIGNED = "INCIDENT_ASSIGNED"
    INCIDENT_STATUS_CHANGED = "INCIDENT_STATUS_CHANGED"
    TASK_CREATED = "TASK_CREATED"
    TASK_ASSIGNED = "TASK_ASSIGNED"
    TASK_DONE = "TASK_DONE"

    def __str__(self) -> str:
        return self.value
