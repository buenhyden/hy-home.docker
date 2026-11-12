---
title: "Stage 98 Archive Deletion Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0249-PLAN-0001"
parent_ids:
- "SPEC-0249"
created: "2026-11-03"
---

# Stage 98 Archive Deletion Plan

## Overview

### Goal and Boundary

Replace every Stage 98 reader first, then delete the archive files, then remove
current references and summarize the retired records, and finally update
governance and record the evidence.

Document-governance libraries and tests, the Registry, Stage 01 and Stage 02
Traceability sections, current documents that linked into Stage 98, governance
text, Stage 98 and Stage 99 READMEs, and this package.

Parent Spec:

- [Spec](spec.md)

### Assumptions

The plan works under the approved SPEC-0249; it assumes no authority beyond it.

## Dependencies

### Prerequisites

The plan needs only the approved Spec and the document-governance libraries, tests, Registry and documents named in its Goal and Boundary; it names no further external contract.

### Dependency Order

W1 has no dependency. W2 starts after W1 and W3 after W2. W4 starts after W1 to W3 and W5 after W1 to W4.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 2 | Replace Stage 98 readers with the Registry `reserved_history`; delete `archive.py`, `archive_migration_0003.py` and `requirement_recovery.py` | None | TSK-0001 | governance and lifecycle unit suites |
| W2 | 1 | Delete Stage 98 files except the README; rewrite the README as the scheme | W1 | TSK-0001 | links alignment; README checks |
| W3 | 1, 3 | Summarize Stage 01 and Stage 02 records into their owners; unlink current links; drop typed references to retired identities | W2 | TSK-0001 | metadata check-changed; links alignment |
| W4 | 3 | Update governance, knowledge, skill, Stage 99 and stage READMEs | W1–W3 | TSK-0001 | review against code |
| W5 | 4 | Record local results | W1–W4 | TSK-0001 | the checks above |

### Change and Rollback

Revert the branch to restore the files and readers; no outside
state changes.

## Verification Plan

### Verification Matrix

Run the document-governance, lifecycle, gate, surface-ownership, Script
Manifest and CI gate plan unit suites; `check-document-metadata.py` in
`check-changed` mode against the PR #722 head; `check-document-corpus-lifecycle.py`;
`check-document-links.py` in `alignment` and `commands` modes; and
`check-script-manifest.py`.

### Stage Placement

The metadata check runs in `check-changed` mode against the PR #722 head; the Plan places no other stage-specific checks, and the Task records each run.

## Risks

### Risks and Mitigations

A current check that silently depended on a deleted Stage 98 file would fail at
import or in its unit suite, which W5 runs. Removed bodies stay recoverable from
version history.

### Escalation

Work stops and returns to the owner when a required check fails or an approval is missing, per the stop rules in [docs/03.specs/AGENTS.md](../AGENTS.md).

## Promotion Map

### Durable Meaning

The lasting meaning lives in the Registry `reserved_history`, the Stage 98 README scheme and the updated governance, knowledge, skill and Stage 99 text from W1 to W4.

### Owner and Receipt

Owner @buenhyden. The receipt is the local result recorded in TSK-0001 (W5).

- [Task](tasks/tsk-0001-stage98-archive-deletion.md)
