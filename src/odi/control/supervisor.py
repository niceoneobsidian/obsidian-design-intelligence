"""Deterministic supervision boundary above ODI orchestration."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from odi.core.contracts import ExecutionContext

from .checkpoint import CheckpointStore
from .recovery import FailureClass, RecoveryDecision, RecoveryPolicy
from .router import CapabilityRouter, RouteDecision
from .state import WorkflowState


@dataclass(frozen=True)
class SupervisionDecision:
    action: str
    reason: str
    terminal: bool


class Supervisor:
    """Coordinates routing, checkpointing and bounded recovery without executing work itself."""

    def __init__(
        self,
        router: CapabilityRouter,
        *,
        recovery: RecoveryPolicy | None = None,
        checkpoints: CheckpointStore | None = None,
    ) -> None:
        self.router = router
        self.recovery = recovery or RecoveryPolicy()
        self.checkpoints = checkpoints or CheckpointStore()

    def select(self, capability_id: str, context: ExecutionContext, *, approved: bool = False) -> RouteDecision:
        return self.router.route(capability_id, context, approved=approved)

    def checkpoint(self, state: WorkflowState):
        return self.checkpoints.save(state)

    def recover(self, state: WorkflowState, failure: FailureClass) -> RecoveryDecision:
        return self.recovery.apply(state, failure)

    def execute(
        self,
        state: WorkflowState,
        capability_id: str,
        executor: Callable[[Any, WorkflowState], Any],
        *,
        approved: bool = False,
    ) -> Any:
        if state.execution is None:
            raise ValueError("WorkflowState.execution is required for supervised execution")
        route = self.select(capability_id, state.execution, approved=approved)
        state.governance.append({"capability_id": capability_id, "agent_id": route.agent.id, "decision": "allow"})
        state.transition("executing")
        output = executor(route.agent, state)
        state.outputs.append({"capability_id": capability_id, "agent_id": route.agent.id, "output": output})
        self.checkpoint(state)
        return output

    def inspect_failure(self, state: WorkflowState) -> SupervisionDecision:
        if not state.recovery:
            return SupervisionDecision("continue", "No failure is recorded.", False)
        latest = state.recovery[-1]
        action = str(latest.get("action", "escalate"))
        return SupervisionDecision(action, str(latest.get("reason", "")), action in {"stop", "escalate"})
