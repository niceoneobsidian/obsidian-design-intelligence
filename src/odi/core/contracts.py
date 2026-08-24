"""Stable domain contracts for Obsidian Design Intelligence."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class LifecycleState(StrEnum):
    DRAFT = "draft"
    DESIGNED = "designed"
    IMPLEMENTED = "implemented"
    TESTED = "tested"
    INTEGRATED = "integrated"
    DEPLOYED = "deployed"
    ACTIVATED = "activated"
    PRODUCTION_VERIFIED = "production_verified"
    DEPRECATED = "deprecated"


class RiskClass(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class CapabilityContract:
    """Stable interface between intent and an execution provider."""

    id: str
    name: str
    version: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    risk_class: RiskClass = RiskClass.LOW
    permissions: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    validation_requirements: tuple[str, ...] = ()
    evidence_requirements: tuple[str, ...] = ()
    lifecycle_state: LifecycleState = LifecycleState.DRAFT


@dataclass
class ExecutionContext:
    """Task-scoped context assembled before capability execution."""

    execution_id: str
    task_id: str
    objective: str
    context: dict[str, Any] = field(default_factory=dict)
    evidence_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
