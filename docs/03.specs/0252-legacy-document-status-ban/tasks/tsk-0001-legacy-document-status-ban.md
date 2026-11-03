---
title: "Legacy Document Status Ban Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0252-TSK-0001"
parent_ids:
- "SPEC-0252-PLAN-0001"
created: "2026-11-04"
---

# Legacy Document Status Ban Task

## Overview

### Objective

Implement W1–W4: disallow legacy statuses and lineage keys in Stage 01 to 03,
retire ADR-0011, and remove the archive scaffolding and receipt field.

## Inputs and Authorization

The user directed that `docs/01.requirements`, `docs/02.architecture`, and
`docs/03.specs` allow no legacy or deprecated document status or format, that
existing ones be cleaned up, and that governance reflect it. On 2026-11-04 the
user decided that ADR-0011, the only `deprecated` document, be summarized and
deleted; that decision is the removal approval. No push, pull request, or merge
from this Task.

## Work Log

### Current contract decision

The user's direction authorizes this Spec and Plan as written.

### Current readiness and execution

Inputs, work units, and checks are recorded here. The Task is ready and in
progress under the approved parents. Hosted CI has not run.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0252 | draft | approved | #current-contract-decision |
| SPEC-0252-PLAN-0001 | draft | approved | #current-contract-decision |
| SPEC-0252-TSK-0001 | draft | ready | #current-readiness-and-execution |
| SPEC-0252-TSK-0001 | ready | in-progress | #current-readiness-and-execution |

### Removed states and keys

- Lifecycles: `requirement` keeps `draft`, `in-review`, `approved`;
  `architecture-description` keeps `draft`, `in-review`, `active`;
  `architecture-decision` keeps `proposed`, `accepted`, `rejected`; `spec` and
  `plan` keep `draft`, `in-review`, `approved`, `cancelled`; `contract` keeps
  `draft`, `review`, `approved`, `active`. `task` was already free of them.
- Profiles: the seven Stage 01 to 03 profiles drop `supersedes` and
  `superseded_by`, and their `superseded` conditional requirement. No current
  document used either key.
- Disposition entry states for those profiles drop `superseded` and `retired`.
- `common.archive_retention` keeps only `disposition_entry_statuses`, which the
  occupancy and package-removal checks read; the catalog, assessment,
  availability, citation, and `legacy_*` keys had no reader.
- Archive profiles `archive-record-completed`, `archive-record-superseded`,
  `archive-record-retired`, `archive-record-resolved`, `migration`,
  `tombstone`, and `archive-retention-catalog`, their transitions, template
  roles, and the two archive templates are removed. Stage 98 classification
  does not need them: occupancy rejects every tracked file there but the
  README.
- `branch_integration_receipts` is removed from the Registry, the frontmatter
  schema, the Spec Package loader, and SPEC-0204-TSK-0001, which is `blocked`
  and therefore editable. Receipts granted nothing since SPEC-0249.

### ADR-0011 retirement

ADR-0011 selected Homer, Portainer, RedisInsight, Dozzle, and Open Notebook
with SurrealDB for the former `11-laboratory` tier, was deprecated on
2026-10-29 when SPEC-0197 removed that tier, and had no remaining decision.
Its surviving selection and the Docker-socket access-control trade-off are
summarized in AD-0011 Traceability. REQ-0012, ADR-0025, AD-0011, and the
decision README no longer link to it; 11 is in the Registry ADR
`reserved_history`. SPEC-0212-TSK-0036 (terminal) and the dated DATA-0096
snapshot keep their mentions.

### Other cleanup

SPEC-0204-TSK-0010 (in progress) had a body line that began `status:`
(`status: PARTIAL, draft recorded.`); it now reads `S10b result: PARTIAL,
draft recorded.` and no longer looks like frontmatter.

### Test changes

| Test | Change |
| --- | --- |
| `test_task_branch_integration_receipt_has_one_closed_typed_contract` | Replaced by `test_retired_branch_integration_receipt_is_rejected`: the field is in no profile, and the closed schema rejects it |
| `test_an_unsafe_receipt_path_is_rejected_at_load` | Deleted: the loader no longer parses receipts; the schema rejection above covers the field |
| `test_stage_01_to_03_lifecycles_offer_no_legacy_status` | Added |
| `test_a_legacy_status_in_stage_01_or_02_is_an_invalid_status` | Added: each legacy status on a Requirement, AD, and ADR yields `invalid-status` |
| Four lifecycle expectation tests and the profile map test | Updated to the narrowed lifecycles; `migration` and `tombstone` left the profile map |
| `test_loads_frozen_canonical_documents_and_validates_graph` | Loads a plain accepted ADR; it no longer builds a superseded pair |
| `test_a_legacy_status_fails_closed_at_load` | Added: the architecture loader rejects `superseded`, `deprecated`, and `retired` |
| `test_dangling_and_asymmetric_supersession_are_reported`, `test_cyclic_supersession_is_reported` | Deleted: their fixtures need a `superseded` status the loader now rejects; the graph rules keep their direct-construction tests |
| `test_metadata_cli_rejects_a_legacy_architecture_status` | Was `test_metadata_cli_rejects_ineffective_supersession_successor`; now asserts the CLI rejects a `superseded` ADR |
| `SealedSectionShapeTests`, `test_a_sealed_shape_is_not_held_to_the_required_order` | Deleted with the sealed section shape mechanism, which only archive route records used |
| Frozen exemption path `docs/98.archive/retired/...` | Dropped from the heading exemption test: no archive profile classifies it |
| `test_a_stage_98_anchor_is_no_longer_admitted` | Was `test_registered_archive_anchor_remains_admitted`; a Stage 98 anchor is now unadmitted |
| `test_every_text_mutator_excludes_the_same_frozen_payloads` | The Registry defines no frozen set, so the anchor must select no tracked file |

