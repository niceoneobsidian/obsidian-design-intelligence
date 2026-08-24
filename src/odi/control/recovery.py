"""Bounded failure-first recovery policy."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .state import WorkflowState


class FailureClass(StrEnum):
    TRANSIENT = "transient"
    PARAMETER = "parameter"
    TOOL = "tool"
    PLAN = "plan"
    STATE = "state"
    PERMISSION = "permission"
    SAFETY = "safety"
    VALIDATION = "validation"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class RecoveryDecision:
    failure: FailureClass
    action: str
    retry_allowed: bool
    terminal: bool
    reason: str


class RecoveryPolicy:
    """Deterministically maps failures to bounded recovery actions."""

    def __init__(self, *, max_retries: int = 2, max_recovery_attempts: int = 3) -> None:
        if max_retries < 0 or max_recovery_attempts < 0:
            raise ValueError("recovery limits must be >= 0")
        self.max_retries = max_retries
        self.max_recovery_attempts = max_recovery_attempts

    def classify(self, failure: FailureClass, state: WorkflowState) -> RecoveryDecision:
        if failure is FailureClass.TRANSIENT:
            allowed = state.retry_count < self.max_retries
            return RecoveryDecision(failure, "retry" if allowed else "escalate", allowed, not allowed,
                                    "Transient failure is retryable." if allowed else "Retry limit exhausted.")
        if failure is FailureClass.PARAMETER:
            return RecoveryDecision(failure, "correct", False, False, "Parameters require correction.")
        if failure is FailureClass.TOOL:
            return RecoveryDecision(failure, "fallback", False, False, "Tool failure should use an alternative capability.")
        if failure is FailureClass.PLAN:
            return RecoveryDecision(failure, "replan", False, False, "Plan failure requires replanning.")
        if failure is FailureClass.STATE:
            allowed = state.recovery_attempts < self.max_recovery_attempts
            return RecoveryDecision(failure, "recover" if allowed else "escalate", False, not allowed,
                                    "State recovery is permitted." if allowed else "State recovery limit exhausted.")
        if failure is FailureClass.PERMISSION:
            return RecoveryDecision(failure, "escalate", False, False, "Permission failures require escalation.")
        if failure is FailureClass.SAFETY:
            return RecoveryDecision(failure, "stop", False, True, "Safety failures terminate execution.")
        if failure is FailureClass.VALIDATION:
            return RecoveryDecision(failure, "refine", False, False, "Validation failure requires refinement and revalidation.")
        return RecoveryDecision(failure, "escalate", False, False, "Unknown failure requires escalation.")

    def apply(self, state: WorkflowState, failure: FailureClass) -> RecoveryDecision:
        decision = self.classify(failure, state)
        state.recovery.append({"failure": failure.value, "action": decision.action, "reason": decision.reason})
        if decision.action == "retry":
            state.retry_count += 1
            state.transition("recovering")
        elif decision.action in {"recover", "refine"}:
            state.recovery_attempts += 1
            state.transition("recovering")
        elif decision.action == "replan":
            state.recovery_attempts += 1
            state.transition("replanning")
        elif decision.action == "escalate":
            state.transition("escalated")
        elif decision.action == "stop":
            state.transition("stopped")
        return decision
