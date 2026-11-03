---
title: "Stage 98 Archive Deletion Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-03"
layer: "specs"
artifact_id: "SPEC-0249-TSK-0001"
parent_ids:
- "SPEC-0249-PLAN-0001"
created: "2026-11-03"
---

# Stage 98 Archive Deletion Task

## Overview

### Objective

Implement W1–W5: delete the Stage 98 files except the README, summarize their
still-current substance into Stage 01 and Stage 02, remove every reader and
reference, and keep retired numbers in the Registry.

## Inputs and Authorization

The user directed that the files under `docs/98.archive/` be deleted, keeping
only the folder scheme and README; that the deleted content be summarized into
the matching `docs/01.requirements/` and `docs/02.architecture/` documents; and
chose "remove references and keep a minimal ID list" over pinned Git reads or a
full Registry migration. The coordinator added the PR #722 re-review items N2,
N3, N4, N6 and N7 to this phase. Exclusions: completed Spec packages in
`docs/03.specs/` (next phase); no push, pull request, or merge from this Task.

## Work Log

### Current contract decision

The user's direction authorizes this Spec and Plan as written.

### Current readiness and execution

Inputs, work units and checks are recorded here. The Task is ready and in
progress under the approved parents. Hosted CI has not run.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0249 | draft | approved | #current-contract-decision |
| SPEC-0249-PLAN-0001 | draft | approved | #current-contract-decision |
| SPEC-0249-TSK-0001 | draft | ready | #current-readiness-and-execution |
| SPEC-0249-TSK-0001 | ready | in-progress | #current-readiness-and-execution |

### Summary map

| Deleted record | Summary location |
| --- | --- |
| REQ-0014 … REQ-0022 (optimization hardening Tombstones) | Traceability of REQ-0002, 0003, 0004, 0006, 0007, 0008, 0009, 0010, 0012 |
| SPEC-0001 … SPEC-0012 domain Spec Tombstones | Traceability of REQ-0001 … REQ-0012 |
| Terraform guide, policy and runbook (retired operations 0068) | Traceability of REQ-0010 |
| ADR-0003, ADR-0018 | Related Documents of ADR-0050 |
| ADR-0015 | Traceability of ADR-0039 |
| ADR-0019 | Traceability of ADR-0040 |
| ADR-0027, ADR-0029 | Traceability of ADR-0032 |
| ADR-0030, 0031, 0033, 0035, 0036 (archive model) | Traceability of ADR-0037 |
| AD-0014 | Traceability of AD-0002 |
| Completed and superseded Spec packages, operations and reference Tombstones, migrations 0001–0005, Retention Catalog, DATA-0067 | Process history only; nothing carried forward |

### Removed

- 263 files under `docs/98.archive/`; only `README.md` remains, rewritten as the
  disposition scheme.
- `archive.py`, `archive_migration_0003.py`, `requirement_recovery.py` and
  `test_archive_readers.py`; their Script Manifest rows and gate selector.
- Readers: the Stage 01 Tombstone gap reader (N2), the sealed Tombstone and
  retired-path reader (N3), the retired SPEC lineage recovery in
  `build_current_manifest`, the 0003 rename and Registry bootstrap branches in
  allocation transition, the 0001 legacy parent identities, the task5 move
  baseline, the link-only legacy exception, the preserved ADR loader, the
  preserved completed Spec loader, the pinned REQ-0012 allocation recovery, and
  the preserved decision-Task branch of identity recovery.
- Stage 98 skips in metadata validation, README runtime checks, link alignment,
  README navigation and the commands check; the `frozen-legacy-status`
  exception and its readers; the unreachable archive-field branch of metadata
  validation (N7).
- Markdownlint ignores for Stage 98 paths.

### Kept and changed

- Registry: `reserved_history` added to the requirement (9 numbers), ADR (14),
  architecture-description (5) and Spec (207) spaces. Requirement gaps and
  Stage 03 removal records read it. A Stage 03 removal reads the Registry of
  the root under check and fails closed when that file is missing, a symlink,
  unreadable or invalid; before this a fixture root inherited this
  repository's reserved numbers.
