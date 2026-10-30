---
title: "Offline Hermes Candidate Validator Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-30"
layer: "specs"
artifact_id: "SPEC-0247-PLAN-0001"
parent_ids:
- "SPEC-0247"
created: "2026-10-30"
---

# Offline Hermes Candidate Validator Plan

## Overview

Implement one read-only Python entrypoint with deterministic v1 checks. Use
synthetic TDD fixtures; keep the producer and runtime outside this repository.

## Scope

Only Stage 03 records, registry/navigation, CLI, Script Manifest, and focused
tests. No service or remote integration.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 2 | Write synthetic CLI tests first; validate identity, shape, statuses and URL evidence | None | TSK-0001 | Focused RED then GREEN pytest |
| W2 | 2, 3 | Validate optional staged source bytes and preserve infra BLOCKED boundary | W1 | TSK-0001 | Focused RED then GREEN pytest |
| W3 | 4 | Register validator, update Stage 03 navigation/identity and record evidence | W1, W2 | TSK-0001 | Document, manifest, style and link gates; diff review |

## Verification Plan

Run `python3 -m pytest -q tests/validation/test_hermes_candidate_validator.py`,
`python3 scripts/validation/check-script-manifest.py`, scoped metadata and
corpus identity validation, and changed-document links. Run the relevant
staged gate only if its prerequisites are available. No network-backed suite
is evidence for this offline capability.

## Risks and Recovery

### Risks and Rollback

A syntactically valid candidate can still contain unverified claims. Output
therefore says preflight, never publish approval. Optional staging cannot prove
execution DB provenance or actual email delivery. Revert the local commit to
remove this reader; no outside state requires rollback.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-offline-hermes-candidate-validator.md)
