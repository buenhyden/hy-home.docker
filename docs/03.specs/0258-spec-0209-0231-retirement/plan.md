---
title: "SPEC-0209 and SPEC-0231 Retirement Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0258-PLAN-0001"
parent_ids:
- "SPEC-0258"
created: "2026-11-04"
---

# SPEC-0209 and SPEC-0231 Retirement Plan

## Overview

Move the migration proof source to the generation 6 revision first, prove it
with tests, then delete the two packages and update the documents.

## Scope

The files named in the Spec; no runtime or remote state changes.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 2 | Read migration proofs from the generation 6 revision; add tests | None | TSK-0001 | spec package tests |
| W2 | 3 | Delete both packages, reserve 209 and 231, update the index and the documentation protocol | W1 | TSK-0001 | metadata check-changed; links |
| W3 | 4 | Record local results | W1–W2 | TSK-0001 | the checks above |

## Verification Plan

Run `check-document-metadata.py` in `check-changed` and `check-active` modes,
`check-document-corpus-lifecycle.py`, `check-document-links.py` in
`alignment`, `navigation`, `language`, `traceability`, `entrypoint` and
`commands` modes, the spec package, Registry and identity history tests, and
the full `tests/lib/document_governance` discovery.

## Risks and Recovery

### Risks and Rollback

A proof read from the wrong revision would admit the wrong Tasks; W1's tests
fail closed when the proof is absent. Revert the branch to restore both
packages and the loader; no outside state changes.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-spec-0209-0231-retirement.md)
