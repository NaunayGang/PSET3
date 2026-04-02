"""Task DTOs."""

from datetime import datetime
from pydantic import BaseModel
from ...domain.enums.task_status import TaskStatus


class TaskCreate(BaseModel):
    """Create task request DTO."""

    incident_id: int
    title: str
    description: str


class TaskUpdate(BaseModel):
    """Update task request DTO."""

    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    assigned_to: int | None = None


class TaskStatusUpdate(BaseModel):
    """Update task status request DTO."""

    status: TaskStatus


class TaskResponse(BaseModel):
    """Task response DTO."""

    id: int
    incident_id: int
    title: str
    description: str
    status: TaskStatus
    assigned_to: int | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
