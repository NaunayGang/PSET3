"""List tasks use case."""

from typing import List, Optional

from ....domain.entities.task import Task
from ....domain.repositories.task_repository import TaskRepository
from ....domain.enums.role import Role
from ....domain.entities.user import User


class ListTasksUseCase:
    """Use case for listing tasks with role-based filtering."""

    def __init__(self, task_repository: TaskRepository, incident_repository=None):
        """
        Initialize use case.

        Args:
            task_repository: Task repository
            incident_repository: Optional incident repository for additional filtering
        """
        self.task_repository = task_repository
        self.incident_repository = incident_repository

    def execute(
        self,
        user: User,
        incident_id: Optional[int] = None,
    ) -> List[Task]:
        """
        List tasks with role-based filtering.

        Args:
            user: Current user (determines visibility)
            incident_id: Optional incident ID to filter by

        Returns:
            List of tasks
        """
        if user.role in [Role.ADMIN, Role.SUPERVISOR]:
            # Admin and Supervisor see all tasks (or filtered by incident)
            if incident_id:
                return self.task_repository.list_by_incident(incident_id)
            else:
                return self.task_repository.list_all()
        else:
            # Operator sees only their assigned tasks
            tasks = self.task_repository.list_by_assignee(user.id)
            if incident_id:
                # Further filter by incident
                tasks = [t for t in tasks if t.incident_id == incident_id]
            return tasks
