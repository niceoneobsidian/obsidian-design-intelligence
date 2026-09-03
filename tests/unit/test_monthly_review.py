from datetime import date

import pytest

from odi.reviews.monthly import (
    MonthlyReviewEngine,
    MonthlyReviewError,
    WeeklyObjective,
    WeeklyReview,
)


def weekly(
    number: int,
    *,
    completed: bool = True,
    blockers: tuple[str, ...] = (),
    risks: tuple[str, ...] = (),
    opportunities: tuple[str, ...] = (),
) -> WeeklyReview:
    return WeeklyReview(
        id=f"week-{number}",
        week_start=date(2026, 9, number * 7 - 6),
        week_end=date(2026, 9, number * 7),
        completed=completed,
        objectives=(
            WeeklyObjective("Ship milestone", "completed"),
            WeeklyObjective("Improve quality", "missed"),
        ),
        metrics={"throughput": float(number * 10)},
        blockers=blockers,
        risks=risks,
        opportunities=opportunities,
    )


def test_monthly_review_aggregates_metrics_and_completion() -> None:
    result = MonthlyReviewEngine().generate(
        [weekly(1), weekly(2)], year=2026, month=9
    )

    assert result.period == "2026-09"
    assert result.week_count == 2
    assert result.objective_completion_rate == 0.5
    assert result.metric_summary == {"throughput": 15.0}


def test_recurring_signals_become_strategic_adjustments_and_priorities() -> None:
    result = MonthlyReviewEngine().generate(
        [
            weekly(1, blockers=("Slow approvals",), risks=("Capacity risk",)),
            weekly(2, blockers=(" slow   approvals ",), risks=("Capacity risk",)),
            weekly(3, opportunities=("New distribution channel",)),
        ],
        year=2026,
        month=9,
    )

    assert result.recurring_blockers == ("Slow approvals",)
    assert result.recurring_risks == ("Capacity risk",)
    assert result.strategic_adjustments[0].category == "corrective"
    assert result.strategic_adjustments[0].evidence_weeks == ("week-1", "week-2")
    assert result.next_month_priorities[0].source_adjustment_ids == (
        result.strategic_adjustments[0].id,
    )


def test_incomplete_weekly_review_is_rejected() -> None:
    with pytest.raises(MonthlyReviewError, match="not completed"):
        MonthlyReviewEngine().generate(
            [weekly(1, completed=False)], year=2026, month=9
        )


def test_cross_month_weekly_review_is_rejected() -> None:
    review = WeeklyReview(
        id="week-cross-month",
        week_start=date(2026, 8, 31),
        week_end=date(2026, 9, 6),
        completed=True,
    )

    with pytest.raises(MonthlyReviewError, match="outside"):
        MonthlyReviewEngine().generate([review], year=2026, month=9)


def test_duplicate_weekly_reviews_are_rejected() -> None:
    review = weekly(1)
    with pytest.raises(MonthlyReviewError, match="duplicate"):
        MonthlyReviewEngine().generate([review, review], year=2026, month=9)


def test_empty_month_is_rejected() -> None:
    with pytest.raises(MonthlyReviewError, match="at least one"):
        MonthlyReviewEngine().generate([], year=2026, month=9)
