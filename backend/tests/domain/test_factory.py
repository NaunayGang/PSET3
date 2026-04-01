"""Tests for Factory pattern."""

import pytest
from src.domain.patterns.factory import EntityFactory
from src.domain.enums.role import Role
from src.domain.enums.incident_severity import IncidentSeverity
from src.domain.enums.incident_status import IncidentStatus
from src.domain.enums.notification_channel import NotificationChannel
from src.domain.enums.notification_status import NotificationStatus
from src.domain.enums.event_type import EventType


class TestEntityFactory:
    """Test EntityFactory."""

    def test_create_user_valid(self):
        """Test creating valid user."""
        user = EntityFactory.create_user(
            id=1,
            name="John Doe",
            email="john@example.com",
            role=Role.ADMIN,
            hashed_password="hashed_pw",
        )
        
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.role == Role.ADMIN

    def test_create_user_invalid_email(self):
        """Test creating user with invalid email."""
        with pytest.raises(ValueError, match="Invalid email"):
            EntityFactory.create_user(
                id=1,
                name="John Doe",
                email="invalid_email",
                role=Role.ADMIN,
                hashed_password="hashed_pw",
            )

    def test_create_user_empty_name(self):
        """Test creating user with empty name."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            EntityFactory.create_user(
                id=1,
                name="",
                email="john@example.com",
                role=Role.ADMIN,
                hashed_password="hashed_pw",
            )

    def test_create_incident_valid(self):
        """Test creating valid incident."""
        incident = EntityFactory.create_incident(
            id=1,
            title="Test Incident",
            description="Test description",
            severity=IncidentSeverity.HIGH,
            status=IncidentStatus.OPEN,
            created_by=1,
        )
        
        assert incident.id == 1
        assert incident.title == "Test Incident"
        assert incident.severity == IncidentSeverity.HIGH

    def test_create_incident_empty_title(self):
        """Test creating incident with empty title."""
        with pytest.raises(ValueError, match="title cannot be empty"):
            EntityFactory.create_incident(
                id=1,
                title="",
                description="Test",
                severity=IncidentSeverity.HIGH,
                status=IncidentStatus.OPEN,
                created_by=1,
            )

    def test_create_notification_valid(self):
        """Test creating valid notification."""
        notification = EntityFactory.create_notification(
            id=1,
            recipient_id=1,
            channel=NotificationChannel.EMAIL,
            message="Test message",
            event_type=EventType.INCIDENT_CREATED,
        )
        
        assert notification.id == 1
        assert notification.recipient_id == 1
        assert notification.status == NotificationStatus.PENDING
