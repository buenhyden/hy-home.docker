---
title: "HOME Classification and Valkey Key Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0189-PLAN-0001"
parent_ids:
- "SPEC-0189"
created: "2026-09-29"
---

# HOME Classification and Valkey Key Plan

## Objective

Rename `VALKEY_MNG_HOST_POST` and classify Tempo and Pyroscope as `HOME`
everywhere, as [SPEC-0189](spec.md) describes.

## Dependencies

- The owner's ruling of 2026-09-29.

## Execution Sequence

1. W1: Rename the key in Compose, `.env.example`, `.env`, GDE-0028, the
   `mng-db` README, and the m0021 row (criterion 1).
2. W2: Classify Tempo and Pyroscope as `HOME` in AD-0006, GDE-0047, POL-0047,
   GDE-0049, POL-0049, POL-0021, the three observability READMEs, and the
   m0021 rows (criterion 2).
3. W3: Run Compose validation, the full gate, and both unit suites
   (criterion 3).

## Risk and Rollback

Each work unit is one commit; reverting it restores the previous key or
wording. The `.env` rename is reversed by renaming the key back.

## Verification

- `git grep VALKEY_MNG_HOST_POST` and a key-order comparison of the two
  environment files.
- `validate-docker-compose.sh`, `run-ci-gate.py --profile full`, `tests/lib`,
  and `tests/validation`.

## Rulings

None yet.
