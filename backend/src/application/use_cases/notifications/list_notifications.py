"""List notifications use case."""

from typing import List
from ....domain.entities.notification import Notification
from ....domain.repositories.notification_repository import NotificationRepository
from ....domain.entities.user import User


class ListNotificationsUseCase:
    """Use case for listing user notifications."""

    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository

    def execute(self, user: User) -> List[Notification]:
        """List notifications for current user."""
        return self.notification_repository.list_by_recipient(user.id)
