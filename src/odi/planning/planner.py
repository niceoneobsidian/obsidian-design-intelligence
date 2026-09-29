from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from odi.context.engine import AssembledContext
from odi.core.types import Intent, Plan


class Planner(ABC):
    @abstractmethod
    def plan(self, intent: Intent, context: AssembledContext) -> Plan: ...


class DeterministicPlanner(Planner):
    def __init__(
        self,
        capability_selector: Callable[[Intent, AssembledContext], tuple[Any, ...]],
    ) -> None:
        self.capability_selector = capability_selector

    def plan(self, intent: Intent, context: AssembledContext) -> Plan:
        steps = tuple(self.capability_selector(intent, context))
        return Plan(
            id=f"plan-{intent.id}",
            steps=steps,
            rationale="Selected from intent, context and registered capabilities.",
        )
