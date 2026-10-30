---
title: "Offline Hermes Candidate Validator Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-30"
layer: "specs"
artifact_id: "SPEC-0247-TSK-0001"
parent_ids:
- "SPEC-0247-PLAN-0001"
created: "2026-10-30"
---

# Offline Hermes Candidate Validator Task

## Overview

### Objective

Implement W1–W3 and record each observable criterion separately.

## Inputs and Authorization

The user authorized offline-only validator code, synthetic tests, Stage 03
package and registry/README, Script Manifest, and local logical commits.
Explicit exclusions: Docker service, server transfer, Blog-data writes,
Cron/email changes, git push, credentials or private live input.

## Work Log

The producer contract was read at
`/home/hyunyoun/storage/research/hermes-report-export/README.md` and its
`export.py`; no files there are changed. Draft Spec and Plan record the scope,
without asserting a separate human approval of their documents. Implement
TDD slices and record observed outputs below.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1, 2 | W1 | focused-tests | synthetic v1 fixtures; uv run --with pytest ... -q | PASS | 33 passed | required | - |
| E2 | 2, 3 | W2 | staged-and-infra-tests | same focused suite; real read-only batch with --source-root and --item-root | PASS | 5? use output | required | - |
| E3 | 4 | W3 | repository-gates | manifest and metadata check-active and entrypoint/navigation links and check-changed | PASS (against merge-base HEAD) | manifest PASS; check-active 495/0; links PASS; check-changed 0 violations | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | accepted | E1 | - | @buenhyden |
| 2 | accepted | E1-E2 | - | @buenhyden |
| 3 | accepted | E2 | - | @buenhyden |
| 4 | accepted | E3 | check-changed 0 violations | @buenhyden |

## Review and Completion

Pending focused tests, local registered checks, exact diff and local commits.
No deployment or remote publication is authorized or claimed.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
