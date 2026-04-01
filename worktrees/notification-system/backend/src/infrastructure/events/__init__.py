"""Event system infrastructure."""

from .event_bus import EventBus
from .setup import initialize_event_system

__all__ = ["EventBus", "initialize_event_system"]
