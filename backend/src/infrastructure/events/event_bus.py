"""EventBus implementation for domain event publishing.

The Observer pattern: EventBus maintains list of observers and notifies them
when domain events occur.
"""

from typing import List
import logging

from ...domain.patterns.observer import Observer, DomainEvent

logger = logging.getLogger(__name__)


class EventBus:
    """
    Central event bus for publishing domain events.

    Implements the Observer pattern where observers register to receive
    notifications of domain events.
    """

    def __init__(self):
        """Initialize event bus with empty observer list."""
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """
        Register an observer.

        Args:
            observer: Observer to register
        """
        if observer not in self._observers:
            self._observers.append(observer)
            logger.debug(f"Attached observer: {observer.__class__.__name__}")

    def detach(self, observer: Observer) -> None:
        """
        Unregister an observer.

        Args:
            observer: Observer to remove
        """
        if observer in self._observers:
            self._observers.remove(observer)
            logger.debug(f"Detached observer: {observer.__class__.__name__}")

    def publish(self, event: DomainEvent) -> None:
        """
        Publish a domain event to all observers.

        Args:
            event: The domain event to publish
        """
        logger.info(f"Publishing event: {event.event_type}")
        for observer in self._observers:
            observer.update(event)
