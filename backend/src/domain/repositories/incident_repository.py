"""Incident repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.incident import Incident
from ..enums.incident_status import IncidentStatus


class IncidentRepository(ABC):
    """Abstract repository interface for Incident entities."""

    @abstractmethod
    def find_by_id(self, incident_id: int) -> Optional[Incident]:
        """
        Find an incident by ID.

        Args:
            incident_id: The incident ID to search for

        Returns:
            Incident entity if found, None otherwise
        """
        pass

    @abstractmethod
    def save(self, incident: Incident) -> Incident:
        """
        Save an incident (create or update).

        Args:
            incident: The incident entity to save

        Returns:
            The saved incident entity with updated ID if newly created
        """
        pass

    @abstractmethod
    def list_all(self) -> List[Incident]:
        """
        List all incidents in the system.

        Returns:
            List of all incident entities
        """
        pass

    @abstractmethod
    def list_by_creator(self, user_id: int) -> List[Incident]:
        """
        List incidents created by a specific user.

        Args:
            user_id: The creator's user ID

        Returns:
            List of incident entities created by the user
        """
        pass

    @abstractmethod
    def list_by_assignee(self, user_id: int) -> List[Incident]:
        """
        List incidents assigned to a specific user.

        Args:
            user_id: The assignee's user ID

        Returns:
            List of incident entities assigned to the user
        """
        pass

    @abstractmethod
    def list_by_status(self, status: IncidentStatus) -> List[Incident]:
        """
        List incidents by status.

        Args:
            status: The incident status to filter by

        Returns:
            List of incident entities with the given status
        """
        pass

    @abstractmethod
    def update_status(self, incident_id: int, status: IncidentStatus) -> Optional[Incident]:
        """
        Update an incident's status.

        Args:
            incident_id: The incident ID
            status: The new status

        Returns:
            Updated incident entity if found, None otherwise
        """
        pass

    @abstractmethod
    def delete(self, incident_id: int) -> bool:
        """
        Delete an incident by ID.

        Args:
            incident_id: The incident ID to delete

        Returns:
            True if deleted, False if incident not found
        """
        pass
