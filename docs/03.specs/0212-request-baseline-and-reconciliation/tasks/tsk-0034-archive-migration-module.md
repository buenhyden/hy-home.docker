---
title: "Archive Migration Module Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0034"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Archive Migration Module Task

## Overview

### Objective

Execute W50: move the Migration 0003 cutover proof out of the general Stage 98
archive module (request lines L113, L126, L132) without changing what any
check proves. This Task owns criterion 45 only.

## Inputs and Authorization

On 2026-10-29 the owner asked for every gap offered after TSK-0029 to be
done. `quality-standards.md` keeps proof readers for preserved bytes even when
their inputs are historical, so removing or skipping the proof was not an
option. Given that, the owner chose to separate the module instead of keeping
it as it was. The input is `main` at merged PR #630. The authorization covers
this refactor, this branch, its pull request, and merge.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0034 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0034 | ready | in-progress | #objective |
| SPEC-0212-TSK-0034 | in-progress | completed | #evidence |

### Change

- `scripts/lib/document_governance/archive_migration_0003.py` now holds the 21
  definitions used only for Migration 0003:
  - the frozen digest, approved commit, one-time verifier paths, historical
    session Specs, and the Task 10 baseline, first row, last row, and row
    fields;
  - the readers that parse, approve, and project the ledger, check the
    275-row Task 10 selection, and load its recovery references and
    preservation decisions.
- An AST pass confirmed that no remaining definition in `archive.py` uses any
  moved name. The dependency now runs one way: the new module uses
  `archive.<helper>`, and `archive.py` imports nothing from it. Calling
  through the module also keeps existing test patches on archive helpers
  working.
- The five importers now import the new module: `identity_history.py`,
  `lifecycle/promoted.py`, `lifecycle/recovery.py`, `metadata/heading.py`,
  and `metadata/profile.py`. So do four test files. `scripts/manifest.yaml`
  registers the new module and updates `archive.py`'s consumers.
- No check was removed or skipped, and no proof changed.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Archive behavior parity | 45 | W50 | `check-document-corpus-lifecycle.py` on `main` and on this branch | Both trees | PASS | Same output: migrations=5, tombstones=140, preserved=111, decisions=286, recovery_rows=374, violations=0 | required | - |
| Affected suites | 45 | W50 | `python3 -m unittest tests.lib.document_governance.test_archive tests.lib.document_governance.test_metadata_validator tests.lib.document_governance.test_identity_history tests.lib.document_governance.lifecycle.test_promoted` | This branch | PASS | 115 tests OK | required | - |
| Document governance suite | 45 | W50 | `python3 -m unittest discover -s tests/lib/document_governance -t .` | This branch | PASS | Full suite OK | required | - |
| Script manifest | 45 | W50 | `check-script-manifest.py` | This branch | PASS | Valid | required | - |
| Lint and format | 45 | W50 | `ruff check` and `ruff format --check` on `scripts/lib/document_governance` and `tests/lib/document_governance` | This branch | PASS | No findings | required | - |
| Metadata and links | 45 | W50 | `check-document-metadata.py --mode check-contracts`, `check-document-links.py --mode alignment` | This branch | PASS | 0 violations, 0 failures | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 45 | accepted | Archive behavior parity, Affected suites, Document governance suite, Script manifest, Lint and format, Metadata and links | The Migration 0003 proof lives in its own module, the general archive module holds no value of that migration, and every check proves the same as before. | SPEC-0212 TSK-0034 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Request line meaning audit](tsk-0029-request-line-meaning-audit.md)
