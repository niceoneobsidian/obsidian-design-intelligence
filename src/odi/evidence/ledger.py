from dataclasses import dataclass
from odi.core.types import Evidence

@dataclass(frozen=True)
class EvidenceRecord:
    evidence: Evidence
    execution_id: str | None = None
    decision_id: str | None = None

class EvidenceLedger:
    def __init__(self) -> None:
        self._records: dict[str, EvidenceRecord] = {}

    def record(self, record: EvidenceRecord) -> None:
        self._records[record.evidence.id] = record

    def get(self, evidence_id: str) -> EvidenceRecord:
        return self._records[evidence_id]

    def for_execution(self, execution_id: str) -> tuple[EvidenceRecord, ...]:
        return tuple(r for r in self._records.values() if r.execution_id == execution_id)
