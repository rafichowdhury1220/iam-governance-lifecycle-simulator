"""
Lifecycle event handlers and event management
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Callable, List, Optional


class EventType(str, Enum):
    """Types of lifecycle events"""
    JOINER = "joiner"
    MOVER = "mover"
    LEAVER = "leaver"


@dataclass
class LifecycleEvent:
    """Represents a lifecycle event"""
    event_type: EventType
    employee_id: str
    employee_name: str
    timestamp: datetime
    details: dict
    processed: bool = False


class EventManager:
    """Manage lifecycle events and handlers"""

    def __init__(self):
        self.events: List[LifecycleEvent] = []
        self.handlers: dict = {
            EventType.JOINER: [],
            EventType.MOVER: [],
            EventType.LEAVER: []
        }

    def register_handler(self, event_type: EventType, handler: Callable) -> None:
        """Register a handler for an event type"""
        self.handlers[event_type].append(handler)

    def emit_event(self, event: LifecycleEvent) -> None:
        """Emit an event and process with registered handlers"""
        self.events.append(event)
        
        for handler in self.handlers[event.event_type]:
            try:
                handler(event)
                event.processed = True
            except Exception as e:
                print(f"Error processing event: {e}")

    def create_joiner_event(self, employee_id: str, employee_name: str, details: dict) -> LifecycleEvent:
        """Create a joiner event"""
        event = LifecycleEvent(
            event_type=EventType.JOINER,
            employee_id=employee_id,
            employee_name=employee_name,
            timestamp=datetime.now(),
            details=details
        )
        self.emit_event(event)
        return event

    def create_mover_event(self, employee_id: str, employee_name: str, details: dict) -> LifecycleEvent:
        """Create a mover event"""
        event = LifecycleEvent(
            event_type=EventType.MOVER,
            employee_id=employee_id,
            employee_name=employee_name,
            timestamp=datetime.now(),
            details=details
        )
        self.emit_event(event)
        return event

    def create_leaver_event(self, employee_id: str, employee_name: str, details: dict = None) -> LifecycleEvent:
        """Create a leaver event"""
        event = LifecycleEvent(
            event_type=EventType.LEAVER,
            employee_id=employee_id,
            employee_name=employee_name,
            timestamp=datetime.now(),
            details=details or {}
        )
        self.emit_event(event)
        return event

    def get_events_for_employee(self, employee_id: str) -> List[LifecycleEvent]:
        """Get all events for a specific employee"""
        return [event for event in self.events if event.employee_id == employee_id]

    def get_event_history(self) -> List[LifecycleEvent]:
        """Get all events in chronological order"""
        return sorted(self.events, key=lambda e: e.timestamp)
