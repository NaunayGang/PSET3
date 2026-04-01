"""Observer pattern implementation for event-driven architecture.

The Observer pattern allows objects to subscribe to and receive notifications
about events that occur in the system.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from ..enums.event_type import EventType


@dataclass
class DomainEvent:
    """Event object carrying information about domain changes."""

    event_type: EventType
    data: Dict[str, Any]
    timestamp: datetime


class Observer(ABC):
    """Abstract observer that reacts to domain events."""

    @abstractmethod
    def update(self, event: DomainEvent) -> None:
        """
        React to a domain event.

        Args:
            event: The domain event to process
        """
        pass


class Subject(ABC):
    """Abstract subject (publisher) that notifies observers of events."""

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to receive event notifications.

        Args:
            observer: The observer to attach
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from receiving notifications.

        Args:
            observer: The observer to detach
        """
        pass

    @abstractmethod
    def notify(self, event: DomainEvent) -> None:
        """
        Notify all attached observers of an event.

        Args:
            event: The domain event to broadcast
        """
        pass
