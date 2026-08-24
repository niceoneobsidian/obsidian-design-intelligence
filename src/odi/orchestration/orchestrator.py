from odi.core.types import ExecutionResult, Plan
from odi.supervision.supervisor import Supervisor
from odi.execution.runtime import ExecutionRuntime
from odi.validation.engine import ValidationEngine

class Orchestrator:
    def __init__(self, runtime: ExecutionRuntime, validator: ValidationEngine, supervisor: Supervisor | None = None):
        self.runtime = runtime
        self.validator = validator
        self.supervisor = supervisor or Supervisor()

    def run(self, plan: Plan) -> ExecutionResult:
        decision = self.supervisor.approve(plan)
        if decision.action != "execute":
            raise RuntimeError(decision.reason)
        result = self.runtime.execute(plan)
        validation = self.validator.validate(result)
        if not validation.passed:
            return ExecutionResult(result.execution_id, "failed_validation", result.output, result.evidence_ids, {"validation": validation.findings})
        return ExecutionResult(result.execution_id, "completed", result.output, result.evidence_ids, {"validation_score": validation.score})
