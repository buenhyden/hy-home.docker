---
title: "Archive and Migration Check Retirement Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0248-PLAN-0001"
parent_ids:
- "SPEC-0248"
created: "2026-11-03"
---

# Archive and Migration Check Retirement Plan

## Overview

### Goal and Boundary

Delete archive validation from the inside out: first stop validating Stage 98
records, then delete the validators and their tests, then prune the dead code
they leave, and finally amend governance and record the inventory.

Document-governance libraries and CLIs, their tests, the workflow contract,
the Script Manifest, governance text, Stage 99 README prose, and this package.
No Stage 98 body is edited.

Parent Spec:

- [Spec](spec.md)

### Assumptions

The plan works under the approved SPEC-0248; it assumes no authority beyond it.

## Dependencies

### Prerequisites

The plan needs only the approved Spec and the document-governance libraries, tests, checks and documents named in its Goal and Boundary; it names no further external contract.

### Dependency Order

W1 has no dependency. W2 starts after W1 and W3 after W2. W4 starts after W1 to W3 and W5 after W1 to W4.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Skip Stage 98 in metadata validation; remove the legacy archive type alias, compaction witness and task10 move baseline | None | TSK-0001 | metadata check-changed against main |
| W2 | 1, 2 | Delete recovery, promoted, snapshots and assessments; move occupancy and the owner lookup; replace the strict archive loader with a lenient retired-path reader | W1 | TSK-0001 | governance and lifecycle unit tests; corpus lifecycle |
| W3 | 1 | Remove archive link passes and metrics; drop archive tests and gate registrations | W2 | TSK-0001 | links alignment; workflow-contract and surface tests |
| W4 | 3 | Amend governance text; remove the `--profiles` alias; inventory readers and legacy allowances | W1–W3 | TSK-0001 | review of the inventory against code |
| W5 | 4 | Record local results | W1–W4 | TSK-0001 | the checks above |

### Change and Rollback

Revert the branch to restore
the previous gates; no outside state changes.

## Verification Plan

### Verification Matrix

Run the document-governance, lifecycle, gate, surface-ownership, Script
Manifest and CI gate plan unit suites; `check-document-metadata.py` in
`check-changed` mode against `origin/main`; `check-document-corpus-lifecycle.py`;
`check-document-links.py --mode alignment`; and `check-script-manifest.py`.

### Stage Placement

The metadata check runs in `check-changed` mode against `origin/main`; the Plan places no other stage-specific checks, and the Task records each run.

## Risks

### Risks and Mitigations

No gate validates a Stage 98 record any more, but an edit there is not invisible:
current checks still read the archive, and three of their readers stay
fail-closed on a malformed record until the archive-file deletion phase
replaces them (the 0003 ledger verifier behind `build_current_manifest`, the
preserved ADR loader, and the preserved Spec Package loader). `docs/98.archive/`
also stays in the document suite path trigger so an archive-only change still
runs those current checks. A non-archive check that depended on a deleted helper
would fail at import, which the unit suites catch.

### Escalation

Work stops and returns to the owner when a required check fails or an approval is missing, per the stop rules in [docs/03.specs/AGENTS.md](../AGENTS.md).

## Promotion Map

### Durable Meaning

The lasting meaning lives in the amended governance text, the workflow contract, the Script Manifest and the Stage 99 README prose that W4 updates.

### Owner and Receipt

Owner @buenhyden. The receipt is the local result recorded in TSK-0001 (W5).

- [Task](tasks/tsk-0001-archive-and-migration-check-retirement.md)
