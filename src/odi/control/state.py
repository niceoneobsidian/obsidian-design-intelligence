"""Task/workflow execution state integrated from the OIS kernel model."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Mapping
from uuid import uuid4

from odi.core.contracts import ExecutionContext


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(frozen=True)
class ExecutionIdentity:
    execution_id: str = field(default_factory=lambda: str(uuid4()))
    tenant_id: str = "default"
    workflow_id: str | None = None
    workflow_version: str | None = None


@dataclass
class WorkflowState:
    """Complete task/workflow state carried across orchestration boundaries."""

    identity: ExecutionIdentity
    objective: str
    workflow: Mapping[str, Any] | None = None
    plan: Mapping[str, Any] | None = None
    execution: ExecutionContext | None = None
    outputs: list[Mapping[str, Any]] = field(default_factory=list)
    evidence: list[Mapping[str, Any]] = field(default_factory=list)
    validation: list[Mapping[str, Any]] = field(default_factory=list)
    recovery: list[Mapping[str, Any]] = field(default_factory=list)
    governance: list[Mapping[str, Any]] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    memory: dict[str, Any] = field(default_factory=dict)
    checkpoint_id: str | None = None
    status: str = "received"
    retry_count: int = 0
    recovery_attempts: int = 0
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def touch(self) -> None:
        self.updated_at = utc_now()

    def transition(self, status: str) -> None:
        if self.status in {"completed", "stopped", "escalated"}:
            raise ValueError(f"Terminal workflow state cannot transition: {self.status}")
        self.status = status
        self.touch()

    def snapshot(self) -> dict[str, Any]:
        return {
            "identity": {
                "execution_id": self.identity.execution_id,
                "tenant_id": self.identity.tenant_id,
                "workflow_id": self.identity.workflow_id,
                "workflow_version": self.identity.workflow_version,
            },
            "objective": self.objective,
            "workflow": dict(self.workflow or {}),
            "plan": dict(self.plan or {}),
            "outputs": list(self.outputs),
            "evidence": list(self.evidence),
            "validation": list(self.validation),
            "recovery": list(self.recovery),
            "governance": list(self.governance),
            "metrics": dict(self.metrics),
            "memory": dict(self.memory),
            "checkpoint_id": self.checkpoint_id,
            "status": self.status,
            "retry_count": self.retry_count,
            "recovery_attempts": self.recovery_attempts,
            "updated_at": self.updated_at.isoformat(),
        }
