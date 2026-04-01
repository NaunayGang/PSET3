"""Tests for Template Method pattern (notification builders)."""

import pytest
from src.domain.patterns.template_method import (
    IncidentCreatedNotificationBuilder,
    IncidentAssignedNotificationBuilder,
    IncidentStatusChangedNotificationBuilder,
)


class TestNotificationBuilders:
    """Test notification builder implementations."""

    def test_incident_created_builder(self):
        """Test IncidentCreatedNotificationBuilder."""
        data = {
            "id": 1,
            "title": "Database Outage",
            "severity": "HIGH",
            "creator_name": "Alice",
        }
        builder = IncidentCreatedNotificationBuilder(data)
        
        notification = builder.build_notification()
        assert "Database Outage" in notification
        assert "HIGH" in notification
        
        subject = builder.build_subject()
        assert "Database Outage" in subject

    def test_incident_assigned_builder(self):
        """Test IncidentAssignedNotificationBuilder."""
        incident_data = {
            "id": 1,
            "title": "Server Down",
            "severity": "CRITICAL",
        }
        builder = IncidentAssignedNotificationBuilder(
            incident_data=incident_data,
            assigner_name="Bob",
        )
        
        notification = builder.build_notification()
        assert "Incident Assigned" in notification
        assert "Bob" in notification
        assert "Server Down" in notification

    def test_incident_status_changed_builder(self):
        """Test IncidentStatusChangedNotificationBuilder."""
        incident_data = {
            "id": 1,
            "title": "Network Latency",
        }
        builder = IncidentStatusChangedNotificationBuilder(
            incident_data=incident_data,
            new_status="IN_PROGRESS",
            changed_by_name="Charlie",
        )
        
        notification = builder.build_notification()
        assert "Status Updated" in notification
        assert "IN_PROGRESS" in notification
        assert "Charlie" in notification

    def test_builder_has_header_body_footer(self):
        """Test that all builders follow template method."""
        data = {"id": 1, "title": "Test"}
        builder = IncidentCreatedNotificationBuilder(data)
        
        header = builder.build_header()
        body = builder.build_body()
        footer = builder.build_footer()
        subject = builder.build_subject()
        
        assert header
        assert body
        assert footer
        assert subject
        assert "\n" in builder.build_notification()
