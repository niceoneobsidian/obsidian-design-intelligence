from dataclasses import dataclass
from odi.core.types import Plan, ValidationResult

@dataclass(frozen=True)
class SupervisionDecision:
    action: str
    reason: str

class Supervisor:
    """Policy checkpoint between planning, execution and recovery."""
    def approve(self, plan: Plan) -> SupervisionDecision:
        return SupervisionDecision("execute", f"Plan {plan.id} approved")

    def after_validation(self, result: ValidationResult) -> SupervisionDecision:
        return SupervisionDecision("complete" if result.passed else "recover", "validation passed" if result.passed else "validation failed")
