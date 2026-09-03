"""Deterministic monthly-review automation.

The engine turns completed weekly reviews into a structured strategic review.
It deliberately has no model/provider dependency: an LLM can be added behind
this contract later without changing the review domain model.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
import re
from typing import Iterable, Mapping
from uuid import uuid4


_COMPLETED = "completed"
_POSITIVE = {"completed", "done", "achieved", "success"}
_PARTIAL = {"partial", "partially_completed", "at_risk"}
_NEGATIVE = {"missed", "failed", "blocked", "deferred"}


@dataclass(frozen=True)
class WeeklyObjective:
    """An objective outcome recorded by a weekly review."""

    title: str
    status: str
    metric: float | None = None


@dataclass(frozen=True)
class WeeklyReview:
    """Canonical input consumed by the monthly review engine."""

    id: str
    week_start: date
    week_end: date
    completed: bool
    objectives: tuple[WeeklyObjective, ...] = ()
    metrics: Mapping[str, float] = field(default_factory=dict)
    wins: tuple[str, ...] = ()
    misses: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    opportunities: tuple[str, ...] = ()
    lessons: tuple[str, ...] = ()
    decisions: tuple[str, ...] = ()


@dataclass(frozen=True)
class StrategicAdjustment:
    """A proposed change to strategy or operating behavior."""

    id: str
    category: str
    title: str
    action: str
    rationale: str
    evidence_weeks: tuple[str, ...]
    priority: int
    confidence: float


@dataclass(frozen=True)
class NextMonthPriority:
    """Machine-readable priority handed to the next planning cycle."""

    id: str
    title: str
    objective: str
    rationale: str
    success_metric: str
    priority: int
    source_adjustment_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class MonthlyReview:
    """Complete monthly synthesis and strategic handoff."""

    id: str
    period: str
    generated_at: datetime
    source_week_ids: tuple[str, ...]
    week_count: int
    objective_completion_rate: float
    metric_summary: Mapping[str, float]
    recurring_blockers: tuple[str, ...]
    recurring_risks: tuple[str, ...]
    recurring_opportunities: tuple[str, ...]
    strategic_adjustments: tuple[StrategicAdjustment, ...]
    next_month_priorities: tuple[NextMonthPriority, ...]
    summary: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable representation of the review."""
        return asdict(self)


class MonthlyReviewError(ValueError):
    """Raised when monthly-review inputs violate the review contract."""


