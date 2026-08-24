"""Canonical cross-layer types used by ODI."""
from dataclasses import dataclass, field
from typing import Any, Mapping
from uuid import uuid4

@dataclass(frozen=True)
class Intent:
    objective: str
    constraints: Mapping[str, Any] = field(default_factory=dict)
    preferences: Mapping[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: f"intent-{uuid4().hex}")

@dataclass(frozen=True)
class Evidence:
    id: str
    source: str
    kind: str
    content: Any
    confidence: float = 1.0
    provenance: Mapping[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class KnowledgeItem:
    id: str
    topic: str
    content: Any
    source_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class PlanStep:
    id: str
    capability_id: str
    objective: str
    dependencies: tuple[str, ...] = ()
    inputs: Mapping[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class Plan:
    id: str
    steps: tuple[PlanStep, ...]
    rationale: str = ""

@dataclass(frozen=True)
class ValidationResult:
    passed: bool
    score: float
    checks: Mapping[str, bool] = field(default_factory=dict)
    findings: tuple[str, ...] = ()

@dataclass(frozen=True)
class ExecutionResult:
    execution_id: str
    status: str
    output: Any = None
    evidence_ids: tuple[str, ...] = ()
    telemetry: Mapping[str, Any] = field(default_factory=dict)
