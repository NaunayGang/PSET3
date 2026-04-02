"""Shared pytest fixtures."""

import pytest
from src.domain.enums.role import Role
from src.domain.entities.user import User


@pytest.fixture
def admin_user():
    """Create test admin user."""
    return User(
        id=1,
        name="Admin User",
        email="admin@test.com",
        role=Role.ADMIN,
        hashed_password="hashed_pw",
        created_at=None,
    )


@pytest.fixture
def supervisor_user():
    """Create test supervisor user."""
    return User(
        id=2,
        name="Supervisor User",
        email="supervisor@test.com",
        role=Role.SUPERVISOR,
        hashed_password="hashed_pw",
        created_at=None,
    )


@pytest.fixture
def operator_user():
    """Create test operator user."""
    return User(
        id=3,
        name="Operator User",
        email="operator@test.com",
        role=Role.OPERATOR,
        hashed_password="hashed_pw",
        created_at=None,
    )
