---
title: "Archive and Migration Check Retirement Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-03"
layer: "specs"
artifact_id: "SPEC-0248-PLAN-0001"
parent_ids:
- "SPEC-0248"
created: "2026-11-03"
---

# Archive and Migration Check Retirement Plan

## Overview

Delete archive validation from the inside out: first stop validating Stage 98
records, then delete the validators and their tests, then prune the dead code
they leave, and finally amend governance and record the inventory.

## Scope

Document-governance libraries and CLIs, their tests, the workflow contract,
the Script Manifest, governance text, Stage 99 README prose, and this package.
No Stage 98 body is edited.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Skip Stage 98 in metadata validation; remove the legacy archive type alias, compaction witness and task10 move baseline | None | TSK-0001 | metadata check-changed against main |
| W2 | 1, 2 | Delete recovery, promoted, snapshots and assessments; move occupancy and the owner lookup; replace the strict archive loader with a lenient retired-path reader | W1 | TSK-0001 | governance and lifecycle unit tests; corpus lifecycle |
| W3 | 1 | Remove archive link passes and metrics; drop archive tests and gate registrations | W2 | TSK-0001 | links alignment; workflow-contract and surface tests |
| W4 | 3 | Amend governance text; remove the `--profiles` alias; inventory readers and legacy allowances | W1–W3 | TSK-0001 | review of the inventory against code |
| W5 | 4 | Record local results | W1–W4 | TSK-0001 | the checks above |

## Verification Plan

Run the document-governance, lifecycle, gate, surface-ownership, Script
Manifest and CI gate plan unit suites; `check-document-metadata.py` in
`check-changed` mode against `origin/main`; `check-document-corpus-lifecycle.py`;
`check-document-links.py --mode alignment`; and `check-script-manifest.py`.

## Risks and Recovery

### Risks and Rollback

No gate validates a Stage 98 record any more, but an edit there is not invisible:
current checks still read the archive, and three of their readers stay
fail-closed on a malformed record until the archive-file deletion phase
replaces them (the 0003 ledger verifier behind `build_current_manifest`, the
preserved ADR loader, and the preserved Spec Package loader). `docs/98.archive/`
also stays in the document suite path trigger so an archive-only change still
runs those current checks. A non-archive check that depended on a deleted helper
would fail at import, which the unit suites catch. Revert the branch to restore
the previous gates; no outside state changes.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-archive-and-migration-check-retirement.md)
