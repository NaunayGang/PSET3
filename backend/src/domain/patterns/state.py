"""State pattern implementation for incident lifecycle management.

The State pattern allows an object to alter its behavior when its internal
state changes. Used here to manage incident status transitions.
"""

from abc import ABC, abstractmethod
from typing import List, Type

from ..enums.incident_status import IncidentStatus


class IncidentState(ABC):
    """Abstract state for incident lifecycle."""

    @abstractmethod
    def get_allowed_transitions(self) -> List[Type["IncidentState"]]:
        """
        Get list of allowed state transitions from this state.

        Returns:
            List of state classes that can be transitioned to
        """
        pass

    @abstractmethod
    def get_status(self) -> IncidentStatus:
        """
        Get the IncidentStatus enum value for this state.

        Returns:
            The incident status enum value
        """
        pass

    def can_transition_to(self, target_state: Type["IncidentState"]) -> bool:
        """
        Check if transition to target state is allowed.

        Args:
            target_state: The state class to transition to

        Returns:
            True if transition is allowed, False otherwise
        """
        return target_state in self.get_allowed_transitions()


class OpenState(IncidentState):
    """Incident is newly created and not yet assigned."""

    def get_allowed_transitions(self) -> List[Type[IncidentState]]:
        return [AssignedState]

    def get_status(self) -> IncidentStatus:
        return IncidentStatus.OPEN


class AssignedState(IncidentState):
    """Incident has been assigned to a user."""

    def get_allowed_transitions(self) -> List[Type[IncidentState]]:
        return [OpenState, InProgressState]

    def get_status(self) -> IncidentStatus:
        return IncidentStatus.ASSIGNED


class InProgressState(IncidentState):
    """Incident is being actively worked on."""

    def get_allowed_transitions(self) -> List[Type[IncidentState]]:
        return [AssignedState, ResolvedState]

    def get_status(self) -> IncidentStatus:
        return IncidentStatus.IN_PROGRESS


class ResolvedState(IncidentState):
    """Incident has been resolved but not yet closed."""

    def get_allowed_transitions(self) -> List[Type[IncidentState]]:
        return [InProgressState, ClosedState]

    def get_status(self) -> IncidentStatus:
        return IncidentStatus.RESOLVED


class ClosedState(IncidentState):
    """Incident is closed and cannot be reopened."""

    def get_allowed_transitions(self) -> List[Type[IncidentState]]:
        return []  # No transitions from closed state

    def get_status(self) -> IncidentStatus:
        return IncidentStatus.CLOSED


class IncidentStateMachine:
    """State machine for managing incident status transitions."""

    # Map status enum to state class
    _state_map = {
        IncidentStatus.OPEN: OpenState,
        IncidentStatus.ASSIGNED: AssignedState,
        IncidentStatus.IN_PROGRESS: InProgressState,
        IncidentStatus.RESOLVED: ResolvedState,
        IncidentStatus.CLOSED: ClosedState,
    }

    def __init__(self, initial_status: IncidentStatus = IncidentStatus.OPEN):
        """Initialize machine with current incident state."""
        self.current_state = initial_status

    def can_transition_to(self, target_status: IncidentStatus) -> bool:
        """Check if transition from current state to target is allowed."""
        return self.can_transition(self.current_state, target_status)

    def transition_to(self, target_status: IncidentStatus) -> None:
        """Transition to target state if valid; otherwise raise error."""
        if not self.can_transition_to(target_status):
            raise ValueError(
                f"Invalid state transition: {self.current_state.value} -> {target_status.value}"
            )
        self.current_state = target_status

    def can_transition(
        self, current_status: IncidentStatus, target_status: IncidentStatus
    ) -> bool:
        """Check if transition from current to target status is allowed."""
        # Allow staying in same state
        if current_status == target_status:
            return True

        current_state_class = self._state_map[current_status]
        target_state_class = self._state_map[target_status]

        current_state = current_state_class()
        return current_state.can_transition_to(target_state_class)

    def get_allowed_transitions(self, current_status: IncidentStatus) -> List[IncidentStatus]:
        """Get list of allowed status transitions from current status."""
        current_state_class = self._state_map[current_status]
        current_state = current_state_class()
        allowed_state_classes = current_state.get_allowed_transitions()

        return [state_class().get_status() for state_class in allowed_state_classes]
