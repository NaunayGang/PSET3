"""User repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.user import User


class UserRepository(ABC):
    """Abstract repository interface for User entities."""

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """
        Find a user by ID.

        Args:
            user_id: The user ID to search for

        Returns:
            User entity if found, None otherwise
        """
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """
        Find a user by email address.

        Args:
            email: The email address to search for

        Returns:
            User entity if found, None otherwise
        """
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        """
        Save a user (create or update).

        Args:
            user: The user entity to save

        Returns:
            The saved user entity with updated ID if newly created
        """
        pass

    @abstractmethod
    def list_all(self) -> List[User]:
        """
        List all users in the system.

        Returns:
            List of all user entities
        """
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """
        Delete a user by ID.

        Args:
            user_id: The user ID to delete

        Returns:
            True if deleted, False if user not found
        """
        pass
