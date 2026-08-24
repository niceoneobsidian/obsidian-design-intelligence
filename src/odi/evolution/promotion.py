from dataclasses import dataclass
from odi.evaluation.evaluator import Evaluation

@dataclass(frozen=True)
class Candidate:
    id: str
    version: str
    payload: object

@dataclass(frozen=True)
class PromotionDecision:
    candidate_id: str
    promoted: bool
    reason: str

class PromotionGate:
    """Controlled evolution boundary: evaluation precedes activation."""
    def decide(self, candidate: Candidate, evaluation: Evaluation, minimum_score: float = 0.9) -> PromotionDecision:
        promoted = evaluation.passed and evaluation.score >= minimum_score
        return PromotionDecision(candidate.id, promoted, "evaluation threshold met" if promoted else "evaluation threshold not met")
