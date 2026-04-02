"""Task ORM model."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..base import Base


class TaskModel(Base):
    """SQLAlchemy ORM model for tasks table."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, index=True)  # TaskStatus values
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    incident = relationship("IncidentModel")
    assignee = relationship("UserModel")

    def __repr__(self) -> str:
        return f"<TaskModel(id={self.id}, title={self.title}, status={self.status})>"
