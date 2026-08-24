"""Unified evaluation harness integrated from the OIS learning work."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable


@dataclass(frozen=True)
class Evaluation:
    name: str
    passed: bool
    score: float
    findings: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EvaluationDataset:
    id: str
    cases: tuple[Any, ...]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Candidate:
    id: str
    version: str
    output: Any
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PromotionDecision:
    candidate_id: str
    eligible: bool
    score: float
    reason: str


class Evaluator:
    """Composable deterministic evaluation harness."""

    def __init__(self, checks: tuple[Callable[[Any], bool], ...] = ()) -> None:
        self.checks = checks

    def evaluate(self, output: Any) -> Evaluation:
        outcomes = tuple(bool(check(output)) for check in self.checks)
        passed = all(outcomes) if outcomes else True
        score = sum(outcomes) / len(outcomes) if outcomes else 1.0
        findings = () if passed else ("One or more evaluation checks failed.",)
        return Evaluation("runtime", passed, score, findings)

    def evaluate_dataset(self, candidate: Candidate, dataset: EvaluationDataset) -> Evaluation:
        results = [self.evaluate(case) for case in dataset.cases]
        score = sum(r.score for r in results) / len(results) if results else 1.0
        passed = all(r.passed for r in results)
        findings = tuple(f"{dataset.id}:{i}:{f}" for i, r in enumerate(results) for f in r.findings)
        return Evaluation(candidate.id, passed, score, findings, {"dataset_id": dataset.id, "candidate_version": candidate.version})

    def promote(self, candidate: Candidate, evaluation: Evaluation, *, threshold: float = 0.8) -> PromotionDecision:
        eligible = evaluation.passed and evaluation.score >= threshold
        return PromotionDecision(
            candidate_id=candidate.id,
            eligible=eligible,
            score=evaluation.score,
            reason="Candidate meets promotion threshold." if eligible else "Candidate failed promotion threshold.",
        )
