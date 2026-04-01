"""Task domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..enums.task_status import TaskStatus


@dataclass
class Task:
    """Task entity representing a work item linked to an incident."""

    id: Optional[int]
    incident_id: int
    title: str
    description: str
    status: TaskStatus
    assigned_to: Optional[int]
    created_at: datetime
    updated_at: datetime

    def is_open(self) -> bool:
        """Check if task is open."""
        return self.status == TaskStatus.OPEN

    def is_in_progress(self) -> bool:
        """Check if task is in progress."""
        return self.status == TaskStatus.IN_PROGRESS

    def is_done(self) -> bool:
        """Check if task is done."""
        return self.status == TaskStatus.DONE

    def is_assigned(self) -> bool:
        """Check if task is assigned."""
        return self.assigned_to is not None
