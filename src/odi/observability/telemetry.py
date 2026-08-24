from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

@dataclass(frozen=True)
class TelemetryEvent:
    name: str
    execution_id: str | None = None
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class TelemetrySink:
    def __init__(self) -> None:
        self.events: list[TelemetryEvent] = []

    def emit(self, event: TelemetryEvent) -> None:
        self.events.append(event)
