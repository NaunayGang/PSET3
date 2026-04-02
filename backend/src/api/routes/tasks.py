"""Task management routes."""

from typing import Annotated
from fastapi import APIRouter, Depends, Query, HTTPException, status

from ...application.dtos.task_dto import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
    TaskStatusUpdate,
)
from ...application.use_cases.tasks.create_task import CreateTaskUseCase
from ...application.use_cases.tasks.update_task import UpdateTaskUseCase
from ...application.use_cases.tasks.list_tasks import ListTasksUseCase
from ...domain.repositories.task_repository import TaskRepository
from ...domain.repositories.incident_repository import IncidentRepository
from ...domain.repositories.user_repository import UserRepository
from ...domain.entities.user import User
from ...domain.exceptions import EntityNotFoundError, PermissionDeniedError
from ..dependencies import (
    get_task_repository,
    get_incident_repository,
    get_user_repository,
    get_current_user,
)

router = APIRouter()


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    current_user: Annotated[User, Depends(get_current_user)],
    task_repo: Annotated[TaskRepository, Depends(get_task_repository)],
    incident_id: Annotated[int | None, Query(None, description="Filter tasks by incident ID")] = None,
):
    """
    List tasks with role-based filtering.

    - ADMIN/SUPERVISOR: see all tasks (or filtered by incident)
    - OPERATOR: see only tasks assigned to them (optionally filtered by incident)
    """
    use_case = ListTasksUseCase(task_repo)
    return use_case.execute(current_user, incident_id=incident_id)


@router.post("", response_model=TaskResponse)
def create_task(
    data: TaskCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    task_repo: Annotated[TaskRepository, Depends(get_task_repository)],
    incident_repo: Annotated[IncidentRepository, Depends(get_incident_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
):
    """
    Create a new task linked to an incident.

    Any authenticated user can create tasks (subject to incident access).
    Operators can only create tasks for incidents they own or are assigned to.
    """
    use_case = CreateTaskUseCase(task_repo, incident_repo, user_repo)
    try:
        return use_case.execute(data, creator_id=current_user.id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    updates: TaskUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    task_repo: Annotated[TaskRepository, Depends(get_task_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
):
    """
    Update a task (status, assignment, title, description).

    - Assigned users can update status and their own tasks
    - ADMIN/SUPERVISOR can update any task and reassign
    """
    use_case = UpdateTaskUseCase(task_repo, user_repo)
    try:
        return use_case.execute(task_id, updates, user_id=current_user.id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    status_update: TaskStatusUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    task_repo: Annotated[TaskRepository, Depends(get_task_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
):
    """
    Update task status.

    Convenience endpoint specifically for status updates.
    """
    # Reuse update_task with only status field
    updates = TaskUpdate(status=status_update.status)
    use_case = UpdateTaskUseCase(task_repo, user_repo)
    try:
        return use_case.execute(task_id, updates, user_id=current_user.id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
