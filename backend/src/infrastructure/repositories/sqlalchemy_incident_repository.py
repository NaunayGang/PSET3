"""SQLAlchemy implementation of IncidentRepository."""

from typing import List, Optional
from sqlalchemy.orm import Session

from ...domain.entities.incident import Incident
from ...domain.enums.incident_severity import IncidentSeverity
from ...domain.enums.incident_status import IncidentStatus
from ...domain.repositories.incident_repository import IncidentRepository
from ..database.models.incident_model import IncidentModel


class SQLAlchemyIncidentRepository(IncidentRepository):
    """SQLAlchemy implementation of incident repository."""

    def __init__(self, session: Session):
        """
        Initialize repository with database session.

        Args:
            session: SQLAlchemy session
        """
        self.session = session

    def _to_entity(self, model: IncidentModel) -> Incident:
        """
        Convert ORM model to domain entity.

        Args:
            model: IncidentModel ORM instance

        Returns:
            Incident domain entity
        """
        return Incident(
            id=model.id,
            title=model.title,
            description=model.description,
            severity=IncidentSeverity(model.severity),
            status=IncidentStatus(model.status),
            created_by=model.created_by,
            assigned_to=model.assigned_to,
            created_at=model.created_at,
            updated_at=model.updated_at or model.created_at,
        )

    def _to_model(self, entity: Incident) -> IncidentModel:
        """
        Convert domain entity to ORM model.

        Args:
            entity: Incident domain entity

        Returns:
            IncidentModel ORM instance
        """
        return IncidentModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            severity=entity.severity.value,
            status=entity.status.value,
            created_by=entity.created_by,
            assigned_to=entity.assigned_to,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def find_by_id(self, incident_id: int) -> Optional[Incident]:
        """Find incident by ID."""
        model = self.session.query(IncidentModel).filter(IncidentModel.id == incident_id).first()
        return self._to_entity(model) if model else None

    def save(self, incident: Incident) -> Incident:
        """Save incident (create or update)."""
        if incident.id:
            # Update existing
            model = self.session.query(IncidentModel).filter(IncidentModel.id == incident.id).first()
            if model:
                model.title = incident.title
                model.description = incident.description
                model.severity = incident.severity.value
                model.status = incident.status.value
                model.created_by = incident.created_by
                model.assigned_to = incident.assigned_to
                model.updated_at = incident.updated_at
            else:
                raise ValueError(f"Incident with ID {incident.id} not found")
        else:
            # Create new
            model = self._to_model(incident)
            self.session.add(model)

        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def list_all(self) -> List[Incident]:
        """List all incidents."""
        models = self.session.query(IncidentModel).all()
        return [self._to_entity(m) for m in models]

    def list_by_creator(self, user_id: int) -> List[Incident]:
        """List incidents created by a user."""
        models = self.session.query(IncidentModel).filter(IncidentModel.created_by == user_id).all()
        return [self._to_entity(m) for m in models]

    def list_by_assignee(self, user_id: int) -> List[Incident]:
        """List incidents assigned to a user."""
        models = self.session.query(IncidentModel).filter(IncidentModel.assigned_to == user_id).all()
        return [self._to_entity(m) for m in models]

    def list_by_status(self, status: IncidentStatus) -> List[Incident]:
        """List incidents by status."""
        models = self.session.query(IncidentModel).filter(IncidentModel.status == status.value).all()
        return [self._to_entity(m) for m in models]

    def update_status(self, incident_id: int, status: IncidentStatus) -> Optional[Incident]:
        """Update incident status."""
        model = self.session.query(IncidentModel).filter(IncidentModel.id == incident_id).first()
        if model:
            model.status = status.value
            self.session.commit()
            self.session.refresh(model)
            return self._to_entity(model)
        return None

    def delete(self, incident_id: int) -> bool:
        """Delete incident by ID."""
        model = self.session.query(IncidentModel).filter(IncidentModel.id == incident_id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False
