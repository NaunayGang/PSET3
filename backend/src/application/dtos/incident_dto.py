"""Incident DTOs."""

from datetime import datetime
from pydantic import BaseModel
from ...domain.enums.incident_severity import IncidentSeverity
from ...domain.enums.incident_status import IncidentStatus


class IncidentCreate(BaseModel):
    """Create incident request DTO."""

    title: str
    description: str
    severity: IncidentSeverity


class IncidentUpdate(BaseModel):
    """Update incident request DTO."""

    title: str | None = None
    description: str | None = None
    severity: IncidentSeverity | None = None


class IncidentAssign(BaseModel):
    """Assign incident request DTO."""

    assigned_to: int


class IncidentStatusUpdate(BaseModel):
    """Update incident status request DTO."""

    status: IncidentStatus


class IncidentResponse(BaseModel):
    """Incident response DTO."""

    id: int
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus
    created_by: int
    assigned_to: int | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
