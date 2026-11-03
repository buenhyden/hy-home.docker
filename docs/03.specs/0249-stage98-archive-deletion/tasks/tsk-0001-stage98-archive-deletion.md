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
- The completed-archive receipt carrier of branch integration was deleted;
  only a current Stage 03 Task carries a receipt.
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
| `test_spec_packages`: ordinary preservation | replaced | preservation flow removed | yes |
| `test_spec_packages`: unsafe catalog retirement | deleted | catalog reader removed; replaced by the Registry-file test | yes |
| `test_spec_packages`: catalog row retirement | deleted | Retention Catalog removed | no |
| `test_spec_packages`: positive handoff via either carrier; blocked current carrier; matching completed identity (`none`, `ambiguous`) | deleted | completed-archive carrier removed; `ambiguous` replaced by the reserved-number tests | `ambiguous` yes |
| `test_spec_packages`: duplicate carrier; archived target without evidence | repointed | must still be rejected by any receipt finding | yes |
| `test_spec_packages`: ready current carrier | kept as its own test | rejection still holds | yes |
| `test_agent_governance_ci_routing`: frozen payload agreement | repointed | requires only the unmanaged archive profile roots | no |

Added fail-closed tests: `test_a_removal_is_recorded_only_by_a_reserved_spec_number`,
`test_a_root_without_its_own_valid_registry_grants_no_retirement` (missing,
symlink, directory), `test_a_malformed_reserved_history_grants_no_retirement`
(unsorted, out of range, not an integer),
`test_a_number_reserved_in_another_space_does_not_retire_a_spec`, and
`test_a_typed_reference_to_a_reserved_only_identity_is_unresolved`.

### Open issues

- The branch-integration receipt still needs a same-identity completed record,
  which can no longer exist, so every handoff is rejected. Its remaining
  rejection tests pass but no longer isolate their specific check. Redesign or
  remove the handoff in the completed Spec package phase.
- The archive-record metadata vocabulary in `metadata/profile.py` and the
  archive profiles stay as scheme definitions; remove them in the legacy and
  deprecated phase if no record type needs them.
- The commands check reports two `_workspace` paths in the frozen DATA-0096
  README; they come from PR #720 and depend on ignored local files.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 3 | W3 | document-links | alignment mode after the reference cleanup | PASS | 950 documents, 8325 links, zero failures | required | - |
| E2 | 3 | W3 | document-commands | commands mode | FAIL | 2 findings for ignored `_workspace` files that PR #720 documents; not caused by this change | required | - |
| E3 | 4 | W5 | governance-unit-tests | four batches while the tree was being edited and committed | FAIL | spec packages 91: 8 failures and 6 errors; registry group 182: 2 failures; links group 287: 2 failures; metadata and lifecycle group 270: 3 failures. Causes: tests of removed archive paths, and Stage 03 changing under the reconciliation tests during commits | required | - |
| E4 | 4 | W5 | governance-unit-tests | final quiet-tree run of all `tests/lib/document_governance` modules, `tests/validation/lifecycle` and the Script Manifest tests | FAIL | spec packages 91 OK; links, operations catalog, metadata validator and generations 286 OK; registry, requirements, identity and architecture 182 with 1 subtest failure; metadata, lifecycle, references, taxonomy and manifest 271 with 1 failure | required | E3 |
| E5 | 4 | W5 | gate-and-ci-routing | `tests/lib/gate` discovery, CI routing and CI gate plan under uv Python | FAIL | 283 tests: the gate evidence module needs `fcntl.F_ADD_SEALS`; two descendant-cleanup subtests under load; frozen payload agreement | required | - |
| E6 | 4 | W5 | gate-evidence | `tests.lib.gate.test_ci_gate_evidence` with system python3 | PASS | 21 tests OK | required | E5 |
| E7 | 4 | W5 | targeted-reruns | identity recovery subtest, Script Manifest tests, frozen payload agreement and descendant cleanup after fixes | PASS | 60 tests OK | required | E4, E5 |
| E8 | 4 | W5 | metadata-active | `check-document-metadata.py --mode check-active` | PASS | 497 selected, zero violations | required | - |
| E9 | 4 | W5 | metadata-changed | `--mode check-changed --base-ref a879f2b64` | PASS | 355 selected, zero violations | required | - |
| E10 | 1, 2 | W5 | corpus-lifecycle | `check-document-corpus-lifecycle.py --base-ref a879f2b64` | PASS | zero violations; occupancy zero | required | - |
| E11 | 4 | W5 | manifest-and-renderer | `check-script-manifest.py`; provider renderer `--check` | PASS | manifest valid; renderer drift 0 | required | - |
| E12 | 4 | W5 | staged-precommit | `run-ci-precommit.sh --mode local-staged` before each commit | PASS | no failing hook after fixing two MD032 blank lines and formatting | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | - | @buenhyden |
| 2 | pending | - | - | @buenhyden |
| 3 | pending | - | - | @buenhyden |
| 4 | pending | - | - | @buenhyden |

## Review and Completion

Local checks are recorded above. The coordinator approved the test deletions
and repointing listed in Test changes. Independent review and hosted CI have
not run, and no criterion is accepted yet.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
