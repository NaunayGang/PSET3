"""Create task use case."""

from datetime import datetime, timezone

from ...dtos.task_dto import TaskCreate
from ....domain.entities.task import Task
from ....domain.enums.event_type import EventType
from ....domain.enums.task_status import TaskStatus
from ....domain.patterns.observer import Subject, DomainEvent
from ....domain.repositories.task_repository import TaskRepository
from ....domain.repositories.incident_repository import IncidentRepository
from ....domain.repositories.user_repository import UserRepository
from ....domain.patterns.factory import EntityFactory
from ....domain.exceptions import EntityNotFoundError, PermissionDeniedError


class CreateTaskUseCase:
    """Use case for creating a new task."""

    def __init__(
        self,
        task_repository: TaskRepository,
        incident_repository: IncidentRepository,
        user_repository: UserRepository,
        factory: EntityFactory | None = None,
        event_publisher: Subject | None = None,
    ):
        """
        Initialize use case.

        Args:
            task_repository: Task repository
            incident_repository: Incident repository (to validate incident exists)
            user_repository: User repository (to check permissions)
            factory: Optional entity factory
        """
        self.task_repository = task_repository
        self.incident_repository = incident_repository
        self.user_repository = user_repository
        self.factory = factory or EntityFactory()
        self.event_publisher = event_publisher

    def execute(self, data: TaskCreate, creator_id: int) -> Task:
        """
        Create a new task linked to an incident.

        Args:
            data: Task creation data (incident_id, title, description)
            creator_id: User ID creating the task

        Returns:
            Created Task entity

        Raises:
            EntityNotFoundError: If incident doesn't exist
            PermissionDeniedError: If creator lacks access to incident
        """
        # Validate incident exists
        incident = self.incident_repository.find_by_id(data.incident_id)
        if not incident:
            raise EntityNotFoundError("Incident", data.incident_id)

        # Permission check: creator must be ADMIN, SUPERVISOR, or incident creator/assignee
        creator = self.user_repository.find_by_id(creator_id)
        if not creator:
            raise EntityNotFoundError("User", creator_id)

        if creator.role.value == "OPERATOR":
            # Operator can only create tasks for incidents they own or are assigned to
            if incident.created_by != creator_id and incident.assigned_to != creator_id:
                raise PermissionDeniedError("Cannot create task for this incident")

        # Create task entity with OPEN status
        task = self.factory.create_task(
            id=None,
            incident_id=data.incident_id,
            title=data.title.strip(),
            description=data.description.strip(),
            status=TaskStatus.OPEN,
            assigned_to=None,  # Not assigned yet
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        # Persist
        saved = self.task_repository.save(task)

        if self.event_publisher is not None:
            self.event_publisher.notify(
                DomainEvent(
                    event_type=EventType.TASK_CREATED,
                    data={
                        "task_id": saved.id,
                        "incident_id": saved.incident_id,
                        "creator_id": creator_id,
                    },
                    timestamp=datetime.now(timezone.utc),
                )
            )

        return saved
