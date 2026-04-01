"""Event bus implementation of Observer pattern.

This is the concrete Subject that publishes domain events to observers.
Implements the Observer pattern from the domain layer.
"""

from ..domain.patterns.observer import Observer, Subject, DomainEvent
from ...domain.enums.event_type import EventType
from typing import List


class EventBus(Subject):
    """
    Event bus singleton for publishing and subscribing to domain events.

    Implements the Subject interface from the Observer pattern.
    Uses singleton pattern to provide a global event bus.
    """

    _instance = None

    def __new__(cls) -> "EventBus":
        """Ensure singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.observers: List[Observer] = []
        return cls._instance

    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to receive events.

        Args:
            observer: Observer to attach
        """
        if observer not in self.observers:
            self.observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """
        Detach an observer.

        Args:
            observer: Observer to detach
        """
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self, event: DomainEvent) -> None:
        """
        Notify all attached observers of an event.

        Args:
            event: Domain event to broadcast
        """
        for observer in self.observers:
            observer.update(event)

    def publish(self, event_type: EventType, data: dict) -> None:
        """
        Publish an event with given type and data.

        Convenience method that creates a DomainEvent and notifies observers.

        Args:
            event_type: Type of event
            data: Event payload data
        """
        import datetime
        event = DomainEvent(
            event_type=event_type,
            data=data,
            timestamp=datetime.datetime.now()
        )
        self.notify(event)
