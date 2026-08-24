from dataclasses import dataclass
from odi.core.contracts import RiskClass

@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str

class PolicyEngine:
    def authorize(self, risk: RiskClass, approved: bool = True) -> PolicyDecision:
        if risk in {RiskClass.HIGH, RiskClass.CRITICAL} and not approved:
            return PolicyDecision(False, "Elevated-risk action requires approval")
        return PolicyDecision(True, "Policy permits action")