- The branch-integration handoff and the ordinary-preservation exemption were
  deleted with their Stage 98 tree readers (I1). A Stage 03 removal is
  legitimate only when its Spec number is reserved; `branch_integration_receipts`
  is still parsed, and a malformed or unsafe receipt still fails at load, but a
  receipt grants nothing.
- Corpus occupancy fails on any tracked file under `docs/98.archive/` other than
  its README (I1).
- Stage 01 gaps read the checked root's Registry when no Registry is passed
  (M2), and a top-level `reserved_history` cannot drop a number its trusted base
  reserved (M1). The unread `requirement_allocation_recovery_decisions` field was
  removed from the Registry and the frontmatter schema (M3).
- REQ-0026 (3.0.0) and AD-0030 (3.0.0) describe summarize-and-delete; REQ-0026
  retired its Tombstone namespace, immutable capture and one-capture-record
  items. ADR-0051 supersedes ADR-0037 decision items 4 to 10 and the last
  sentence of decision 1, recorded in prose on both sides because typed
  supersession would mark all of ADR-0037 superseded (I3, I4, N2).
- Every top-level identity space now records `reserved_history`, including
  operations subjects, incidents, research, audits, data, migrations, and
  Tombstones (N3). The dead `archive_disposition_model` switch is removed (m4).
- Occupancy reads the tracked inventory with `git ls-files -z` and fails closed
  when it cannot (m2).
- The pre-commit `frozen_archive_payloads` anchor now names only the
  `completed/`, `superseded/` and `retired/` roots, matching the Registry
  after the `frozen-legacy-status` exception was removed.
- Incident closure keeps its identifier checks, now local to
  `operations_catalog.py`.
- The commands check keeps the terminal-Task exemption but keys it on the
  Registry Task path profile (N4), documented in documentation protocol rule 15
  with a negative test.
- Identity history still scans version history under `docs/98.archive/`, which
  needs no file in the tree.
- The archive scheme definitions stay: `PRESERVED_*` path constants,
  `common.archive_retention`, the archive profiles and templates.

### Reference cleanup

- 119 markdown links into Stage 98 in 69 current documents were turned into
  plain text.
- 11 typed references to retired identities were removed or repointed: six
  `supersedes` entries on ADR-0032, 0037, 0039, 0040, 0050 and AD-0002, and four
  `parent_ids` from SPEC-0094 or SPEC-0158 to REQ-0024.
- Governance (N6): documentation protocol retention section and rule 15,
  quality standards, bootstrap, task checklists, approval boundaries, repository
  map, incident-response skill, and the docs, Stage 99, Stage 98 and root
  READMEs.

### Test changes

Deleted only where the behavior they checked was removed by this change.
Repointed tests keep their fixture and assert the new fail-closed result.

