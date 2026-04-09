"""Create incident use case."""

from datetime import datetime, timezone

from ...dtos.incident_dto import IncidentCreate, IncidentResponse
from ....domain.entities.incident import Incident
from ....domain.enums.event_type import EventType
from ....domain.enums.incident_status import IncidentStatus
from ....domain.patterns.observer import Subject, DomainEvent
from ....domain.repositories.incident_repository import IncidentRepository
from ....domain.patterns.factory import EntityFactory
from ....infrastructure.events.event_bus import EventBus


class CreateIncidentUseCase:
    """Use case for creating a new incident."""

    def __init__(
        self,
        incident_repository: IncidentRepository,
        factory: EntityFactory | None = None,
        event_publisher: Subject | None = None,
    ):
        """
        Initialize use case.

        Args:
            incident_repository: Incident repository for persistence
            factory: Optional entity factory (creates new if not provided)
        """
        self.incident_repository = incident_repository
        self.factory = factory or EntityFactory()
        self.event_publisher = event_publisher

    def execute(self, data: IncidentCreate, created_by: int) -> Incident:
        """
        Create a new incident.

        Args:
            data: Incident creation data (title, description, severity)
            created_by: User ID of creator

        Returns:
            Created Incident entity

        Raises:
            ValueError: If validation fails
        """
        # Validate required fields (Pydantic already validated types)
        if not data.title.strip():
            raise ValueError("Title cannot be empty")
        if not data.description.strip():
            raise ValueError("Description cannot be empty")

        # Create incident entity with OPEN status
        incident = self.factory.create_incident(
            id=None,
            title=data.title.strip(),
            description=data.description.strip(),
            severity=data.severity,
            status=IncidentStatus.OPEN,
            created_by=created_by,
            assigned_to=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        # Persist
        saved = self.incident_repository.save(incident)

        if self.event_publisher is not None:
            self.event_publisher.notify(
                DomainEvent(
                    event_type=EventType.INCIDENT_CREATED,
                    data={
                        "incident_id": saved.id,
                        "created_by": saved.created_by,
                    },
                    timestamp=datetime.now(timezone.utc),
                )
            )

        return saved
