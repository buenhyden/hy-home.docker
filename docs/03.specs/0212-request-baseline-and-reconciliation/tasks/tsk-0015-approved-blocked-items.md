---
title: "Approved Blocked Items Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0015"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Approved Blocked Items Task

## Overview

### Objective

Execute W31: apply the owner's approval of the two items TSK-0013 blocked, and
repair the regression the TSK-0012 removal caused on `main`. This Task owns
criterion 26 only.

## Inputs and Authorization

On 2026-10-29 the owner approved the template subtopic work and the removal of
`cliff.toml`, which TSK-0013 had blocked. That approval resolves the overlap
with the release-writer scope named in SPEC-0211 TSK-0001; this Task does not
edit that Task. The input is branch `perf/archive-history-scan` (PR #610) on
top of merged PR #609. The authorization covers this branch, its pull request,
and merge through the protected path.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0015 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0015 | ready | in-progress | #objective |
| SPEC-0212-TSK-0015 | in-progress | completed | #evidence |

### git-cliff removal

No workflow or script ran git-cliff; the release producer validates a
hand-written `CHANGELOG.md`. `cliff.toml`, its test block in
`tests/lib/gate/test_ci_gate_adapters.py`, its two `.github/workflow-contract.yml`
entries, and its two routing-list entries are removed. Commitizen parsing and
SemVer bump tests remain.

### Template subtopics

| Template | `###` subtopics added |
| --- | --- |
| `specs/spec` | Intent, Background; In Scope, Out of Scope; Normal, Error, Boundary Behavior, Constraints; Observable Failures, Stop Boundaries |
| `specs/contracts/data-model` | Types, Nullability and Defaults; Cardinality, Ownership; Keys and Uniqueness, Referential Rules; Creation and Mutation, Retention |
| `references/audit`, `data`, `research` | Boundaries, Reproducible Method; Dated Observations, Interpretation; Unobserved Facts, Interpretation Limits |
| `governance/contract` | Approved Scope, Source Inputs; Stages, Status Transitions; Owned and Not-Owned Decisions; Artifacts, Task Evidence |
| `governance/control` | Surfaces, Actors; Required, Prohibited; Scoped Exceptions, Authorization Boundaries; Checks, Expected Signals, Evidence Limits |
| `governance/knowledge` | Included, Excluded; Sources, Refresh Triggers |
| `governance/provider` | Entry Shim, Bootstrap Order; Generated and Authored Native Surfaces; Registered Gate, Unsupported Behavior |
| `governance/rule` | Event, Pattern; Checks, Expected Signals, Evidence Limits |
| `governance/skill` | Required Inputs, Preconditions; Artifacts, Evidence; Stop Conditions, Recovery |

Single-value sections (titles, links, one list) keep no subtopic. No `###`
name repeats a `##` section name of the same profile. `archive/tombstone` gets
none: its loader reads each section body to the next `##` as one value, so a
`###` line would corrupt the Retired Path or Successor value. Existing
documents are not rewritten; the subtopics apply to new documents.

### Removal regression

`test_every_registered_index_governs_at_least_one_package` failed on `main`
after PR #609 for `docs/90.references/audits/README.md` and
`docs/90.references/data/README.md`: their last members became
`git-history-only`. The capture row keeps those units discoverable, so the
test now also counts members named by a history-only unit's catalog `Source`.
The path-selected PR checks did not run this module, which is how it reached
`main`.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Metadata contracts | 26 | W31 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |
| Template lint | 26 | W31 | `markdownlint-cli2` on the 11 changed templates | This branch | PASS | 0 issues | required | - |
| Gate tests | 26 | W31 | `python3 -m unittest tests.lib.gate.test_ci_gate_adapters tests.validation.test_agent_governance_ci_routing tests.validation.test_ci_gate_plan` | This branch; Python 3.12.3 | PASS | 175 tests | required | - |
| Template tests | 26 | W31 | `test_heading`, `test_profile`, `test_reference`, `test_operations_catalog`, `test_registry`, `test_requirements` | This branch | PASS | All pass after the regression fix | required | - |
| Regression reproduction | 26 | W31 | `IndexMembershipTests` at `2059b0d57` and at merged `main` | Both revisions | PASS | OK before PR #609; 2 failures after; OK on this branch | required | - |
| Full suite | 26 | W31 | `python3 -m unittest discover -s tests -t .`, then the failing modules at `2059b0d57` | This branch and baseline | FAIL | 18 failures in secret-metadata sync, SMTP generator, secret catalog, and two modules that need the uninstalled `referencing` package; the identical set fails at `2059b0d57` | optional | - |

The full-suite FAIL predates this session; its owners are the secret-sync,
SMTP, and resource-contract surfaces, and this Task does not claim it.

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 26 | accepted | Metadata contracts, Template lint, Gate tests, Template tests, Regression reproduction | git-cliff configuration removed, 11 templates gained subtopics, and the index-membership regression is fixed; the pre-existing full-suite failures stay with their owners. | SPEC-0212 TSK-0015 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