| Test | Change | Reason | Fail-closed |
| --- | --- | --- | --- |
| `test_archive_readers.py` (module) | deleted | `archive.py` readers removed | yes; replaced by the reserved-number tests below |
| `test_registry`: `test_frozen_legacy_status_exception_is_exact` | deleted | `frozen-legacy-status` exception removed | no |
| `test_registry`: `RequirementRecoveryBoundaryTests` (3 tests) | deleted | `requirement_recovery.py` removed | yes (symlink, oversized, invalid proof); the code path no longer exists |
| `test_registry`: ADR-0035 switch binding | replaced | ADR-0035 file deleted; now asserts the number is reserved | no |
| `test_identity_history`: blob-once and pre-introduction base tests | replaced | pre-Registry bootstrap removed; now `test_predecessor_without_a_registry_fails_closed` | yes |
| `test_identity_history`: archived decision Task subtest | repointed | archived completed Task no longer owns a decision; all dispositions now rejected | yes |
| `test_metadata_validator`: retired Spec lineage recovery | deleted | lineage recovery removed; replaced by the reserved-only typed-reference test | yes |
| `test_requirements`: two Tombstone gap tests | replaced | gaps now come from `reserved_history`; unreserved gap still fails | yes |
| `test_links`: archive body and archive README skips | deleted | the Stage 98 skips were removed | no |
| `test_links`: hidden governance links | repointed | Stage 98 links are now checked | no |
| `test_links`: self-declared Task outside the Task path | added | N4 negative case | yes |
| `metadata/test_heading`: archive README runtime exemption | narrowed | exemption removed | no |
| `test_spec_packages`: ordinary preservation | replaced | first replaced while the preservation exemption still read Stage 98 (the earlier "preservation flow removed" note was inaccurate); I1 then deleted that exemption, and the test became `test_only_a_reserved_number_records_a_package_removal` | yes |
| `test_spec_packages`: unsafe catalog retirement | deleted | catalog reader removed; replaced by the Registry-file test | yes |
| `test_spec_packages`: catalog row retirement | deleted | Retention Catalog removed | no |
| `test_spec_packages`: positive handoff via either carrier; blocked current carrier; matching completed identity (`none`, `ambiguous`) | deleted | completed-archive carrier removed; `ambiguous` replaced by the reserved-number tests | `ambiguous` yes |
| `test_spec_packages`: ready carrier, completed identity, duplicate carrier, invalid bindings, missing origin, exact package bytes | deleted (I1) | the handoff validator was deleted; replaced by `test_a_branch_integration_receipt_grants_no_removal`, and the unsafe-path case kept as `test_an_unsafe_receipt_path_is_rejected_at_load` | yes |
| `test_spec_packages`: injected disposition sets signature | repointed | `preserved_paths` removed | no |
| `test_generation6`: ready base enters the completed archive | deleted (I1) | `_ordinary_preserved_paths` removed | no |
| `test_agent_governance_ci_routing`: frozen payload agreement | repointed | requires only the unmanaged archive profile roots | no |

Added fail-closed tests: `test_a_removal_is_recorded_only_by_a_reserved_spec_number`,
`test_a_root_without_its_own_valid_registry_grants_no_retirement` (missing,
symlink, directory), `test_a_malformed_reserved_history_grants_no_retirement`
(unsorted, out of range, not an integer),
`test_a_number_reserved_in_another_space_does_not_retire_a_spec`,
`test_a_typed_reference_to_a_reserved_only_identity_is_unresolved`, and after
the PR #723 review `test_an_archive_copy_does_not_record_an_unreserved_removal`
(I2), `test_any_tracked_stage_98_file_but_its_readme_is_a_violation` (I1),
`test_gaps_are_explained_only_by_the_checked_roots_registry` (M2), and
`test_reserved_history_cannot_drop_a_number` (M1).

### Open issues

- SPEC-0204-TSK-0001 still carries `branch_integration_receipts`; the field is
  parsed but inert, and its schema entry can go with the completed Spec package
  phase.
- The owner decided to accept ADR-0051, but the changed-document check rejects
  a new ADR that does not enter as `proposed`; no Task event or CI override can
  carry that transition. ADR-0051 therefore lands as `proposed` and moves to
  `accepted` in the first change after it merges, as ADR-0050 did.
- Review items M4 and M5 are recorded as open, as directed.
- `operations-subject` stood at high-water 102 while RUN-0103 to RUN-0106 were
  already issued; it is now 106. No check caught it because the identity
  scanner maps the `GUIDE-`, `POLICY-` and `RUNBOOK-` prefixes while issued
  operations identities use `GDE-`, `POL-` and `RUN-`, so operations numbers are
  never observed by allocation or by the new reserved-but-live check. The
  scanner now takes one prefix table from the current Registry patterns
  (`GDE-`, `POL-`, `RUN-` and the other numbered spaces), drops the stale
  `GUIDE-`, `POLICY-`, `RUNBOOK-`, `OPS-`, `REF-`, `AUDIT-` and `TOMBSTONE-`
  aliases and the bare legacy incident form, and a test fails if a numbered
  Registry prefix is not scanned.
- The final evidence rows name revision b8832d8ee or ef6046cc9; the Task-only
  commit that records them changes no checked code or Registry data.
