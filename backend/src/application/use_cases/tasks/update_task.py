"""Update task use case."""

from datetime import datetime, timezone

from ...dtos.task_dto import TaskUpdate
from ....domain.entities.task import Task
from ....domain.repositories.task_repository import TaskRepository
from ....domain.repositories.user_repository import UserRepository
from ....domain.enums.role import Role
from ....domain.enums.task_status import TaskStatus
from ....domain.enums.event_type import EventType
from ....domain.patterns.observer import DomainEvent
from ....domain.exceptions import EntityNotFoundError, PermissionDeniedError
from ....infrastructure.events.event_bus import EventBus



class UpdateTaskUseCase:
    """Use case for updating a task."""

    def __init__(
        self,
        task_repository: TaskRepository,
        user_repository: UserRepository,
        event_bus: EventBus | None = None,
    ):

        """
        Initialize use case.

        Args:
            task_repository: Task repository
            user_repository: User repository (for permission checks)
        """
        self.task_repository = task_repository
        self.user_repository = user_repository
        self.event_bus = event_bus


    def execute(self, task_id: int, updates: TaskUpdate, user_id: int) -> Task:
        """
        Update a task with validation.

        Args:
            task_id: ID of task to update
            updates: Fields to update
            user_id: User performing update (for permission checks)

        Returns:
            Updated task

        Raises:
            EntityNotFoundError: If task not found
            PermissionDeniedError: If user lacks permission
        """
        # Get task
        task = self.task_repository.find_by_id(task_id)
        if not task:
            raise EntityNotFoundError("Task", task_id)

        # Permission check: user must be assigned to task or have SUPERVISOR/ADMIN role
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise EntityNotFoundError("User", user_id)

        is_assigned = task.assigned_to == user_id
        is_privileged = user.role in [Role.ADMIN, Role.SUPERVISOR]

        if not (is_assigned or is_privileged):
            raise PermissionDeniedError("Cannot update this task")

        # Track previous values for event publishing
        previous_status = task.status
        previous_assigned_to = task.assigned_to

        # Apply updates
        if updates.title is not None:

            task.title = updates.title.strip()
        if updates.description is not None:
            task.description = updates.description.strip()
        if updates.status is not None:
            task.status = updates.status
        if updates.assigned_to is not None:
            # Changing assignee requires privilege
            if not is_privileged:
                raise PermissionDeniedError("Only ADMIN/SUPERVISOR can reassign tasks")
            # Validate that the new assignee exists
            new_assignee = self.user_repository.find_by_id(updates.assigned_to)
            if not new_assignee:
                raise EntityNotFoundError("User", updates.assigned_to)
            task.assigned_to = updates.assigned_to

        task.updated_at = datetime.now(timezone.utc)

        # Persist
        saved = self.task_repository.save(task)

        if self.event_bus is not None and saved.id is not None:
            if saved.assigned_to is not None and saved.assigned_to != previous_assigned_to:
                self.event_bus.publish(
                    DomainEvent(
                        event_type=EventType.TASK_ASSIGNED,
                        data={
                            "task_id": saved.id,
                            "incident_id": saved.incident_id,
                            "assigned_to_id": saved.assigned_to,
                            "assigner_id": user_id,
                        },
                        timestamp=datetime.now(timezone.utc),
                    )
                )

            if previous_status != TaskStatus.DONE and saved.status == TaskStatus.DONE:
                self.event_bus.publish(
                    DomainEvent(
                        event_type=EventType.TASK_DONE,
                        data={
                            "task_id": saved.id,
                            "incident_id": saved.incident_id,
                            "completed_by": user_id,
                        },
                        timestamp=datetime.now(timezone.utc),
                    )
                )

        return saved

