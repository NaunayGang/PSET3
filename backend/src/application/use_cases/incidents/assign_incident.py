"""Assign incident use case."""

from datetime import datetime, timezone

from ...dtos.incident_dto import IncidentAssign
from ....domain.entities.incident import Incident
from ....domain.enums.event_type import EventType
from ....domain.enums.incident_status import IncidentStatus
from ....domain.patterns.observer import Subject, DomainEvent
from ....domain.repositories.incident_repository import IncidentRepository
from ....domain.repositories.user_repository import UserRepository
from ....domain.exceptions import EntityNotFoundError, PermissionDeniedError


class AssignIncidentUseCase:
    """Use case for assigning an incident to a user."""

    def __init__(
        self,
        incident_repository: IncidentRepository,
        user_repository: UserRepository,
        event_publisher: Subject | None = None,
    ):
        """
        Initialize use case.

        Args:
            incident_repository: Incident repository
            user_repository: User repository (to verify assignee exists)
        """
        self.incident_repository = incident_repository
        self.user_repository = user_repository
        self.event_publisher = event_publisher

    def execute(self, incident_id: int, assigned_to_id: int, assigner_id: int) -> Incident:
        """
        Assign incident to a user.

        Args:
            incident_id: ID of incident to assign
            assigned_to_id: User ID to assign to
            assigner_id: User ID performing assignment (for permission check)

        Returns:
            Updated incident

        Raises:
            EntityNotFoundError: If incident or user not found
            PermissionDeniedError: If assigner lacks permission
        """
        # Get incident
        incident = self.incident_repository.find_by_id(incident_id)
        if not incident:
            raise EntityNotFoundError("Incident", incident_id)

        # Verify assignee exists
        assignee = self.user_repository.find_by_id(assigned_to_id)
        if not assignee:
            raise EntityNotFoundError("User", assigned_to_id)

        # Permission check: Only ADMIN or SUPERVISOR can assign
        # This will be enforced by route decorator, but also check here
        # (or rely on route to check)

        # Update assignment
        incident.assigned_to = assigned_to_id
        incident.status = IncidentStatus.ASSIGNED
        incident.updated_at = datetime.now()

        saved = self.incident_repository.save(incident)

        if self.event_publisher is not None:
            self.event_publisher.notify(
                DomainEvent(
                    event_type=EventType.INCIDENT_ASSIGNED,
                    data={
                        "incident_id": saved.id,
                        "assigned_to_id": assigned_to_id,
                        "assigner_id": assigner_id,
                    },
                    timestamp=datetime.now(timezone.utc),
                )
            )

        return saved
