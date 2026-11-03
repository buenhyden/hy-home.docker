---
title: "Stage 98 Archive Deletion Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-03"
layer: "specs"
artifact_id: "SPEC-0249-PLAN-0001"
parent_ids:
- "SPEC-0249"
created: "2026-11-03"
---

# Stage 98 Archive Deletion Plan

## Overview

Replace every Stage 98 reader first, then delete the archive files, then remove
current references and summarize the retired records, and finally update
governance and record the evidence.

## Scope

Document-governance libraries and tests, the Registry, Stage 01 and Stage 02
Traceability sections, current documents that linked into Stage 98, governance
text, Stage 98 and Stage 99 READMEs, and this package.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 2 | Replace Stage 98 readers with the Registry `reserved_history`; delete `archive.py`, `archive_migration_0003.py` and `requirement_recovery.py` | None | TSK-0001 | governance and lifecycle unit suites |
| W2 | 1 | Delete Stage 98 files except the README; rewrite the README as the scheme | W1 | TSK-0001 | links alignment; README checks |
| W3 | 1, 3 | Summarize Stage 01 and Stage 02 records into their owners; unlink current links; drop typed references to retired identities | W2 | TSK-0001 | metadata check-changed; links alignment |
| W4 | 3 | Update governance, knowledge, skill, Stage 99 and stage READMEs | W1–W3 | TSK-0001 | review against code |
| W5 | 4 | Record local results | W1–W4 | TSK-0001 | the checks above |

## Verification Plan

Run the document-governance, lifecycle, gate, surface-ownership, Script
Manifest and CI gate plan unit suites; `check-document-metadata.py` in
`check-changed` mode against the PR #722 head; `check-document-corpus-lifecycle.py`;
`check-document-links.py` in `alignment` and `commands` modes; and
`check-script-manifest.py`.

## Risks and Recovery

### Risks and Rollback

A current check that silently depended on a deleted Stage 98 file would fail at
import or in its unit suite, which W5 runs. Removed bodies stay recoverable from
version history. Revert the branch to restore the files and readers; no outside
state changes.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-stage98-archive-deletion.md)
