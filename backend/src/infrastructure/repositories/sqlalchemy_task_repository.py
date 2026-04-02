"""SQLAlchemy implementation of TaskRepository."""

from typing import List, Optional
from sqlalchemy.orm import Session

from ...domain.entities.task import Task
from ...domain.enums.task_status import TaskStatus
from ...domain.repositories.task_repository import TaskRepository
from ..database.models.task_model import TaskModel


class SQLAlchemyTaskRepository(TaskRepository):
    """SQLAlchemy implementation of task repository."""

    def __init__(self, session: Session):
        """
        Initialize repository with database session.

        Args:
            session: SQLAlchemy session
        """
        self.session = session

    def _to_entity(self, model: TaskModel) -> Task:
        """
        Convert ORM model to domain entity.

        Args:
            model: TaskModel ORM instance

        Returns:
            Task domain entity
        """
        return Task(
            id=model.id,
            incident_id=model.incident_id,
            title=model.title,
            description=model.description,
            status=TaskStatus(model.status),
            assigned_to=model.assigned_to,
            created_at=model.created_at,
            updated_at=model.updated_at or model.created_at,
        )

    def _to_model(self, entity: Task) -> TaskModel:
        """
        Convert domain entity to ORM model.

        Args:
            entity: Task domain entity

        Returns:
            TaskModel ORM instance
        """
        return TaskModel(
            id=entity.id,
            incident_id=entity.incident_id,
            title=entity.title,
            description=entity.description,
            status=entity.status.value,
            assigned_to=entity.assigned_to,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def find_by_id(self, task_id: int) -> Optional[Task]:
        """Find task by ID."""
        model = self.session.query(TaskModel).filter(TaskModel.id == task_id).first()
        return self._to_entity(model) if model else None

    def save(self, task: Task) -> Task:
        """Save task (create or update)."""
        if task.id:
            # Update existing
            model = self.session.query(TaskModel).filter(TaskModel.id == task.id).first()
            if model:
                model.title = task.title
                model.description = task.description
                model.status = task.status.value
                model.assigned_to = task.assigned_to
                model.incident_id = task.incident_id
                model.updated_at = task.updated_at
            else:
                raise ValueError(f"Task with ID {task.id} not found")
        else:
            # Create new
            model = self._to_model(task)
            self.session.add(model)

        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def list_by_incident(self, incident_id: int) -> List[Task]:
        """List tasks for a specific incident."""
        models = self.session.query(TaskModel).filter(TaskModel.incident_id == incident_id).all()
        return [self._to_entity(m) for m in models]

    def list_by_assignee(self, user_id: int) -> List[Task]:
        """List tasks assigned to a user."""
        models = self.session.query(TaskModel).filter(TaskModel.assigned_to == user_id).all()
        return [self._to_entity(m) for m in models]

    def list_by_status(self, status: TaskStatus) -> List[Task]:
        """List tasks by status."""
        models = self.session.query(TaskModel).filter(TaskModel.status == status.value).all()
        return [self._to_entity(m) for m in models]

    def list_all(self) -> List[Task]:
        """List all tasks."""
        models = self.session.query(TaskModel).all()
        return [self._to_entity(m) for m in models]

    def update_status(self, task_id: int, status: TaskStatus) -> Optional[Task]:
        """Update task status."""
        model = self.session.query(TaskModel).filter(TaskModel.id == task_id).first()
        if model:
            model.status = status.value
            self.session.commit()
            self.session.refresh(model)
            return self._to_entity(model)
        return None

    def delete(self, task_id: int) -> bool:
        """Delete task by ID."""
        model = self.session.query(TaskModel).filter(TaskModel.id == task_id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False
