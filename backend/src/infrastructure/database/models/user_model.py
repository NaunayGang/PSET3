"""User ORM model."""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from ..base import Base


class UserModel(Base):
    """SQLAlchemy ORM model for users table."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    role = Column(String(50), nullable=False)  # ADMIN, SUPERVISOR, OPERATOR
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<UserModel(id={self.id}, email={self.email}, role={self.role})>"
