# Monthly Review Automation

## Purpose

Monthly Review is the strategic layer above Weekly Review. It consumes only completed weekly reviews, identifies repeated signals, and produces machine-readable strategic adjustments and next-month priorities.

```text
Completed Weekly Reviews
          ↓
   Monthly Review Engine
          ↓
 performance + patterns
          ↓
 strategic adjustments
          ↓
 next-month priorities
          ↓
      next plan
```

## Contract

`MonthlyReviewEngine.generate(...)` requires:

- one or more `WeeklyReview` inputs;
- every input marked `completed=True`;
- unique weekly-review IDs;
- valid week ranges;
- a requested `YYYY-MM` period matching the week's closing date.

A week that crosses a month boundary is assigned to the month in which it closes. This prevents one weekly review from being silently counted twice.

## Outputs

`MonthlyReview` contains:

- objective completion rate;
- average values for each supplied metric;
- recurring blockers, risks, and opportunities;
- ranked `StrategicAdjustment` objects with evidence-week IDs and confidence;
- ranked `NextMonthPriority` objects linked to their source adjustments;
- a concise synthesis summary.

Recurring signals require occurrence in at least two distinct weekly reviews. Repeated copies of the same note inside one weekly review count once.

## Governance boundary

The implementation is deterministic and provider-neutral. It does not silently mutate strategy, activate a capability, or execute a priority. It creates candidate strategic decisions. Existing governance, planning, execution, validation, evidence, and controlled-evolution layers remain responsible for authorization and activation.

An LLM or other reasoning provider may later enrich the synthesis behind this contract without changing the core review data model.
