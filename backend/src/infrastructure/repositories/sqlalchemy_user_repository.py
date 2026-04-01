"""SQLAlchemy implementation of UserRepository."""

from typing import List, Optional
from sqlalchemy.orm import Session

from ...domain.entities.user import User
from ...domain.enums.role import Role
from ...domain.repositories.user_repository import UserRepository
from ..database.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of user repository."""

    def __init__(self, session: Session):
        """
        Initialize repository with database session.

        Args:
            session: SQLAlchemy session
        """
        self.session = session

    def _to_entity(self, model: UserModel) -> User:
        """
        Convert ORM model to domain entity.

        Args:
            model: UserModel ORM instance

        Returns:
            User domain entity
        """
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            role=Role(model.role),
            hashed_password=model.hashed_password,
            created_at=model.created_at,
        )

    def _to_model(self, entity: User) -> UserModel:
        """
        Convert domain entity to ORM model.

        Args:
            entity: User domain entity

        Returns:
            UserModel ORM instance
        """
        return UserModel(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            role=entity.role.value,
            hashed_password=entity.hashed_password,
            created_at=entity.created_at,
        )

    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find user by ID."""
        model = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(model) if model else None

    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email."""
        model = self.session.query(UserModel).filter(UserModel.email == email.lower()).first()
        return self._to_entity(model) if model else None

    def save(self, user: User) -> User:
        """Save user (create or update)."""
        if user.id:
            # Update existing user
            model = self.session.query(UserModel).filter(UserModel.id == user.id).first()
            if model:
                model.name = user.name
                model.email = user.email.lower()
                model.role = user.role.value
                model.hashed_password = user.hashed_password
            else:
                raise ValueError(f"User with ID {user.id} not found")
        else:
            # Create new user
            model = self._to_model(user)
            self.session.add(model)

        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def list_all(self) -> List[User]:
        """List all users."""
        models = self.session.query(UserModel).all()
        return [self._to_entity(model) for model in models]

    def delete(self, user_id: int) -> bool:
        """Delete user by ID."""
        model = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False
