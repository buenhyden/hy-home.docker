---
title: "Remaining HOME Classification Plan"
version: "0.3.0"
type: "sdlc/plan"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190-PLAN-0001"
parent_ids:
- "SPEC-0190"
created: "2026-09-29"
---

# Remaining HOME Classification Plan

## Objective

Classify `registry`, `dcgm-exporter`, and `seaweedfs-s3` as `HOME` in every
current document, as [SPEC-0190](spec.md) describes.

## Dependencies

- The owner's ruling of 2026-09-29.

## Execution Sequence

1. W1: Change the wording in GDE-0065, POL-0065, the registry README,
   GDE-0045, the GPU alert rule comment, the observability README, and the
   three m0021 rows (criterion 1).
2. W2: Run the full gate and both unit suites (criterion 2).

## Risk and Rollback

W1 is one commit; reverting it restores the previous wording.

## Verification

- A line-wide search of each owner for `OPTIONAL`, `opt-in`, on-demand, and
  HOME exclusion.
- `run-ci-gate.py --profile full`, `tests/lib`, and `tests/validation`.

## Rulings

None yet.
