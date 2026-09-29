---
title: "HOME Classification and Valkey Key"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0189-TSK-0001"
parent_ids:
- "SPEC-0189"
- "SPEC-0189-PLAN-0001"
created: "2026-09-29"
---

# HOME Classification and Valkey Key

## Objective

Execute W1 through W3 of the [Plan](../plan.md) and record the evidence for
every acceptance criterion of [SPEC-0189](../spec.md).

## Inputs

- The two Deferred Items of the SPEC-0188 Task.
- The owner's request of 2026-09-29 to fix the `VALKEY_MNG_HOST_POST` spelling
  and to unify the Tempo and Pyroscope `OPTIONAL` and `HOME` wording.

## Work Log

- 2026-09-29: Spec, Plan, and Task drafted on branch
  `fix/home-classification-and-valkey-key`.

## Verification Evidence

Not started.

## Review Evidence

None yet.

## Commit Ledger

None yet.

## Rulings

- 2026-09-29: Owner ruled to fix the key spelling and to unify the Tempo and
  Pyroscope classification; POL-0078's later HOME selection decides it.

## Deferred Items

- `registry`, `dcgm-exporter`, and `seaweedfs-s3` are `OPTIONAL` in the m0021
  inventory while their profiles are in HOME.
