---
title: "SPEC-0209 and SPEC-0231 Retirement Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0258-TSK-0001"
parent_ids:
- "SPEC-0258-PLAN-0001"
created: "2026-11-04"
---

# SPEC-0209 and SPEC-0231 Retirement Task

## Overview

### Objective

Read the lifecycle generation 5 and 6 migration proofs from the last
generation 6 revision, then delete SPEC-0209 and SPEC-0231.

## Inputs and Authorization

The user asked to delete SPEC-0209 and SPEC-0231 (option L1) and approved
reading the proofs from the generation 6 revision. On 2026-11-04 the user
said "Not started 중 지금 실행할 수 있는 요구사항을 검토하여 진행한다." The
work starts from main `0ab42bc30`. This Task pushes and merges nothing; the
coordinator pushes the branch and opens the pull request, and the user
merges.

## Work Log

### Current contract decision

The user's direction authorizes this Spec and Plan as written.

### Current readiness and execution

Inputs, work units and checks are recorded here. The Task is ready and in
progress under the approved parents. Hosted CI has not run.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0258 | draft | approved | #current-contract-decision |
| SPEC-0258-PLAN-0001 | draft | approved | #current-contract-decision |
| SPEC-0258-TSK-0001 | draft | ready | #current-readiness-and-execution |
| SPEC-0258-TSK-0001 | ready | in-progress | #current-readiness-and-execution |

### Decisions

- `previous_generation_revision(root, 7)` resolves to
  `49f8dd661acf37bf292ee0aa59abfe1af16cde10`. At that revision the
  generation 5 proof (source `8b85e88fe2dfef54f4cc125ee2687982c86c1942`) is
  in SPEC-0209-TSK-0001 and the generation 6 proof (source
  `2a57d4122dc8dac954afca364b838e4bf97fd44a`) in SPEC-0231-TSK-0001.
- `load_spec_packages` loads the generation 6 tree once when the Registry
  generation is 7 or later and passes it as `proof_packages` to the
  generation 5, 6 and 7 admission paths. The generation 7 path still admits
  only Tasks of packages in the current tree. With no `proof_packages`, the
  generation 5 and 6 paths keep reading proofs from the given packages.
- Before the change, loading the tree without the two packages failed with
  "lifecycle generation migration requires one proof"; after it, the loader
  returns all 14 current packages.
- The Spec number 258 follows the open SPEC-0257 branch; the Registry `spec`
  high-water moves to 258 and `next_number` to 259.
- Other packages' Task records that mention the two packages as proof
  (SPEC-0250-TSK-0001, SPEC-0253-TSK-0001, SPEC-0248-TSK-0001) are their own
  history and stay. SPEC-0250's Spec bullet is reworded to past tense.
  ADR-0048 decision text and the provenance comments in
  `metadata/lifecycle.py` and `test_generation6.py` stay as lineage.

### Changed

- `scripts/lib/document_governance/spec_packages.py`: proof source.
- `tests/lib/document_governance/test_spec_packages.py`: three tests.
- `docs/03.specs/0209-common-document-contract-adoption/` and
  `docs/03.specs/0231-task-lifecycle-generation-6/`: deleted.
- `docs/99.templates/registry.json`: 209 and 231 in `reserved_history`;
  high-water 258, `next_number` 259.
- `docs/03.specs/README.md`: rows removed, SPEC-0258 row, retention bullet.
- `.agents/governance/documentation-protocol.md`: retention sentence.
- `docs/02.architecture/decisions/README.md`: ADR-0048 entry wording.
- `docs/03.specs/0250-finished-spec-package-deletion/spec.md`: past tense.

### Open issues

- None.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1, 2 | W1 | unit-tests | the three new `test_spec_packages` tests, uncommitted tree on 0ab42bc30 with both packages deleted | PASS | 3 tests OK; the proof-source test errors without the loader change | required | - |
| E2 | 3 | W2 | metadata-changed | `check-changed --base-ref origin/main`, same uncommitted tree on 0ab42bc30 with this package | PASS | selected 13, zero violations | required | - |
| E3 | 3 | W2 | metadata-active | `check-active`, same uncommitted tree on 0ab42bc30 | PASS | selected 503, zero violations | required | - |
| E4 | 3 | W2 | corpus-lifecycle | `check-document-corpus-lifecycle.py --base-ref origin/main`, same uncommitted tree on 0ab42bc30 | PASS | lifecycle zero, occupancy zero | required | - |
| E5 | 3 | W2 | document-links | links `alignment`, `navigation`, `language`, `traceability`, `entrypoint`, `commands`, same uncommitted tree on 0ab42bc30 | PASS | 870 documents, 8092 links, zero failures in each mode | required | - |
| E6 | 1, 2 | W1 | unit-tests | `test_spec_packages`, `test_registry`, `test_identity_history` with `/usr/bin/python3`, same uncommitted tree on 0ab42bc30 | PASS | 242 tests OK | required | - |
| E7 | 4 | W3 | unit-tests | `tests/lib/document_governance` discovery with `/usr/bin/python3`, same uncommitted tree on 0ab42bc30 | PASS | 764 tests OK | required | - |
| E8 | 4 | W3 | hosted-ci | GitHub Actions | NOT_RUN | branch not pushed | required | - |

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
