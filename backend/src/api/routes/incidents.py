"""Incident management routes."""

from typing import Annotated
from fastapi import APIRouter, Depends, Query, HTTPException, status

from ...application.dtos.incident_dto import (
    IncidentCreate,
    IncidentResponse,
    IncidentAssign,
    IncidentStatusUpdate,
)
from ...application.use_cases.incidents.create_incident import CreateIncidentUseCase
from ...application.use_cases.incidents.assign_incident import AssignIncidentUseCase
from ...application.use_cases.incidents.change_incident_status import ChangeIncidentStatusUseCase
from ...application.use_cases.incidents.list_incidents import ListIncidentsUseCase
from ...application.use_cases.incidents.get_incident import GetIncidentUseCase
from ...domain.repositories.incident_repository import IncidentRepository
from ...domain.repositories.user_repository import UserRepository
from ...domain.entities.user import User
from ...domain.exceptions import EntityNotFoundError, InvalidStateTransitionError
from ...infrastructure.events.event_bus import EventBus
from ..dependencies import get_incident_repository, get_user_repository, get_current_user, get_event_bus

router = APIRouter()


@router.get("", response_model=list[IncidentResponse])
def list_incidents(
    current_user: Annotated[User, Depends(get_current_user)],
    incident_repo: Annotated[IncidentRepository, Depends(get_incident_repository)],
):
    """
    List incidents with role-based filtering.

    - ADMIN: sees all incidents
    - SUPERVISOR: sees all incidents
    - OPERATOR: sees only incidents they created or are assigned to
    """
    use_case = ListIncidentsUseCase(incident_repo)
    return use_case.execute(current_user)


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    incident_repo: Annotated[IncidentRepository, Depends(get_incident_repository)],
):
    """
    Get incident by ID with access control.
    """
    use_case = GetIncidentUseCase(incident_repo)
    incident = use_case.execute(incident_id, current_user)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found or access denied"
        )
    return incident


@router.post("", response_model=IncidentResponse)
def create_incident(
    data: IncidentCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    incident_repo: Annotated[IncidentRepository, Depends(get_incident_repository)],
    event_bus: Annotated[EventBus, Depends(get_event_bus)],
):
    """
    Create a new incident.

    Any authenticated user can create incidents (OPERATOR and above).
    """
    use_case = CreateIncidentUseCase(incident_repo, event_bus=event_bus)
    try:
        return use_case.execute(data, created_by=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{incident_id}/assign", response_model=IncidentResponse)
def assign_incident(
    incident_id: int,
    assignment: IncidentAssign,
    current_user: Annotated[User, Depends(get_current_user)],
    incident_repo: Annotated[IncidentRepository, Depends(get_incident_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    event_bus: Annotated[EventBus, Depends(get_event_bus)],
):

    """
    Assign incident to a user.

    Requires SUPERVISOR or ADMIN role (should be enforced by route decorator).
    """
    use_case = AssignIncidentUseCase(incident_repo, user_repo, event_bus=event_bus)

    try:
        return use_case.execute(
            incident_id=incident_id,
            assigned_to_id=assignment.assigned_to,
            assigner_id=current_user.id,
        )
    except (ValueError, EntityNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{incident_id}/status", response_model=IncidentResponse)
def change_incident_status(
    incident_id: int,
    status_update: IncidentStatusUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    incident_repo: Annotated[IncidentRepository, Depends(get_incident_repository)],
    event_bus: Annotated[EventBus, Depends(get_event_bus)],
):

    """
    Change incident status.

    Status transitions governed by State pattern.
    - OPERATOR can change their own incidents (implemented in future)
    - SUPERVISOR/ADMIN can change any incident
    """
    use_case = ChangeIncidentStatusUseCase(incident_repo, event_bus=event_bus)

    try:
        return use_case.execute(
            incident_id=incident_id,
            new_status=status_update.status,
            user_id=current_user.id,
        )
    except (ValueError, InvalidStateTransitionError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
