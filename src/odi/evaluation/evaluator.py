from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class Evaluation:
    name: str
    passed: bool
    score: float
    findings: tuple[str, ...] = ()

class Evaluator:
    def __init__(self, checks: tuple[Callable[[Any], bool], ...] = ()):
        self.checks = checks

    def evaluate(self, output: Any) -> Evaluation:
        outcomes = tuple(bool(c(output)) for c in self.checks)
        passed = all(outcomes) if outcomes else True
        score = sum(outcomes) / len(outcomes) if outcomes else 1.0
        return Evaluation("runtime", passed, score)
