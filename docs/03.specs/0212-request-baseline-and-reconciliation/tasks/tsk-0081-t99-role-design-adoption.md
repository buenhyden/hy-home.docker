---
title: "T99 Role Design Adoption Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0081"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-17"
---

# T99 Role Design Adoption Task

## Scope

### Objective and Parent

Own criterion 137 and work units W142 to W147 under the [Spec](../spec.md)
and [Plan](../plan.md). Adopt the shared document role design core
`workspace-document-role-design` 4.0.0 in this workspace, one role group at
a time, and keep every unmoved form honest about the contract it follows.
The [W03-FORMS Task](tsk-0073-w03-forms-3-0-1.md) holds the form work this
reuses.

### Inputs and Authority

The direct 2026-11-17 request runs T99-CONFORMANCE from the git-ignored
package `_workspace/workspace_governance_4_2_0_20261116/`. It reads D01, D02,
D03, D24, D25, D26, D27 and D28 and the package's
`template-design-targets.json` 4.0.0. The package marks that core
`DESIGN_PROPOSAL_NOT_WORKSPACE_ADOPTION`. On 2026-11-17 the owner answered
the adoption question with full adoption in this chat, and authorized push,
pull request and merge. Terminal Task bodies stay as recorded, so the Task
role reaches new packages through a new lifecycle generation. No other
repository is opened or required.

## Execution Log

### Work Performed

#### Inventory and comparison

The Registry has 39 template roles over 47 tracked Stage 99 files. A one-time
export at `fdb92cd82` read the Registry and every template source with its
SHA-256, mapped 19 local roles to the 19 core roles and listed 20 unmapped
forms. The package's `compare_template_contracts.py` returned `MISMATCH`
for all 19 roles. Only the Task role shares its H2 titles; its H3 titles
and tables differ, with 9 evidence columns against the core's 12. 209
differences are in the typed contract fields the local Registry does not
carry. Four negative inputs were rejected as `INVALID_INPUT` or `MISMATCH`:
a changed source hash, a missing source digest, an inexact revision, and a
declared core with the local tables. The export and its output stayed in
the session scratchpad and are not committed.

About 700 current documents follow the moved forms. The largest groups are
130 package READMEs, 110 Tasks, and 78, 78 and 77 guides, runbooks and
policies.

#### Adoption design

The adopted core stays one file: the package source and its schema are
copied byte for byte to `docs/99.templates/contracts/`. The Registry pins
both in `common.role_design_contract` by path and SHA-256, as it pins the
glossary for the vocabulary contract. A template role declares either
`core_role` or `core_exception`. An exception is `pending-migration` with
its target core role, `domain` or `native`, each with a reason. The profile
schema holds that shape: exactly one of the two fields, a core role on a
pending exception and none on a domain or native one. 26 roles are
pending, 8 are domain forms and 5 are native syntax. TemplateDefinition reports
the role design contract only for a bound role, so an unmoved role keeps
reporting `COMMON-DOC-FORM-1` or the legacy contract it actually follows.

`check-document-metadata.py --mode check-contracts` checks the pin, the
schema, the identity and every bound role. A bound role conforms when its
H2 and H3 titles, their order and requiredness, and each table's section,
column labels and column requiredness equal the core. Matching titles with
different tables fail, and so does an extra or missing table. The core
assigns all 22 of its tables to an H2, so a table may sit in any H3 of that
H2. Not compared: a table's own condition, which the projection does not
carry, and the core's numeric order fields, which the array order already
expresses. The core is 196,063 bytes, 74.8% of the 262,144-byte read
limit it shares with the Stage 99 schemas. Each pinned file is read once to
hash it and once to parse it. Every core H2 and H3 in 4.0.0 is required, and so is every
column. The core assigns different value types to the same
column label in different roles, so the global column dictionary cannot
carry them. W143, which binds the first role, makes a bound role read its
column types from the core. W142 binds no role. Rejected: copying the
core into Registry profiles, which would leave two owners, and binding all
roles at once, which would report an unmoved form under the new contract.

