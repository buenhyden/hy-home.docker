---
title: "Implementation Alignment Fixes Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0255-PLAN-0001"
parent_ids:
- "SPEC-0255"
created: "2026-11-04"
---

# Implementation Alignment Fixes Plan

## Overview

Correct the verified audit findings that no open branch owns, in one batch;
the findings that touch files open elsewhere wait for a second batch.

## Scope

The files named in the Spec; no runtime or remote state changes.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | AD-0026 network rows and the GDE-0077 anchor | None | TSK-0001 | links alignment |
| W2 | 2 | Rewrite present-tense pointers to deleted Specs | None | TSK-0001 | metadata check-changed |
| W3 | 3 | POL-0004 globs, REQ-0005 ownership, POL-0021 database list, SonarQube README key, secret names, provenance and audience fixes | None | TSK-0001 | metadata check-changed; links |
| W4 | 4 | Record local results | W1–W3 | TSK-0001 | the checks above |

## Verification Plan

Run `check-document-metadata.py` in `check-changed` and `check-active` modes,
`check-document-corpus-lifecycle.py`, `check-operations-catalog.py`, and
`check-document-links.py` in `alignment`, `navigation`, `language` and
`traceability` modes.

## Risks and Recovery

### Risks and Rollback

A wrong subnet or member would mislead an operator; W1 copies each value from
Compose. Revert the branch to restore the previous text; no outside state
changes.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-implementation-alignment-fixes.md)
