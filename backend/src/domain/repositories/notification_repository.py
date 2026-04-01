"""Notification repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.notification import Notification
from ..enums.notification_status import NotificationStatus


class NotificationRepository(ABC):
    """Abstract repository interface for Notification entities."""

    @abstractmethod
    def find_by_id(self, notification_id: int) -> Optional[Notification]:
        """
        Find a notification by ID.

        Args:
            notification_id: The notification ID to search for

        Returns:
            Notification entity if found, None otherwise
        """
        pass

    @abstractmethod
    def save(self, notification: Notification) -> Notification:
        """
        Save a notification (create or update).

        Args:
            notification: The notification entity to save

        Returns:
            The saved notification entity with updated ID if newly created
        """
        pass

    @abstractmethod
    def list_by_recipient(self, user_id: int) -> List[Notification]:
        """
        List notifications for a specific recipient.

        Args:
            user_id: The recipient's user ID

        Returns:
            List of notification entities for the recipient
        """
        pass

    @abstractmethod
    def list_by_status(self, status: NotificationStatus) -> List[Notification]:
        """
        List notifications by status.

        Args:
            status: The notification status to filter by

        Returns:
            List of notification entities with the given status
        """
        pass

    @abstractmethod
    def update_status(self, notification_id: int, status: NotificationStatus) -> Optional[Notification]:
        """
        Update a notification's status.

        Args:
            notification_id: The notification ID
            status: The new status

        Returns:
            Updated notification entity if found, None otherwise
        """
        pass

    @abstractmethod
    def delete(self, notification_id: int) -> bool:
        """
        Delete a notification by ID.

        Args:
            notification_id: The notification ID to delete

        Returns:
            True if deleted, False if notification not found
        """
        pass
