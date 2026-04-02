"""Notification management routes."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from ...application.dtos.notification_dto import (
    NotificationResponse,
    NotificationStatusUpdate,
)
from ...application.use_cases.notifications.list_notifications import ListNotificationsUseCase
from ...domain.repositories.notification_repository import NotificationRepository
from ...domain.entities.user import User
from ...domain.enums.notification_status import NotificationStatus
from ..dependencies import get_notification_repository, get_current_user

router = APIRouter()


@router.get("", response_model=list[NotificationResponse])
def list_notifications(
    current_user: Annotated[User, Depends(get_current_user)],
    notification_repo: Annotated[NotificationRepository, Depends(get_notification_repository)],
):
    """List notifications for current user."""
    use_case = ListNotificationsUseCase(notification_repo)
    return use_case.execute(current_user)


@router.patch("/{notification_id}/status", response_model=NotificationResponse)
def mark_notification(
    notification_id: int,
    status_update: NotificationStatusUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    notification_repo: Annotated[NotificationRepository, Depends(get_notification_repository)],
):
    """Mark notification as read/acknowledged."""
    notification = notification_repo.find_by_id(notification_id)
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    
    if notification.recipient_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot access other user's notification")
    
    updated = notification_repo.update_status(notification_id, status_update.status)
    if not updated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not update notification")
    
    return updated
