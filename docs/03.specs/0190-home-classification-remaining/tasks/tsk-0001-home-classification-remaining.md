---
title: "Remaining HOME Classification"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190-TSK-0001"
parent_ids:
- "SPEC-0190"
- "SPEC-0190-PLAN-0001"
created: "2026-09-29"
---

# Remaining HOME Classification

## Objective

Execute W1 and W2 of the [Plan](../plan.md) and record the evidence for every
acceptance criterion of [SPEC-0190](../spec.md).

## Inputs

- The Deferred Item of the SPEC-0189 Task.
- The owner's request of 2026-09-29 to resolve the same `OPTIONAL` and `HOME`
  mismatch for the three remaining services.
- The resolved HOME selection: `docker compose config --services` with the
  POL-0078 HOME profiles lists 44 services, including `registry`,
  `dcgm-exporter`, and `seaweedfs-s3`.

## Work Log

- 2026-09-29: Spec, Plan, and Task drafted on branch
  `fix/home-classification-remaining`.

## Verification Evidence

Not started.

## Review Evidence

None yet.

## Commit Ledger

None yet.

## Rulings

- 2026-09-29: Owner ruled to resolve the mismatch; the HOME selection decides
  it.
