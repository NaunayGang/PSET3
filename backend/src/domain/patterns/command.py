"""Command pattern implementation for encapsulating actions.

The Command pattern encapsulates a request as an object, allowing you to
parameterize clients with different requests, queue or log requests, and
support undoable operations.
"""

from abc import ABC, abstractmethod


class Command(ABC):
    """Abstract command interface."""

    @abstractmethod
    def execute(self) -> None:
        """
        Execute the command action.

        This method should contain all the logic needed to perform the action.
        """
        pass
