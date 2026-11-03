---
title: "Archive and Migration Check Retirement Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-03"
layer: "specs"
artifact_id: "SPEC-0248-TSK-0001"
parent_ids:
- "SPEC-0248-PLAN-0001"
created: "2026-11-03"
---

# Archive and Migration Check Retirement Task

## Overview

### Objective

Implement W1–W5: remove every gate that validates Stage 98, keep the
non-archive checks beside it, and inventory what still reads Stage 98.

## Inputs and Authorization

The user directed that CI/CD checks of `docs/98.archive/` files and records be
minimized and preferably deleted, that the related migration checks be deleted
too, including the archive link checks, and that the legacy allowances that keep
accepting existing metadata deficits be made removable later. Stage 98 bodies
are not edited here; the user scheduled their removal as a later phase that
keeps only the folder structure and README. Exclusions: no push, pull request,
or merge from this Task.

## Work Log

### Current contract decision

The user's direction authorizes this Spec and Plan as written. It does not
authorize removing Stage 98 bodies, which is the next phase.

### Current readiness and execution

Inputs, work units and checks are recorded here. The Task is ready and in
progress under the approved parents. Hosted CI has not run.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0248 | draft | approved | #current-contract-decision |
| SPEC-0248-PLAN-0001 | draft | approved | #current-contract-decision |
| SPEC-0248-TSK-0001 | draft | ready | #current-readiness-and-execution |
| SPEC-0248-TSK-0001 | ready | in-progress | #current-readiness-and-execution |

### Removed

- Modules: `archive_assessments.py`, `archive_snapshots.py`,
  `lifecycle/recovery.py`, `lifecycle/promoted.py`.
- `archive.py`: Retention Catalog, coverage, identity and retention
  validators; Tombstone parsing and the strict `load_archive`; preservation
  boundary; recovery rows. It keeps only read-only loaders.
- `archive_migration_0003.py`: the task10 ledger rows and recovery and
  preservation-decision loaders.
- Metadata: every Stage 98 record is skipped by `validate_record`; the legacy
  archive route-type alias and its source binding, the 0003 compaction witness,
  and the task10 moved-body baseline are gone.
- Links: the historical-link pass, archive assessment and route contexts,
  `archive-assessment-link`, `active-archive-link`, and the archive direct-link
  metric. Outbound links from Stage 98 are not checked; a link into it is
  checked for target integrity only.
- Corpus lifecycle: the archive recovery and promoted (DATA-0067) checks, and
  the archive provenance check on manifest archive targets.
- Tests and gates: the archive, assessment, catalog, snapshot, recovery and
  promoted suites, archive-only cases in the link, reference, lifecycle and
  validator suites, their workflow-contract selectors, and `docs/98.archive/`
  in the document suite path trigger.
- Legacy: the code-based legacy deficit allowance
  (`missing-required-key`, `replacement-free-supersession`, `stale-active`
  with `MIGRATION_TYPED_KEYS` and `APPROVED_MIGRATION_PATHS`), whose inventory
  was zero, and the `--profiles` transition alias of the metadata and corpus
  lifecycle CLIs, whose only callers were tests.

### Kept and moved

- Active-stage occupancy and Task cancellation moved to
  `lifecycle/occupancy.py` and still run from the corpus lifecycle route.
- The incident corrective-owner lookup moved into `operations_catalog.py`.
- `spec_packages._recorded_retirements` now uses
  `archive.recorded_retired_paths`, a lenient reader that grants no exemption
  for a record it cannot parse.

### Remaining Stage 98 readers

Each reader below is read-only and raises no archive finding. The next phase,
which removes the Stage 98 bodies, must replace or drop each one first.

| Reader | Files read | Used by | Replacement before body removal |
| --- | --- | --- | --- |
| `archive.recover_legacy_parent_identities` | `migrations/0001-sdlc-taxonomy-convergence.md` | link-only legacy allowance in `metadata/reference.py` | drop with the allowance below |
| `metadata/lifecycle._task5_move_body_sources` and `_task5_moved_body_baseline` | `migrations/0001-sdlc-taxonomy-convergence.md` | changed-body baseline for documents moved by mig-0001 | drop; every mig-0001 move is long merged |
| `archive_migration_0003._migration_document` | `migrations/0003-workspace-governance-simplification.md`, `retired/90.references/data/0067-foundation/data.yaml` | `metadata/profile.build_current_manifest` keeps retired SPEC IDs resolvable | inline the retired SPEC ID map into a tracked Stage 99 input |
| `archive_migration_0003._approved_migration_document` | the 0003 ledger at its approved commit | `identity_history` rename rows and high-water bootstrap | read the ledger from Git history only, or inline the rows |
| `metadata/reference.py` Spec lifecycle gate | existence of `migrations/0003-workspace-governance-simplification.md` | enables Spec Package lifecycle validation | remove the existence condition; otherwise lifecycle validation silently stops |
| `archive.recorded_retired_paths` | `tombstones/*/*.md`, `retention-catalog.md`, `retired/` | `spec_packages._recorded_retirements` | record retired Stage 03 paths in a tracked input, or drop the exemption |
| `requirements._tombstoned_requirement_ids` | `tombstones/01.requirements/` | Stage 01 numbering gaps | move the gap list to the Registry `reserved_history` |
| `spec_packages._load_preserved_spec_packages("completed")` | `completed/03.specs/` | branch-integration receipts | drop or read from Git history |
| `requirement_recovery` | `completed/03.specs/0180-home-dev-convergence/tasks/` | requirement allocation recovery | inline the recovered decisions |
| `architecture.load_preserved_architecture_documents` | `superseded/02.architecture/` | ADR supersession predecessors | resolve predecessors from Git history or the Registry |
| `identity_history` issued-identity scan | every tracked path under `docs/98.archive/` | identities issued count as used | keep counting from Git history |
| link alignment | targets under `docs/98.archive/` named by current documents | ordinary target integrity | remove or repoint those links |

