"""Incident ORM model."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..base import Base


class IncidentModel(Base):
    """SQLAlchemy ORM model for incidents table."""

    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    severity = Column(String(50), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(50), nullable=False, index=True)  # IncidentStatus values
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    creator = relationship("UserModel", foreign_keys=[created_by])
    assignee = relationship("UserModel", foreign_keys=[assigned_to])

    def __repr__(self) -> str:
        return f"<IncidentModel(id={self.id}, title={self.title}, status={self.status})>"
