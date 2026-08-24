from dataclasses import dataclass
from typing import Any
from odi.core.types import Intent, KnowledgeItem, Evidence

@dataclass(frozen=True)
class AssembledContext:
    intent: Intent
    knowledge: tuple[KnowledgeItem, ...]
    evidence: tuple[Evidence, ...]
    data: dict[str, Any]

class ContextEngine:
    def assemble(self, intent: Intent, knowledge: tuple[KnowledgeItem, ...] = (), evidence: tuple[Evidence, ...] = ()) -> AssembledContext:
        return AssembledContext(intent=intent, knowledge=knowledge, evidence=evidence, data={"objective": intent.objective, **dict(intent.constraints)})
