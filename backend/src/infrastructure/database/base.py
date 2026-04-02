"""SQLAlchemy declarative base and model imports.

All ORM models must be imported here so Alembic can detect them.
"""

from sqlalchemy.ext.declarative import declarative_base

# Create declarative base
Base = declarative_base()

# Import all models so Alembic can detect them
from .models.user_model import UserModel  # noqa: F401, E402

__all__ = ["Base"]
