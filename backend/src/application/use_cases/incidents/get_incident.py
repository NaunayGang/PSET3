"""Get incident by ID use case."""

from typing import Optional

from ....domain.entities.incident import Incident
from ....domain.repositories.incident_repository import IncidentRepository
from ....domain.entities.user import User
from ....domain.enums.role import Role


class GetIncidentUseCase:
    """Use case for retrieving a single incident by ID."""

    def __init__(self, incident_repository: IncidentRepository):
        """
        Initialize use case.

        Args:
            incident_repository: Incident repository
        """
        self.incident_repository = incident_repository

    def execute(self, incident_id: int, user: User) -> Optional[Incident]:
        """
        Get incident by ID with role-based access check.

        Args:
            incident_id: ID of incident to retrieve
            user: Current user (for access control)

        Returns:
            Incident if accessible, None if not found or no access
        """
        incident = self.incident_repository.find_by_id(incident_id)
        if not incident:
            return None

        # Role-based access control
        if user.role in [Role.ADMIN, Role.SUPERVISOR]:
            # Admin and Supervisor can see any incident
            return incident
        else:
            # Operator can only see incidents they created or are assigned to
            if incident.created_by == user.id or incident.assigned_to == user.id:
                return incident
            return None
