---
title: "Archive and Migration Check Retirement Task"
version: "0.1.1"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-10"
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
  validator suites, and their workflow-contract selectors. The first change
  also removed `docs/98.archive/` from the document suite path trigger; review
  restored it (see the Kept list).
- Lifecycle contract: the `check-promoted` and `check-recovery` mode names and
  the archive, promoted-manifest and archived-blob finding codes that nothing
  can emit any more.
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
  `archive.recorded_retired_paths`, and the Stage 01 gap reader uses the same
  `archive.sealed_tombstone` contract: `type: archive/tombstone`,
  `status: sealed`, a safe retired path and a recovery commit OID. A retired
  path also needs a blob proof at that commit. A record failing the contract
  grants no exemption.
- The Spec Package contract no longer depends on the 0003 ledger existing.
- `docs/98.archive/` stays in the document suite path trigger, so an
  archive-only change still runs the current checks that read Stage 98.

### Remaining Stage 98 readers

Each reader below is read-only. The next phase, which removes the Stage 98
bodies, must replace or drop each one first. Three of them deliberately stay
fail-closed on a malformed record until then: the 0003 ledger verifier behind
`build_current_manifest`, `architecture.load_preserved_architecture_documents`,
and `spec_packages._load_preserved_spec_packages`. An edit to those records can
therefore still fail a current check.

| Reader | Files read | Used by | Replacement before body removal |
| --- | --- | --- | --- |
| `archive.recover_legacy_parent_identities` | `migrations/0001-sdlc-taxonomy-convergence.md` | link-only legacy allowance in `metadata/reference.py` | drop with the allowance below |
| `metadata/lifecycle._task5_move_body_sources` and `_task5_moved_body_baseline` | `migrations/0001-sdlc-taxonomy-convergence.md` | changed-body baseline for documents moved by mig-0001 | drop; every mig-0001 move is long merged |
| `archive_migration_0003._migration_document` | `migrations/0003-workspace-governance-simplification.md`, `retired/90.references/data/0067-foundation/data.yaml` | `metadata/profile.build_current_manifest` keeps retired SPEC IDs resolvable | inline the retired SPEC ID map into a tracked Stage 99 input |
| `archive_migration_0003._approved_migration_document` | the 0003 ledger at its approved commit | `identity_history` rename rows and high-water bootstrap | read the ledger from Git history only, or inline the rows |
| `archive.recorded_retired_paths` (sealed contract and blob proof) | `tombstones/*/*.md`, `retention-catalog.md`, `retired/` | `spec_packages._recorded_retirements` | record retired Stage 03 paths in a tracked input, or drop the exemption |
| `requirements._tombstoned_requirement_ids` (sealed contract) | `tombstones/01.requirements/` | Stage 01 numbering gaps | move the gap list to the Registry `reserved_history` |
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

### Forward dependencies for the archive-file deletion phase

- M3: removing `active-archive-link` lets a current document add a new link
  into Stage 98. Those links become broken targets when the bodies go; repoint
  or remove them in that phase.
- M4: Stage 98 records are no longer validated, but they still feed
  `build_current_manifest`, so their identities remain available to parent
  resolution of current records. Replace that input before the bodies go.

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
| E14 | 4 | W5 | gate-and-manifest-tests | the E5 selector named `tests.lib.gate.test_p03_workflow_contract`, which exists only after PR #720; reran after the rebase onto 355e8caa1 | PASS | the module loads and passes in E13 and E16 | required | E5 |
| E15 | 1, 2 | W2 | governance-library-leaf | all 16 modules of `leaf.document-governance-library-regressions` after the review fixes for I2 and M1 | PASS | 633 tests OK | required | - |
| E16 | 4 | W5 | lifecycle-metadata-gate-suites | lifecycle (4 modules), metadata reference, lifecycle, heading and profile, surface ownership, Script Manifest, workflow contracts (github, p03, p11), CI gate plan, CI routing and validator entrypoints after I1 | FAIL | 416 tests: 4 OpenAPI fixture failures, because Spec Package validation now ran in fixtures with no Stage 03 or Registry history | required | - |
| E17 | 4 | W5 | lifecycle-metadata-gate-suites | metadata reference, github workflow contract, CI gate plan and surface ownership after gating Spec validation on current Stage 03 | PASS | 138 tests OK | required | E16 |
| E18 | 4 | W5 | gate-evidence | `tests.lib.gate.test_ci_gate_evidence` with system python3, because the uv Python lacks `fcntl.F_ADD_SEALS` | PASS | 21 tests OK | required | - |
| E19 | 1 | W3 | document-commands | links `commands` mode after the archive module removal | FAIL | 8 failures: 6 in completed SPEC-0209-TSK-0001 naming removed archive modules, and 2 for ignored `_workspace` files absent from this worktree | required | - |
| E20 | 1 | W3 | document-commands | after exempting terminal Task bodies; links, owner lookup and lifecycle contract tests | FAIL | 105 tests OK; commands mode still reports 2 findings, both for ignored `_workspace` files from PR #720 that are absent from this worktree; baseline debt not caused by this change, and commands mode runs only locally | required | - |
| E21 | 1, 2 | W2 | corpus-lifecycle-and-links | after the review fixes | PASS | corpus lifecycle zero; occupancy zero; link alignment PASS; Script Manifest PASS | required | - |
| E22 | 4 | W5 | metadata-changed | final tree after the review fixes, base origin/main 355e8caa1 | PASS | selected 8, zero violations, zero legacy exceptions | required | - |
| E23 | 4 | W5 | hosted-ci | CI Quality Gates run 41595209280 on head a879f2b64 | PASS | candidate-quality success; main-security skipped by its trigger | required | - |
| E24 | 4 | W5 | full-suite-comparison | `tests/lib` and `tests/validation` discovery on a879f2b64 against main ec8555d09, system python3 | FAIL | lib 1053 tests, validation 2179; every failure also fails on main (15 secret metadata sync, 1 SMTP, 3 loader errors, 1 identity history) except 11 that read live `docs/03.specs` while a commit landed mid-run, and one lifecycle public test broken by the E23 row shape, since corrected | required | - |
| E25 | 4 | W5 | quiet-tree-rerun | `test_spec_packages`, `test_requirements`, lifecycle `test_public` on the corrected tree with no concurrent writes | PASS | 122 tests OK; corpus lifecycle zero; metadata check-changed selected 7, zero violations | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | - | @buenhyden |
| 2 | pending | - | - | @buenhyden |
| 3 | pending | - | - | @buenhyden |
| 4 | pending | - | - | @buenhyden |

## Review and Completion

Local checks are recorded above. Independent review of PR #721 requested
changes (I1–I6, M1–M5); they are addressed in this branch and recorded in the
Evidence table, with M3 and M4 kept as forward dependencies. Hosted CI for the
corrected head has not run, and no criterion is accepted yet.

### Merge receipt 2026-11-10

Recorded 2026-11-10 from `gh pr view`: #721 merge `ec8555d09` at
2026-11-03T06:33:54Z; #722 merge `b9fdd67d4` at 2026-11-03T08:12:37Z; #723
merge `85904818e` at 2026-11-03T13:14:59Z. Hosted checks on the merged PR:
every completed check SUCCESS, the rest SKIPPED, none failing. Candidate
quality: the merged change is a candidate that passed hosted CI. This receipt
is not owner acceptance: no criterion is accepted and the status is unchanged.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
