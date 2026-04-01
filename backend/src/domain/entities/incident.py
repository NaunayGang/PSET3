"""Incident domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..enums.incident_severity import IncidentSeverity
from ..enums.incident_status import IncidentStatus


@dataclass
class Incident:
    """Incident entity representing an operational incident."""

    id: Optional[int]
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus
    created_by: int
    assigned_to: Optional[int]
    created_at: datetime
    updated_at: datetime

    def is_open(self) -> bool:
        """Check if incident is open."""
        return self.status == IncidentStatus.OPEN

    def is_assigned(self) -> bool:
        """Check if incident is assigned."""
        return self.assigned_to is not None

    def is_closed(self) -> bool:
        """Check if incident is closed."""
        return self.status == IncidentStatus.CLOSED

    def can_be_assigned(self) -> bool:
        """Check if incident can be assigned."""
        return self.status in [IncidentStatus.OPEN, IncidentStatus.ASSIGNED]

    def is_critical(self) -> bool:
        """Check if incident is critical severity."""
        return self.severity == IncidentSeverity.CRITICAL
