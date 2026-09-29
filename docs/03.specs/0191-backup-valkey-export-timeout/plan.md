---
title: "Backup Valkey Export Timeout Plan"
version: "0.3.0"
type: "sdlc/plan"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0191-PLAN-0001"
parent_ids:
- "SPEC-0191"
created: "2026-09-29"
---

# Backup Valkey Export Timeout Plan

## Objective

Bound the `mng-valkey` RDB export in the nightly backup, as
[SPEC-0191](spec.md) describes.

## Dependencies

- The owner's approval of 2026-09-29 (backup action A).

## Execution Sequence

1. W1: Add the contract assertions and observe them fail; change the script
   and RUN-0021; check the image's `timeout` and a live export (criteria 1,
   2, 3).
2. W2: Run the full gate and both unit suites (criterion 4).

## Risk and Rollback

W1 is one commit; reverting it restores the unbounded export.

## Verification

- `BackupContractTests`, `bash -n`, and pre-commit.
- `run-ci-gate.py --profile full`, `tests/lib`, and `tests/validation`.

## Rulings

None yet.
