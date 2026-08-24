from odi.core.types import Intent, PlanStep
from odi.context.engine import ContextEngine
from odi.design.capability import DesignCapability, DesignCapabilityFabric
from odi.execution.runtime import CapabilityExecutor, ExecutionRuntime
from odi.orchestration.orchestrator import Orchestrator
from odi.planning.planner import DeterministicPlanner
from odi.validation.engine import ValidationEngine

class EchoExecutor(CapabilityExecutor):
    def execute(self, capability_id: str, inputs: dict) -> object:
        return {"capability": capability_id, "inputs": inputs}

def test_canonical_stack_executes():
    design = DesignCapabilityFabric()
    design.register(DesignCapability("design.test", "test", "Test", "Test capability"))
    intent = Intent("run test design capability")
    context = ContextEngine().assemble(intent)
    planner = DeterministicPlanner(lambda _intent, _context: (PlanStep("step-1", "design.test", intent.objective),))
    plan = planner.plan(intent, context)
    result = Orchestrator(ExecutionRuntime(EchoExecutor()), ValidationEngine()).run(plan)
    assert result.status == "completed"
    assert result.output["step-1"]["capability"] == "design.test"
