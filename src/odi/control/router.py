"""Capability-to-agent routing integrated from the OIS registry/supervisor work."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from odi.core.contracts import CapabilityContract, ExecutionContext
from odi.registry.agents import AgentDefinition, AgentRegistry
from odi.registry.capabilities import CapabilityRegistry

from .policy import PolicyDecision, PolicyEngine


@dataclass(frozen=True)
class RouteDecision:
    capability: CapabilityContract
    agent: AgentDefinition
    candidates: tuple[AgentDefinition, ...]
    reason: str


class CapabilityRouter:
    """Resolve exactly one policy-authorized and available agent."""

    def __init__(
        self,
        capabilities: CapabilityRegistry,
        agents: AgentRegistry,
        policy: PolicyEngine,
        availability: Callable[[AgentDefinition], bool] | None = None,
    ) -> None:
        self.capabilities = capabilities
        self.agents = agents
        self.policy = policy
        self.availability = availability

    def route(self, capability_id: str, context: ExecutionContext, *, approved: bool = False) -> RouteDecision:
        capability = self.capabilities.get(capability_id)
        policy = self.policy.authorize(context, capability, approved=approved)
        if policy.decision is not PolicyDecision.ALLOW:
            raise PermissionError("; ".join(policy.reasons) or "Capability is not authorized")

        candidates = self.agents.resolve_for(capability_id)
        eligible = tuple(a for a in candidates if self.availability is None or self.availability(a))
        if not eligible:
            raise LookupError(f"No eligible agent for {capability_id}@{capability.version}")
        if len(eligible) > 1:
            raise RuntimeError(f"Ambiguous agent routing for {capability_id}: {len(eligible)} eligible agents")
        return RouteDecision(capability, eligible[0], eligible, "Selected the sole eligible agent after policy and availability filtering.")
