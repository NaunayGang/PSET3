"""List incidents use case."""

from typing import List

from ....domain.entities.incident import Incident
from ....domain.repositories.incident_repository import IncidentRepository
from ....domain.enums.role import Role
from ....domain.entities.user import User


class ListIncidentsUseCase:
    """Use case for listing incidents with role-based filtering."""

    def __init__(self, incident_repository: IncidentRepository):
        """
        Initialize use case.

        Args:
            incident_repository: Incident repository
        """
        self.incident_repository = incident_repository

    def execute(self, user: User) -> List[Incident]:
        """
        List incidents based on user role.

        Args:
            user: Current user (determines what they can see)

        Returns:
            List of incidents
        """
        if user.role == Role.ADMIN or user.role == Role.SUPERVISOR:
            # Admin and Supervisor see all incidents
            return self.incident_repository.list_all()
        else:
            # Operator sees only their own or assigned incidents
            created = self.incident_repository.list_by_creator(user.id)
            assigned = self.incident_repository.list_by_assignee(user.id)
            # Combine and deduplicate (by ID)
            all_incidents = created + assigned
            seen = set()
            unique = []
            for inc in all_incidents:
                if inc.id not in seen:
                    seen.add(inc.id)
                    unique.append(inc)
            return unique
