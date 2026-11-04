---
title: "Analytics Labs Migration Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0262-PLAN-0001"
parent_ids:
- "SPEC-0262"
created: "2026-11-04"
---

# Analytics Labs Migration Plan

## Overview

Move the services into LAB entrypoints, then reconcile every reference and
record the checks.

## Scope

The files named in the Spec; no runtime or remote state changes.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 2 | Write the LAB entrypoints, move assets, drop root includes and unused secrets | None | TSK-0001 | compose config; LAB isolation tests |
| W2 | 3 | Update tests, hardening, catalogs, ledger, READMEs and Stage 01/02 statements | W1 | TSK-0001 | unit tests; hardening |
| W3 | 4 | Move the Stage 05 documents to `15-labs` and update their claims | W1 | TSK-0001 | operations catalog; metadata; links |
| W4 | 5 | Record local results | W1-W3 | TSK-0001 | the checks above |

## Verification Plan

Run `docker compose config` for the root and each LAB, the full unit suite,
`check-all-hardening.sh`, `check-document-metadata.py` in `check-changed` and
`check-active` modes, `check-document-links.py --mode all`,
`check-document-corpus-lifecycle.py`, `check-operations-catalog.py` and
`check-script-manifest.py`.

## Risks and Recovery

### Risks and Rollback

A LAB cannot reach its HOME dependency without an approved endpoint; the
Task records this as an owner decision. Revert the branch to restore the root
includes.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-analytics-labs-migration.md)