`registry.preserved_origin_path` maps a path and reads no file. The archive
structure and scheme stay defined by `docs/98.archive/README.md`, the Registry
`common.archive_retention` block, `archive_disposition_model`, the `migration`,
`tombstone`, `archive-retention-catalog` and `archive-record-*` profiles, and the
templates under `docs/99.templates/templates/archive/`.

### Legacy and deprecated backlog

| Item | Current inventory | Reason kept | Removal condition |
| --- | --- | --- | --- |
| Link-only legacy deficit allowance (`_legacy_exception_evidence`) | 0 excused deficits in the corpus report; 0 on this change | a link-only rewrite of a document with base deficits would otherwise fail | remove with `recover_legacy_parent_identities` once no change needs it |
| `frozen-legacy-status` Registry exception and `declares_frozen_legacy_*` | 1 profile (`migration`) | removing it changes Registry validation and its routing tests | remove with the Stage 98 bodies |
| `metadata_validator.py` compatibility facade | imported by validators and tests | public import surface of the split validator | remove when callers import the split modules directly |
| Generation 5–7 Spec migration, terminal Task immutability, transition overrides | in use by current Spec packages | current lifecycle contracts | out of scope |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W1 | metadata-changed | worktree against origin/main ac573aaa1 before the Stage 03 package | PASS | selected 4, zero violations, zero legacy exceptions | required | - |
| E2 | 3 | W4 | metadata-report | worktree corpus | PASS | only finding: 8 unsupported-profile, which no allowance excuses | required | - |
| E3 | 1, 2 | W2 | governance-unit-tests | tests/lib/document_governance discovery | FAIL | 761 tests: 6 failures, 2 errors from tests still naming removed archive helpers and archive-only fixtures | required | - |
| E4 | 1, 2 | W2 | governance-unit-tests | the eight failing modules plus archive readers and lifecycle tests after test updates | PASS | 361 tests OK | required | E3 |
| E5 | 4 | W5 | gate-and-manifest-tests | lifecycle, gate, surface ownership, Script Manifest, CI gate plan, CI routing and validator entrypoint suites | FAIL | 263 tests: lifecycle public expected the removed recovery line; one process-cleanup test; one selector named a module absent from main | required | - |
| E6 | 4 | W5 | gate-and-manifest-tests | lifecycle public after its expectation update and the process-cleanup test alone | PASS | lifecycle public passed in E4; process-cleanup test passed on rerun | required | E5 |
| E7 | 1, 2 | W2 | corpus-lifecycle | worktree with this package | PASS | document corpus lifecycle zero violations; active stage occupancy zero violations | required | - |
| E8 | 1 | W3 | document-links | alignment mode | PASS | 1181 documents, 9586 links, zero failures and warnings | required | - |
| E9 | 4 | W5 | metadata-changed | worktree with this package against origin/main ac573aaa1 | PASS | selected 8, zero violations, zero legacy exceptions | required | - |
| E10 | 4 | W5 | script-manifest | worktree before new files were staged | FAIL | three path-untracked and tests-untracked failures for the new occupancy module and tests | required | - |
| E11 | 4 | W5 | script-manifest | after the code commit staged the new files | PASS | script manifest is valid | required | E10 |
| E12 | 4 | W5 | staged-precommit | `run-ci-precommit.sh --mode local-staged` before each commit | PASS | no failing hook | required | - |
| E13 | 4 | W5 | post-rebase-checks | branch rebased onto origin/main 355e8caa1 (PR #720 merged) | PASS | metadata check-changed selected 8 zero violations; corpus lifecycle and occupancy zero; link alignment, Script Manifest PASS; 415 surface, manifest, workflow-contract, CI gate plan, lifecycle, archive reader, operations catalog and Spec package tests OK | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | - | @buenhyden |
| 2 | pending | - | - | @buenhyden |
| 3 | pending | - | - | @buenhyden |
| 4 | pending | - | - | @buenhyden |

## Review and Completion

Local checks are recorded above. Independent review and hosted CI have not
run, and no criterion is accepted yet.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
