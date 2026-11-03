---
title: "Completed Spec Package Deletion Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-03"
layer: "specs"
artifact_id: "SPEC-0250-PLAN-0001"
parent_ids:
- "SPEC-0250"
created: "2026-11-03"
---

# Completed Spec Package Deletion Plan

## Overview

Prepare the checks first, then delete the packages and reserve their numbers,
then unlink current documents, and finally update governance and record the
evidence.

## Scope

Document-governance libraries and tests, the Registry, the Stage 03 README,
current documents that linked into deleted packages, the documentation
protocol, and this package.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 3 | Drop the SPEC-0211 Resolves correction; read only present packages in generation 7 admission; excuse terminal Task links into reserved packages | None | TSK-0001 | governance and lifecycle unit suites |
| W2 | 1 | Delete the fully terminal packages except the proof carriers; reserve their numbers; drop their README rows | W1 | TSK-0001 | corpus lifecycle; metadata check-changed |
| W3 | 2, 3 | Unlink current documents; drop the RUN-0098 parent; repoint test fixtures | W2 | TSK-0001 | links alignment |
| W4 | 2 | Describe the deletion rule in the documentation protocol and Stage 03 README | W2 | TSK-0001 | review against code |
| W5 | 4 | Record local results | W1–W4 | TSK-0001 | the checks above |

## Verification Plan

Run `tests/lib/document_governance`, `tests/validation/lifecycle`, the gate,
CI routing and CI gate plan suites, `test_ci_gate_evidence` under system
python3, `check-document-metadata.py` in `check-changed` and `check-active`
modes, `check-document-corpus-lifecycle.py`, `check-document-links.py` in
`alignment` and `commands` modes, `check-script-manifest.py`, and the provider
renderer `--check`.

## Risks and Recovery

### Risks and Rollback

A check that relied on a deleted package fails in its unit suite or in corpus
lifecycle, which W5 runs. Deleted bodies stay in version history. Revert the
branch to restore them; no outside state changes.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-completed-spec-package-deletion.md)
