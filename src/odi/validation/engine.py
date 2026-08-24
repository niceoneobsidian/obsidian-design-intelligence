from collections.abc import Callable
from odi.core.types import ExecutionResult, ValidationResult

class ValidationEngine:
    def __init__(self, checks: tuple[Callable[[ExecutionResult], bool], ...] = ()):
        self.checks = checks

    def validate(self, result: ExecutionResult) -> ValidationResult:
        outcomes = tuple(bool(check(result)) for check in self.checks)
        passed = all(outcomes) if outcomes else result.status == "executed"
        score = sum(outcomes) / len(outcomes) if outcomes else (1.0 if passed else 0.0)
        return ValidationResult(passed, score, {f"check_{i}": value for i, value in enumerate(outcomes)}, () if passed else ("One or more validation checks failed.",))
