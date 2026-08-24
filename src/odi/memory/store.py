from dataclasses import dataclass, field
from typing import Any

@dataclass
class MemoryRecord:
    id: str
    scope: str
    content: Any
    metadata: dict[str, Any] = field(default_factory=dict)

class MemoryStore:
    """Explicit memory boundary; memory is state, not curated knowledge."""
    def __init__(self) -> None:
        self._records: dict[str, MemoryRecord] = {}

    def put(self, record: MemoryRecord) -> None:
        self._records[record.id] = record

    def get(self, record_id: str) -> MemoryRecord:
        return self._records[record_id]

    def by_scope(self, scope: str) -> tuple[MemoryRecord, ...]:
        return tuple(r for r in self._records.values() if r.scope == scope)
