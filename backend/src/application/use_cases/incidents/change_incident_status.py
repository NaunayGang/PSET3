"""Change incident status use case."""

from datetime import datetime, timezone

from ...dtos.incident_dto import IncidentStatusUpdate
from ....domain.entities.incident import Incident
from ....domain.enums.event_type import EventType
from ....domain.enums.incident_status import IncidentStatus
from ....domain.patterns.observer import Subject, DomainEvent
from ....domain.patterns.state import IncidentStateMachine
from ....domain.repositories.incident_repository import IncidentRepository
from ....domain.exceptions import InvalidStateTransitionError


class ChangeIncidentStatusUseCase:
    """Use case for changing incident status using State pattern."""

    def __init__(self, incident_repository: IncidentRepository, event_publisher: Subject | None = None):
        """
        Initialize use case.

        Args:
            incident_repository: Incident repository
        """
        self.incident_repository = incident_repository
        self.state_machine = IncidentStateMachine()
        self.event_publisher = event_publisher

    def execute(self, incident_id: int, new_status: IncidentStatus, user_id: int) -> Incident:
        """
        Change incident status with State pattern validation.

        Args:
            incident_id: ID of incident
            new_status: Desired new status
            user_id: User performing action (for permission checks)

        Returns:
            Updated incident

        Raises:
            EntityNotFoundError: If incident not found
            InvalidStateTransitionError: If transition is not allowed
        """
        # Get incident
        incident = self.incident_repository.find_by_id(incident_id)
        if not incident:
            raise ValueError(f"Incident {incident_id} not found")

        # Validate state transition using State pattern
        if not self.state_machine.can_transition(incident.status, new_status):
            raise InvalidStateTransitionError(
                f"Cannot transition from {incident.status.value} to {new_status.value}"
            )

        # Update status
        previous_status = incident.status
        incident.status = new_status
        incident.updated_at = datetime.now()

        saved = self.incident_repository.save(incident)

        if self.event_publisher is not None:
            self.event_publisher.notify(
                DomainEvent(
                    event_type=EventType.INCIDENT_STATUS_CHANGED,
                    data={
                        "incident_id": saved.id,
                        "previous_status": previous_status.value,
                        "new_status": saved.status.value,
                        "changer_id": user_id,
                    },
                    timestamp=datetime.now(timezone.utc),
                )
            )

        return saved