- The archive-record metadata vocabulary in `metadata/profile.py` and the
  archive profiles stay as scheme definitions; remove them in the legacy and
  deprecated phase if no record type needs them.
- The `frozen_archive_payloads` pre-commit exclude now matches no tracked file.
  It is kept because `scripts/hooks/post-tool-validate.sh` requires the anchor
  and its hook tests read it; removing it is a hook change for a later phase.
- The commands check reports two `_workspace` paths in the frozen DATA-0096
  README; they come from PR #720 and depend on ignored local files.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 3 | W3 | document-links | alignment mode after the reference cleanup | PASS | 950 documents, 8325 links, zero failures | required | - |
| E2 | 3 | W3 | document-commands | commands mode | FAIL | 2 findings for ignored `_workspace` files that PR #720 documents; not caused by this change | required | - |
| E3 | 4 | W5 | governance-unit-tests | four batches while the tree was being edited and committed | FAIL | spec packages 91: 8 failures and 6 errors; registry group 182: 2 failures; links group 287: 2 failures; metadata and lifecycle group 270: 3 failures. Causes: tests of removed archive paths, and Stage 03 changing under the reconciliation tests during commits | required | - |
| E4 | 4 | W5 | governance-unit-tests | final quiet-tree run of all `tests/lib/document_governance` modules, `tests/validation/lifecycle` and the Script Manifest tests | FAIL | spec packages 91 OK; links, operations catalog, metadata validator and generations 286 OK; registry, requirements, identity and architecture 182 with 1 subtest failure; metadata, lifecycle, references, taxonomy and manifest 271 with 1 failure; supersedes E3 | required | - |
| E5 | 4 | W5 | gate-and-ci-routing | `tests/lib/gate` discovery, CI routing and CI gate plan under uv Python | FAIL | 283 tests: the gate evidence module needs `fcntl.F_ADD_SEALS`; two descendant-cleanup subtests under load; frozen payload agreement | required | - |
| E6 | 4 | W5 | gate-evidence | `tests.lib.gate.test_ci_gate_evidence` with system python3 | PASS | 21 tests OK | required | - |
| E7 | 4 | W5 | governance-unit-tests | the identity recovery subtest and Script Manifest tests after their fixes | PASS | all passed in a 60-test targeted rerun | required | E4 |
| E8 | 4 | W5 | metadata-active | `check-document-metadata.py --mode check-active` | PASS | 497 selected, zero violations | required | - |
| E9 | 4 | W5 | metadata-changed | `--mode check-changed --base-ref a879f2b64` | PASS | 355 selected, zero violations | required | - |
| E10 | 2 | W1 | corpus-lifecycle | `check-document-corpus-lifecycle.py --base-ref a879f2b64` | PASS | zero violations; occupancy zero | required | - |
| E11 | 4 | W5 | manifest-and-renderer | `check-script-manifest.py`; provider renderer `--check` | PASS | manifest valid; renderer drift 0 | required | - |
| E12 | 4 | W5 | staged-precommit | `run-ci-precommit.sh --mode local-staged` before each commit | PASS | no failing hook after fixing two MD032 blank lines and formatting | required | - |
| E13 | 4 | W5 | gate-and-ci-routing | frozen payload agreement and descendant cleanup after fixes, uv Python; gate evidence passes under system python3 in E6 | PASS | all passed in the same 60-test targeted rerun | required | E5 |
| E14 | 3 | W3 | metadata-changed | review fix: ADR-0034, 0039, 0040, 0042, 0044 and AD-0030 no longer claim Stage 98 preservation; pre-commit ruff comment updated | PASS | check-changed base a879f2b64: 357 selected, zero violations | required | - |
| E15 | 3 | W3 | document-links | alignment after the review fix | PASS | zero failures and warnings; corpus lifecycle and occupancy zero | required | - |
| E16 | 4 | W5 | governance-unit-tests | PR #723 review fixes, quiet tree: all `tests/lib/document_governance` modules, `tests/validation/lifecycle`, Script Manifest | FAIL | spec packages 88 OK; links, operations catalog, metadata validator, generations 285 OK; registry, requirements, identity, architecture 184 OK; metadata, lifecycle, references, taxonomy, manifest 272 with 1 failure and 1 error from a bare REQ-0026 child identity | required | - |
| E17 | 4 | W5 | governance-unit-tests | after naming the retired REQ-0026 items in words and committing | PASS | metadata profile and repository contract tests OK in a 32-test rerun | required | E16 |
| E18 | 4 | W5 | gate-and-ci-routing | `tests/lib/gate` (includes workflow-contract tests), CI routing and CI gate plan under uv Python | FAIL | 283 tests: the gate evidence module needs `fcntl.F_ADD_SEALS`; one descendant-cleanup subtest under load | required | - |
| E19 | 4 | W5 | gate-and-ci-routing | descendant cleanup alone; gate evidence with `/usr/bin/python3` | PASS | descendant test OK alone; gate evidence 21 OK | required | E18 |
| E20 | 4 | W5 | metadata-changed | `check-changed --base-ref origin/main` | PASS | 371 selected, zero violations after fixing ADR-0051 parent order | required | - |
| E21 | 4 | W5 | metadata-active | `check-active` | PASS | 497 selected, zero violations | required | - |
| E22 | 2 | W1 | corpus-lifecycle | `--base-ref origin/main` | PASS | zero violations; occupancy zero | required | - |
| E23 | 3 | W3 | document-links | alignment | PASS | 954 documents, 8342 links, zero failures and warnings | required | - |
| E24 | 4 | W5 | manifest-and-renderer | Script Manifest; provider renderer `--check` | PASS | manifest valid; drift 0 | required | - |
| E25 | 4 | W5 | hosted-ci | GitHub Actions on the pushed head | NOT_RUN | not observed from this worktree | required | - |
| E26 | 4 | W5 | governance-unit-tests | PR #723 re-review fixes, quiet tree: every `tests/lib/document_governance` module, `tests/validation/lifecycle`, Script Manifest (revision dc6b0a9eb, with the FR-0003 fix applied during the run; ADR-0051 `accepted`) | FAIL | spec packages 88 OK; links, operations catalog, metadata validator, generations 285 OK; registry, requirements, identity, architecture 181 OK; metadata, lifecycle, references, taxonomy, manifest 274 with 1 error from a bare REQ-0026 child identity in the narrowed FR-0003 | required | - |
| E27 | 4 | W5 | governance-unit-tests | the metadata, lifecycle, references, taxonomy and manifest batch rerun in full after that fix (revision fb75f9955; ADR-0051 `accepted`) | PASS | 274 tests OK | required | E26 |
| E28 | 4 | W5 | gate-and-ci-routing | `tests/lib/gate` (includes workflow-contract tests), CI routing and CI gate plan under uv Python (revision dc6b0a9eb; ADR-0051 `accepted`) | FAIL | 283 tests: the gate evidence module needs `fcntl.F_ADD_SEALS` | required | - |
| E29 | 4 | W5 | gate-and-ci-routing | `tests.lib.gate.test_ci_gate_evidence` with `/usr/bin/python3` (revision dc6b0a9eb; ADR-0051 `accepted`) | PASS | 21 tests OK | required | E28 |
| E30 | 4 | W5 | metadata-changed | `check-changed --base-ref origin/main` with ADR-0051 `accepted` | FAIL | invalid-initial-status: a new ADR must start at proposed | required | - |
| E31 | 4 | W5 | metadata-changed | `check-changed --base-ref origin/main` with ADR-0051 `proposed` | PASS | 372 selected, zero violations | required | E30 |
| E32 | 4 | W5 | metadata-active | `check-active` | PASS | 497 selected, zero violations | required | - |
| E33 | 2 | W1 | corpus-lifecycle | `--base-ref origin/main` | PASS | zero violations; occupancy zero | required | - |
| E34 | 3 | W3 | document-links | alignment (revision fb75f9955; ADR-0051 `accepted`) | PASS | 954 documents, 8343 links, zero failures and warnings | required | - |
| E35 | 4 | W5 | manifest-and-renderer | Script Manifest; provider renderer `--check` (revision fb75f9955; ADR-0051 `accepted`) | PASS | manifest valid; drift 0 | required | - |
| E36 | 4 | W5 | staged-precommit | `run-ci-precommit.sh --mode local-staged` before each re-review commit | PASS | no failing hook | required | - |
| E37 | 4 | W5 | hosted-ci | GitHub Actions on the new head | NOT_RUN | not observed from this worktree; the coordinator reported CI passing on 42809b561 | required | - |
| E38 | 4 | W5 | governance-unit-tests | final re-review fixes, revision b8832d8ee (ADR-0051 `proposed`), quiet tree: every `tests/lib/document_governance` module, `tests/validation/lifecycle`, Script Manifest | FAIL | spec packages 88 OK; links, operations catalog, metadata validator, generations 285 OK; metadata, lifecycle, references, taxonomy, manifest 275 OK; registry, requirements, identity, architecture 181 with 2 failures: two allocation fixtures reused the now-reserved SPEC-0104 | required | - |
| E39 | 4 | W5 | governance-unit-tests | registry, requirements, identity and architecture batch rerun in full at ef6046cc9 after repointing those fixtures | PASS | 181 tests OK | required | E38 |
| E40 | 4 | W5 | gate-and-ci-routing | `tests/lib/gate` (includes workflow-contract tests), CI routing and CI gate plan under uv Python, revision b8832d8ee | FAIL | 283 tests: the gate evidence module needs `fcntl.F_ADD_SEALS` | required | - |
| E41 | 4 | W5 | gate-and-ci-routing | `tests.lib.gate.test_ci_gate_evidence` with `/usr/bin/python3`, revision b8832d8ee | PASS | 21 tests OK | required | E40 |
| E42 | 4 | W5 | metadata-changed | `check-changed --base-ref origin/main`, revision b8832d8ee, ADR-0051 `proposed` | PASS | 372 selected, zero violations | required | - |
| E43 | 4 | W5 | metadata-active | `check-active`, revision b8832d8ee | PASS | 497 selected, zero violations | required | - |
| E44 | 2 | W1 | corpus-lifecycle | `--base-ref origin/main`, revision b8832d8ee | PASS | zero violations; occupancy zero | required | - |
| E45 | 3 | W3 | document-links | alignment, revision b8832d8ee | PASS | 954 documents, 8343 links, zero failures and warnings | required | - |
| E46 | 4 | W5 | manifest-and-renderer | Script Manifest and provider renderer `--check`, revision b8832d8ee | PASS | manifest valid; drift 0 | required | - |
| E47 | 4 | W5 | staged-precommit | `run-ci-precommit.sh --mode local-staged` before each final re-review commit | PASS | no failing hook | required | - |
| E48 | 4 | W5 | hosted-ci | GitHub Actions on the final head | NOT_RUN | not observed from this worktree | required | - |
| E49 | 4 | W5 | operations-prefix-scan | identity history tests, metadata check-changed `--base-ref origin/main`, registry and requirements tests, corpus lifecycle after the prefix table change | PASS | 29 identity tests OK; check-changed 372 selected, 0 violations; registry and requirements OK; lifecycle and occupancy 0 | required | - |
| E50 | 4 | W5 | hosted-ci-prior-head | CI Quality Gates run 41637977928 on d80fddbac | PASS | candidate-quality success; main-security skipped | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | - | @buenhyden |
| 2 | pending | - | - | @buenhyden |
| 3 | pending | - | - | @buenhyden |
| 4 | pending | - | - | @buenhyden |

## Review and Completion

Local checks are recorded above. The coordinator approved the test deletions
and repointing listed in Test changes. Independent review of PR #723 requested
changes (I1 to I6, M1 to M6), and its re-review requested N1 to N4 and m1 to m6;
all are addressed in this branch, as are the final re-review items 1 to 8,
with M4 and M5 recorded as open and ADR-0051 acceptance deferred to the change
after merge. Hosted CI for the new head has
not been observed, and no criterion is accepted yet.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
