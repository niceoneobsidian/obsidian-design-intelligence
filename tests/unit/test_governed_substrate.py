from odi.control import (
    ApprovalMatrix,
    CapabilityRouter,
    CheckpointStore,
    FailureClass,
    PolicyDecision,
    PolicyEngine,
    RecoveryPolicy,
    WorkflowState,
)
from odi.control.state import ExecutionIdentity
from odi.core.contracts import CapabilityContract, ExecutionContext, RiskClass
from odi.evaluation.evaluator import Candidate, EvaluationDataset, Evaluator
from odi.registry.agents import AgentDefinition, AgentRegistry
from odi.registry.capabilities import CapabilityRegistry


def _context() -> ExecutionContext:
    return ExecutionContext("exec-1", "task-1", "Design a logo")


def test_policy_requires_approval_for_high_risk() -> None:
    policy = PolicyEngine(
        allowed_permissions={"design.write"}, approval_matrix=ApprovalMatrix()
    )
    contract = CapabilityContract(
        "logo", "Logo", "1.0", {}, {}, RiskClass.HIGH, ("design.write",)
    )
    assert policy.evaluate(_context(), contract).decision is PolicyDecision.REQUIRE_APPROVAL
    assert policy.authorize(_context(), contract, approved=True).decision is PolicyDecision.ALLOW


def test_router_selects_single_capable_agent() -> None:
    capabilities = CapabilityRegistry()
    contract = CapabilityContract(
        "logo", "Logo", "1.0", {}, {}, permissions=("design.read",)
    )
    capabilities.register(contract)
    agents = AgentRegistry()
    agents.register(
        "logo-agent",
        AgentDefinition("logo-agent", "Logo Agent", "designer", ("logo",)),
    )
    router = CapabilityRouter(capabilities, agents, PolicyEngine({"design.read"}))
    decision = router.route("logo", _context())
    assert decision.agent.id == "logo-agent"


def test_checkpoint_is_immutable_history() -> None:
    state = WorkflowState(identity=ExecutionIdentity("exec-1"), objective="x")
    store = CheckpointStore()
    first = store.save(state)
    state.outputs.append({"x": 1})
    second = store.save(state)
    assert first.sequence == 1
    assert second.sequence == 2
    assert len(store.history("exec-1")) == 2


def test_recovery_is_bounded_and_classified() -> None:
    state = WorkflowState(identity=ExecutionIdentity("exec-1"), objective="x")
    policy = RecoveryPolicy(max_retries=1)
    first = policy.apply(state, FailureClass.TRANSIENT)
    second = policy.apply(state, FailureClass.TRANSIENT)
    assert first.action == "retry"
    assert second.action == "escalate"


def test_evaluation_dataset_supports_promotion() -> None:
    evaluator = Evaluator((lambda value: value is not None,))
    candidate = Candidate("logo-v1", "1.0", "artifact")
    dataset = EvaluationDataset("smoke", ("a", "b"))
    result = evaluator.evaluate_dataset(candidate, dataset)
    decision = evaluator.promote(candidate, result, threshold=0.8)
    assert result.passed is True
    assert decision.eligible is True
