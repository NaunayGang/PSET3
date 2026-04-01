"""Task repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.task import Task
from ..enums.task_status import TaskStatus


class TaskRepository(ABC):
    """Abstract repository interface for Task entities."""

    @abstractmethod
    def find_by_id(self, task_id: int) -> Optional[Task]:
        """
        Find a task by ID.

        Args:
            task_id: The task ID to search for

        Returns:
            Task entity if found, None otherwise
        """
        pass

    @abstractmethod
    def save(self, task: Task) -> Task:
        """
        Save a task (create or update).

        Args:
            task: The task entity to save

        Returns:
            The saved task entity with updated ID if newly created
        """
        pass

    @abstractmethod
    def list_by_incident(self, incident_id: int) -> List[Task]:
        """
        List tasks associated with a specific incident.

        Args:
            incident_id: The incident ID

        Returns:
            List of task entities for the incident
        """
        pass

    @abstractmethod
    def list_by_assignee(self, user_id: int) -> List[Task]:
        """
        List tasks assigned to a specific user.

        Args:
            user_id: The assignee's user ID

        Returns:
            List of task entities assigned to the user
        """
        pass

    @abstractmethod
    def list_by_status(self, status: TaskStatus) -> List[Task]:
        """
        List tasks by status.

        Args:
            status: The task status to filter by

        Returns:
            List of task entities with the given status
        """
        pass

    @abstractmethod
    def list_all(self) -> List[Task]:
        """
        List all tasks in the system.

        Returns:
            List of all task entities
        """
        pass

    @abstractmethod
    def update_status(self, task_id: int, status: TaskStatus) -> Optional[Task]:
        """
        Update a task's status.

        Args:
            task_id: The task ID
            status: The new status

        Returns:
            Updated task entity if found, None otherwise
        """
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: The task ID to delete

        Returns:
            True if deleted, False if task not found
        """
        pass
