from odi.core.contracts import ExecutionContext
from odi.core.lifecycle import GovernedExecutor
from odi.core.ois_protocols import ExecutionRequest, ExecutionResult, PolicyDecision


class AllowPolicy:
    def authorize(self, request: ExecutionRequest) -> PolicyDecision:
        return PolicyDecision(allowed=True)


class Executor:
    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        return ExecutionResult(status="completed", outputs={"artifact": "design"})


class Validator:
    def validate(self, request: ExecutionRequest, result: ExecutionResult) -> bool:
        return result.status == "completed"


class Evidence:
    def record(self, request: ExecutionRequest, result: ExecutionResult) -> list[str]:
        return [f"evidence:{request.execution.execution_id}"]


def request() -> ExecutionRequest:
    context = ExecutionContext(
        execution_id="exec-001",
        task_id="task-001",
        objective="evaluate a design direction",
    )
    return ExecutionRequest(
        capability_id="design.evaluation",
        execution=context,
        idempotency_key="task-001:design.evaluation:1",
    )


def test_policy_precedes_execution_and_validation_follows() -> None:
    outcome = GovernedExecutor(
        AllowPolicy(), Executor(), Validator(), Evidence()
    ).run(request())

    assert outcome.validated is True
    assert outcome.result.outputs["artifact"] == "design"
    assert outcome.evidence_ids == ("evidence:exec-001",)


def test_denied_execution_does_not_run() -> None:
    class DenyPolicy:
        def authorize(self, request: ExecutionRequest) -> PolicyDecision:
            return PolicyDecision(allowed=False, reason="approval required")

    try:
        GovernedExecutor(DenyPolicy(), Executor(), Validator(), Evidence()).run(request())
    except PermissionError as exc:
        assert str(exc) == "approval required"
    else:
        raise AssertionError("denied execution must raise before provider invocation")
