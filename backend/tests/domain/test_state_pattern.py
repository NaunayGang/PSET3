"""Tests for State pattern (incident lifecycle)."""

import pytest
from src.domain.patterns.state import IncidentStateMachine
from src.domain.enums.incident_status import IncidentStatus


class TestIncidentStateMachine:
    """Test IncidentStateMachine."""

    def test_valid_transition_open_to_assigned(self):
        """Test valid transition from OPEN to ASSIGNED."""
        machine = IncidentStateMachine(IncidentStatus.OPEN)
        assert machine.can_transition_to(IncidentStatus.ASSIGNED) is True
        machine.transition_to(IncidentStatus.ASSIGNED)
        assert machine.current_state == IncidentStatus.ASSIGNED

    def test_valid_transition_assigned_to_in_progress(self):
        """Test valid transition from ASSIGNED to IN_PROGRESS."""
        machine = IncidentStateMachine(IncidentStatus.ASSIGNED)
        assert machine.can_transition_to(IncidentStatus.IN_PROGRESS) is True
        machine.transition_to(IncidentStatus.IN_PROGRESS)
        assert machine.current_state == IncidentStatus.IN_PROGRESS

    def test_invalid_transition_open_to_closed(self):
        """Test invalid direct transition from OPEN to CLOSED."""
        machine = IncidentStateMachine(IncidentStatus.OPEN)
        assert machine.can_transition_to(IncidentStatus.CLOSED) is False

    def test_backward_transition_assigned_to_open(self):
        """Test backward transition from ASSIGNED to OPEN."""
        machine = IncidentStateMachine(IncidentStatus.ASSIGNED)
        assert machine.can_transition_to(IncidentStatus.OPEN) is True
        machine.transition_to(IncidentStatus.OPEN)
        assert machine.current_state == IncidentStatus.OPEN

    def test_transition_raises_on_invalid(self):
        """Test that invalid transition raises exception."""
        machine = IncidentStateMachine(IncidentStatus.OPEN)
        with pytest.raises(ValueError):
            machine.transition_to(IncidentStatus.CLOSED)

    def test_closed_state_no_transitions(self):
        """Test that CLOSED state prevents transitions."""
        machine = IncidentStateMachine(IncidentStatus.CLOSED)
        assert machine.can_transition_to(IncidentStatus.OPEN) is False
        assert machine.can_transition_to(IncidentStatus.RESOLVED) is False