Two classifications are decisions. The governance policy form moves to the
core policy role with the operations policy form in W143. The provider
runtime READMEs are Markdown READMEs that the provider renderer writes, so
they move to the core root README role in W145 through that renderer, not by
hand. The data model contract stays a domain form: it describes entities in
a Spec Package, not a Stage 90 data reference.

Each later work unit moves one role group in one change: the Registry
profile, the template, the readers and the current documents. The role then
switches from `core_exception` to `core_role`. Reverting a work unit
restores its form and exception together.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0081 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0081 | ready | in-progress | #adoption-design |

### Blockers and Decisions

The owner decided full adoption on 2026-11-17. Moving W143 to W147 changes
current documents, and those changes need the same per-group review.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Core comparison baseline | 137 | W142 | role-design-export | Workspace export at `fdb92cd82` through the package `compare_template_contracts.py --workspace-root` | FAIL | MISMATCH for 19 of 19 roles, 20 unmapped forms, exit 1 | required | - |
| Comparison negatives | 137 | W142 | role-design-export-negative | Changed hash, missing digest, inexact revision and declared core with local tables | PASS | Three INVALID_INPUT and one MISMATCH, as designed | required | - |
| Conformance RED | 137 | W142 | role-design-conformance | RoleDesignConformanceTests before the implementation | ERROR | `role_design_findings` did not exist, exit 1 | required | - |
| Conformance GREEN | 137 | W142 | role-design-conformance | test_template_definition with the pinned core and classified roles | PASS | 35 tests, exit 0 | required | Conformance RED |
| Contract wiring | 137 | W142 | document-contracts | check-document-metadata.py --mode check-contracts, then with one byte appended to the core | PASS | 0 violations; the changed core gave `role-design-source-changed`, exit 1; restored | required | - |
| Foundation review | 137 | W142 | independent-review | Commits `c1541ea86` and `9019594c7` | FAIL | CHANGES_REQUIRED: H2-owned tables rejected inside their H3, Stage 99 checks unrecorded, schema unpinned, failure paths and exception rules incomplete | required | - |
| Conformance review fixes | 137 | W142 | role-design-conformance | RoleDesignConformanceTests at `3e30b52ce` with H3 placement, extra and missing tables, H3 requiredness, unknown and unmapped roles, schema-held exception shape and identity | PASS | 13 tests, exit 0 | required | - |
| Foundation regression | 137 | W142 | document-governance-regression | test_registry, test_template_definition, metadata.test_heading, metadata.test_reference, test_metadata_validator and test_taxonomy at `3e30b52ce` | PASS | 374 tests in 363.184 seconds, exit 0 | required | - |
| Foundation corpus | 137 | W142 | document-corpus | check-active, check-contracts, corpus lifecycle, link alignment and governance contract at `3e30b52ce` | PASS | 589 selected and 0 violations; 0 contract, lifecycle and governance findings; alignment PASS | required | - |
| Foundation re-review | 137 | W142 | independent-review | Commits `3e30b52ce` and `f958da1ef` against the first review | PASS | APPROVE; six minor notes, of which the schema-hash test, the two document mentions, these revisions and the duplicate test are applied | required | Foundation review |

### Resolution Links

Conformance GREEN resolves Conformance RED, and Foundation re-review resolves
Foundation review. The comparison baseline stays
open until every role group conforms.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 137 | pending | Conformance GREEN, Contract wiring | Awaits W143 to W147 and the owner's decision | @buenhyden |

### Remaining Conditions

W143 to W147 move their role groups. The comparison baseline is resolved
only by a later export that conforms for every bound role.

## Handoff

### Promotion Receipt

The Registry, the tracked core and its schema, `template_definition.py` and
the contracts check hold the binding. The documentation protocol lists the
role design contract as a version object.

### Next Owner

The implementer owns W143 to W147. The owner decides criterion 137.
