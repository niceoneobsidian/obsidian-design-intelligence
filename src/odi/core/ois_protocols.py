"""Provider-neutral protocols for integrating ODI with the OIS substrate.

ODI intentionally depends on contracts, not on a copied OIS implementation.
"""

from dataclasses import dataclass, field
from typing import Any, Protocol, Sequence

from .contracts import ExecutionContext


@dataclass(frozen=True)
class PolicyDecision:
    """Authorization result returned by the governing substrate."""

    allowed: bool
    reason: str = ""
    required_approvals: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExecutionRequest:
    """Normalized request handed from ODI to an execution provider."""

    capability_id: str
    execution: ExecutionContext
    inputs: dict[str, Any] = field(default_factory=dict)
    idempotency_key: str | None = None


@dataclass(frozen=True)
class ExecutionResult:
    """Normalized provider result; validation decides whether it is accepted."""

    status: str
    outputs: dict[str, Any] = field(default_factory=dict)
    evidence_ids: tuple[str, ...] = ()
    trace_id: str | None = None
    error: str | None = None


class OISPolicyPort(Protocol):
    """Policy boundary. ODI cannot authorize its own consequential actions."""

    def authorize(self, request: ExecutionRequest) -> PolicyDecision:
        ...


class OISExecutionPort(Protocol):
    """Execution boundary supplied by OIS or another conforming runtime."""

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        ...


class OISEvidencePort(Protocol):
    """Evidence/provenance boundary."""

    def record(self, execution: ExecutionRequest, result: ExecutionResult) -> Sequence[str]:
        ...


class OISValidationPort(Protocol):
    """Post-execution validation boundary."""

    def validate(self, request: ExecutionRequest, result: ExecutionResult) -> bool:
        ...