### Open issues

- The archive-record frontmatter vocabulary in `metadata/profile.py`
  (disposition and snapshot fields, `EXPECTED_ARCHIVE_SOURCE_PREFIXES`) and
  `common.archive_source_prefixes` remain; no current profile uses them, and
  removing them is a separate validator change.
- The `migration` and `tombstone` identity spaces keep their reserved numbers.
- `architecture.py` and `metadata/reference.py` keep the supersession graph
  code; it can no longer receive an edge from a Stage 02 document.
- The `frozen_archive_payloads` pre-commit anchor and its reader in
  `scripts/hooks/post-tool-validate.sh` remain and select no file; removing
  them is a hook change for the QA and CI/CD cleanup phase.
- The `sealed` status and `sealed-record` lifecycle are removed with the
  archive profiles; `_registered_section_findings` keeps an unused
  `changed_boundary` parameter.
- Operational, reference, and governance lifecycles still offer `deprecated`,
  `superseded`, and `retired`; the user's rule names Stage 01 to 03 only.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W1 | registry-tests | `test_registry` after the lifecycle change, before the expectation updates, worktree on cb7c324d3 | FAIL | 204 tests with Spec Package tests: 4 failures and 1 error, all asserting the removed states or profiles | required | - |
| E2 | 1 | W1 | registry-tests | `test_registry` after the expectation updates | PASS | 117 tests OK | required | E1 |
| E3 | 1 | W1 | legacy-status-tests | the three added tests | PASS | 3 tests OK | required | - |
| E4 | 2 | W2 | metadata-changed | `check-changed --base-ref origin/main`, commit 1ac1b884b | PASS | selected 13, zero violations | required | - |
| E5 | 2 | W2 | document-links | alignment mode, commit 1ac1b884b | PASS | 848 documents, 7902 links, zero failures | required | - |
| E6 | 2 | W2 | corpus-lifecycle | `--base-ref origin/main`, commit 1ac1b884b | PASS | lifecycle zero; occupancy zero | required | - |
| E7 | 4 | W4 | governance-suite | `tests/lib/document_governance` discovery, commit 847e13f23, quiet tree | FAIL | 766 tests: 4 failures and 6 errors, all from tests that encoded the removed supersession fixtures, sealed shapes, archive anchors, or the index row wording | required | - |
| E8 | 4 | W4 | governance-suite | same discovery after the test alignment, commit bc6fe0bb5 | PASS | 758 tests OK | required | E7 |
| E9 | 4 | W4 | routing-ownership | CI routing and surface ownership, commit 847e13f23 | FAIL | 92 tests, 1 failure: the frozen payload test required an archive profile | required | - |
| E10 | 4 | W4 | routing-ownership | same suites, commit bc6fe0bb5 | PASS | 92 tests OK | required | E9 |
| E11 | 4 | W4 | lifecycle-and-gate-suites | `tests/validation/lifecycle` and `test_ci_gate_evidence` (system python3), commit bc6fe0bb5 | PASS | 20 and 21 tests OK | required | - |
| E12 | 4 | W4 | repository-checks | metadata check-active, links alignment, Script Manifest, renderer `--check`, agent governance contract, commit bc6fe0bb5 | PASS | 497 selected, zero violations; alignment PASS; manifest valid; drift 0; contract failures 0 | required | - |
| E13 | 4 | W4 | document-commands | links `commands` mode, commit bc6fe0bb5 | FAIL | 2 findings: the ignored `_workspace` paths in the DATA-0096 README, present on main before this change | required | - |
| E14 | 4 | W4 | base-drift | metadata check-changed and corpus lifecycle against `origin/main` after PR #728 merged (4adeb3d37), commit bc6fe0bb5 | FAIL | configuration error on `docs/01.requirements/AGENTS.md`, which this branch's loaders did not yet admit; the rebase onto 4adeb3d37 brings in that support | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | - | @buenhyden |
| 2 | pending | - | - | @buenhyden |
| 3 | pending | - | - | @buenhyden |
| 4 | pending | - | - | @buenhyden |

## Review and Completion

Local checks are recorded above. Independent review and hosted CI have not run,
and no criterion is accepted yet.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
