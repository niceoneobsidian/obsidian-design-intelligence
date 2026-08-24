from abc import ABC, abstractmethod
from uuid import uuid4
from odi.core.types import ExecutionResult, Plan

class CapabilityExecutor(ABC):
    @abstractmethod
    def execute(self, capability_id: str, inputs: dict) -> object: ...

class ExecutionRuntime:
    def __init__(self, executor: CapabilityExecutor):
        self.executor = executor

    def execute(self, plan: Plan) -> ExecutionResult:
        execution_id = f"exec-{uuid4().hex}"
        outputs = {}
        for step in plan.steps:
            outputs[step.id] = self.executor.execute(step.capability_id, dict(step.inputs))
        return ExecutionResult(execution_id, "executed", outputs, (), {"step_count": len(plan.steps)})
