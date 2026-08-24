"""Deterministic policy and approval controls.

Derived from the Niceone Obsidian kernel policy contract and adapted to ODI's
CapabilityContract/ExecutionContext types.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable

from odi.core.contracts import CapabilityContract, ExecutionContext, RiskClass


class PolicyDecision(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"


@dataclass(frozen=True)
class PolicyResult:
    decision: PolicyDecision
    reasons: tuple[str, ...] = ()

    @property
    def allowed(self) -> bool:
        return self.decision is not PolicyDecision.DENY


class ApprovalMatrix:
    """Maps risk classes to approval requirements."""

    def __init__(self, *, high_requires_approval: bool = True, critical_requires_approval: bool = True) -> None:
        self.high_requires_approval = high_requires_approval
        self.critical_requires_approval = critical_requires_approval

    def requires_approval(self, risk: RiskClass) -> bool:
        return (
            (risk is RiskClass.HIGH and self.high_requires_approval)
            or (risk is RiskClass.CRITICAL and self.critical_requires_approval)
        )


class PolicyEngine:
    """Conservative policy gate for permission, risk and approval checks."""

    def __init__(
        self,
        allowed_permissions: Iterable[str] = (),
        *,
        maximum_risk: RiskClass = RiskClass.MEDIUM,
        approval_matrix: ApprovalMatrix | None = None,
        allow_irreversible: bool = False,
    ) -> None:
        self.allowed_permissions = frozenset(allowed_permissions)
        self.maximum_risk = maximum_risk
        self.approval_matrix = approval_matrix or ApprovalMatrix()
        self.allow_irreversible = allow_irreversible

    def evaluate(self, context: ExecutionContext, contract: CapabilityContract) -> PolicyResult:
        reasons: list[str] = []
        order = {RiskClass.LOW: 0, RiskClass.MEDIUM: 1, RiskClass.HIGH: 2, RiskClass.CRITICAL: 3}

        if not context.execution_id:
            reasons.append("Execution identity is required.")
        if not context.task_id:
            reasons.append("Task identity is required.")
        if order[contract.risk_class] > order[self.maximum_risk]:
            reasons.append(f"Risk exceeds policy limit: {contract.risk_class.value}")
        missing = set(contract.permissions) - self.allowed_permissions
        if missing:
            reasons.append("Missing permissions: " + ", ".join(sorted(missing)))

        if reasons:
            return PolicyResult(PolicyDecision.DENY, tuple(reasons))
        if self.approval_matrix.requires_approval(contract.risk_class):
            return PolicyResult(PolicyDecision.REQUIRE_APPROVAL)
        return PolicyResult(PolicyDecision.ALLOW)

    def authorize(self, context: ExecutionContext, contract: CapabilityContract, *, approved: bool = False) -> PolicyResult:
        result = self.evaluate(context, contract)
        if result.decision is PolicyDecision.REQUIRE_APPROVAL and approved:
            return PolicyResult(PolicyDecision.ALLOW, ("Required approval supplied.",))
        return result
