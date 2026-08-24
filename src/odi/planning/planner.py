from abc import ABC, abstractmethod
from odi.core.types import Plan, Intent
from odi.context.engine import AssembledContext

class Planner(ABC):
    @abstractmethod
    def plan(self, intent: Intent, context: AssembledContext) -> Plan: ...

class DeterministicPlanner(Planner):
    def __init__(self, capability_selector):
        self.capability_selector = capability_selector

    def plan(self, intent: Intent, context: AssembledContext) -> Plan:
        steps = tuple(self.capability_selector(intent, context))
        return Plan(id=f"plan-{intent.id}", steps=steps, rationale="Selected from intent, context and registered capabilities.")
