# 001 - Static Conclusion, Dynamic Models

Status: Accepted

## Context

The model artifacts are regenerated whenever a scenario is run or promoted.
Human conclusions need review, judgment, and source-aware wording. Letting a
promotion command rewrite canonical prose would make a timestamped model run
look like reviewed analysis.

## Decision

Promotion writes promoted JSON artifacts only. `data_center/conclusion.md` is a
static reviewed document tied to the promoted defaults by deliberate review.
Generated or draft Markdown may exist only as noncanonical scratch output.

## Consequences

Default model changes require a separate conclusion review. This adds a small
manual step, but it prevents stale or machine-written prose from silently
becoming the public conclusion.