class MonthlyReviewEngine:
    """Aggregate completed weekly reviews into strategic monthly decisions."""

    def __init__(self, *, max_adjustments: int = 5, max_priorities: int = 5) -> None:
        if max_adjustments < 1 or max_priorities < 1:
            raise ValueError("max_adjustments and max_priorities must be positive")
        self.max_adjustments = max_adjustments
        self.max_priorities = max_priorities

    def generate(
        self,
        weekly_reviews: Iterable[WeeklyReview],
        *,
        year: int,
        month: int,
    ) -> MonthlyReview:
        reviews = tuple(weekly_reviews)
        period = self._period(year, month)
        self._validate(reviews, year, month)

        source_ids = tuple(review.id for review in reviews)
        metric_summary = self._summarize_metrics(reviews)
        completion_rate = self._completion_rate(reviews)
        blockers = self._recurring(reviews, "blockers")
        risks = self._recurring(reviews, "risks")
        opportunities = self._recurring(reviews, "opportunities")

        adjustments = self._build_adjustments(reviews, blockers, risks, opportunities)
        priorities = self._build_priorities(adjustments, opportunities, metric_summary)
        summary = self._summary(
            period,
            len(reviews),
            completion_rate,
            blockers,
            risks,
            opportunities,
        )

        return MonthlyReview(
            id=f"monthly-review-{uuid4().hex}",
            period=period,
            generated_at=datetime.now(timezone.utc),
            source_week_ids=source_ids,
            week_count=len(reviews),
            objective_completion_rate=completion_rate,
            metric_summary=metric_summary,
            recurring_blockers=tuple(item for item, _ in blockers),
            recurring_risks=tuple(item for item, _ in risks),
            recurring_opportunities=tuple(item for item, _ in opportunities),
            strategic_adjustments=tuple(adjustments),
            next_month_priorities=tuple(priorities),
            summary=summary,
        )

    @staticmethod
    def _period(year: int, month: int) -> str:
        if month not in range(1, 13):
            raise MonthlyReviewError("month must be between 1 and 12")
        if year < 1:
            raise MonthlyReviewError("year must be positive")
        return f"{year:04d}-{month:02d}"

    @staticmethod
    def _validate(reviews: tuple[WeeklyReview, ...], year: int, month: int) -> None:
        if not reviews:
            raise MonthlyReviewError("at least one completed weekly review is required")
        seen: set[str] = set()
        for review in reviews:
            if review.id in seen:
                raise MonthlyReviewError(f"duplicate weekly review: {review.id}")
            seen.add(review.id)
            if not review.completed:
                raise MonthlyReviewError(f"weekly review is not completed: {review.id}")
            if review.week_start > review.week_end:
                raise MonthlyReviewError(f"invalid week range: {review.id}")
            if review.week_start.year != year or review.week_start.month != month:
                raise MonthlyReviewError(
                    f"weekly review {review.id} is outside the requested period"
                )

    @staticmethod
    def _completion_rate(reviews: tuple[WeeklyReview, ...]) -> float:
        objectives = [objective for review in reviews for objective in review.objectives]
        if not objectives:
            return 0.0
        completed = sum(objective.status.strip().lower() in _POSITIVE for objective in objectives)
        return round(completed / len(objectives), 4)

    @staticmethod
    def _summarize_metrics(reviews: tuple[WeeklyReview, ...]) -> dict[str, float]:
        values: dict[str, list[float]] = defaultdict(list)
        for review in reviews:
            for name, value in review.metrics.items():
                values[name].append(float(value))
        return {
            name: round(sum(items) / len(items), 4)
            for name, items in sorted(values.items())
        }

    @classmethod
    def _recurring(
        cls,
        reviews: tuple[WeeklyReview, ...],
        field_name: str,
    ) -> tuple[tuple[str, int], ...]:
        occurrences: Counter[str] = Counter()
        display: dict[str, str] = {}
        for review in reviews:
            # Count once per week: a repeated note in one review is still one signal.
            seen_this_week: set[str] = set()
            for raw in getattr(review, field_name):
                key = cls._normalize(raw)
                if not key or key in seen_this_week:
                    continue
                seen_this_week.add(key)
                occurrences[key] += 1
                display.setdefault(key, raw.strip())
        ranked = sorted(occurrences.items(), key=lambda item: (-item[1], item[0]))
        return tuple((display[key], count) for key, count in ranked if count >= 2)

    def _build_adjustments(
        self,
        reviews: tuple[WeeklyReview, ...],
        blockers: tuple[tuple[str, int], ...],
        risks: tuple[tuple[str, int], ...],
        opportunities: tuple[tuple[str, int], ...],
    ) -> list[StrategicAdjustment]:
        candidates: list[tuple[int, str, str, str, tuple[str, ...], float]] = []
        for item, count in blockers:
            candidates.append(
                (
                    100 + count * 10,
                    "corrective",
                    f"Remove recurring blocker: {item}",
                    f"Create a concrete countermeasure for '{item}' and review its effect weekly.",
                    self._evidence_for(reviews, "blockers", item),
                    min(0.95, 0.55 + 0.10 * count),
                )
            )
        for item, count in risks:
            candidates.append(
                (
                    90 + count * 10,
                    "risk",
                    f"Mitigate recurring risk: {item}",
                    f"Assign an explicit mitigation and leading indicator for '{item}'.",
                    self._evidence_for(reviews, "risks", item),
                    min(0.95, 0.55 + 0.10 * count),
                )
            )
        for item, count in opportunities:
            candidates.append(
                (
                    70 + count * 10,
                    "growth",
                    f"Test recurring opportunity: {item}",
                    f"Run a bounded experiment around '{item}' with a measurable success criterion.",
                    self._evidence_for(reviews, "opportunities", item),
                    min(0.95, 0.50 + 0.10 * count),
                )
            )
        candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
        return [
            StrategicAdjustment(
                id=f"adjustment-{uuid4().hex}",
                category=category,
                title=title,
                action=action,
                rationale=f"Observed in {len(evidence)} weekly review(s).",
                evidence_weeks=evidence,
                priority=index,
                confidence=confidence,
            )
            for index, (_, category, title, action, evidence, confidence) in enumerate(
                candidates[: self.max_adjustments], start=1
            )
        ]

    @staticmethod
    def _build_priorities(
        adjustments: list[StrategicAdjustment],
        opportunities: tuple[tuple[str, int], ...],
        metric_summary: Mapping[str, float],
    ) -> list[NextMonthPriority]:
        priorities: list[NextMonthPriority] = []
        for adjustment in adjustments:
            metric = next(iter(metric_summary), "the agreed operating metric")
            priorities.append(
                NextMonthPriority(
                    id=f"priority-{uuid4().hex}",
                    title=adjustment.title,
                    objective=adjustment.action,
                    rationale=adjustment.rationale,
                    success_metric=f"Improve {metric} or demonstrate measurable impact by month-end.",
                    priority=len(priorities) + 1,
                    source_adjustment_ids=(adjustment.id,),
                )
            )
        if not priorities and opportunities:
            item, _ = opportunities[0]
            priorities.append(
                NextMonthPriority(
                    id=f"priority-{uuid4().hex}",
                    title=f"Validate opportunity: {item}",
                    objective=f"Run a measurable experiment around '{item}'.",
                    rationale="No recurring corrective signal was strong enough to create a priority.",
                    success_metric="Experiment has a predefined pass/fail outcome.",
                    priority=1,
                )
            )
        return priorities

    @staticmethod
    def _evidence_for(
        reviews: tuple[WeeklyReview, ...], field_name: str, item: str
    ) -> tuple[str, ...]:
        target = MonthlyReviewEngine._normalize(item)
        return tuple(
            review.id
            for review in reviews
            if any(MonthlyReviewEngine._normalize(value) == target for value in getattr(review, field_name))
        )

    @staticmethod
    def _normalize(value: str) -> str:
        return re.sub(r"\s+", " ", value.strip().casefold())

    @staticmethod
    def _summary(
        period: str,
        week_count: int,
        completion_rate: float,
        blockers: tuple[tuple[str, int], ...],
        risks: tuple[tuple[str, int], ...],
        opportunities: tuple[tuple[str, int], ...],
    ) -> str:
        return (
            f"{period}: synthesized {week_count} completed weekly reviews; "
            f"objective completion was {completion_rate:.0%}. "
            f"Recurring signals: {len(blockers)} blockers, {len(risks)} risks, "
            f"and {len(opportunities)} opportunities."
        )
