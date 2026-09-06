"""Small, deterministic lifecycle coordinator for the ODI/OIS boundary."""

from dataclasses import dataclass

from .ois_protocols import (
    ExecutionRequest,
    ExecutionResult,
    OISEvidencePort,
    OISExecutionPort,
    OISPolicyPort,
    OISValidationPort,
)


@dataclass(frozen=True)
class LifecycleOutcome:
    """Outcome of a governed capability invocation."""

    result: ExecutionResult
    validated: bool
    evidence_ids: tuple[str, ...]


class GovernedExecutor:
    """Enforces policy before execution and validation after execution."""

    def __init__(
        self,
        policy: OISPolicyPort,
        execution: OISExecutionPort,
        validation: OISValidationPort,
        evidence: OISEvidencePort,
    ) -> None:
        self._policy = policy
        self._execution = execution
        self._validation = validation
        self._evidence = evidence

    def run(self, request: ExecutionRequest) -> LifecycleOutcome:
        decision = self._policy.authorize(request)
        if not decision.allowed:
            raise PermissionError(decision.reason or "execution denied by policy")

        result = self._execution.execute(request)
        evidence_ids = tuple(self._evidence.record(request, result))
        validated = self._validation.validate(request, result)
        return LifecycleOutcome(
            result=result,
            validated=validated,
            evidence_ids=evidence_ids,
        )
