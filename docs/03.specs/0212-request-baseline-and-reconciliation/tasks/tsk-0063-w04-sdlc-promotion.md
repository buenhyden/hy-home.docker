---
title: "v14.7 W04 SDLC and Promotion Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0063"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-13"
---

# v14.7 W04 SDLC and Promotion Task

## Scope

### Objective and Parent

#### Objective

Own W121/criterion 116, the v14.7 W04 run for this workspace:

- H-07 from TSK-0059: the Registry `common` heading names
  (`spec_section`, `plan_section`, `task_section`,
  `criterion_acceptance_section`, `execution_items.section`,
  `task_lifecycle_events.section`, `incident_closure.corrective_section`)
  are bound to the common form the profiles declare, and the Spec Package
  reader reads that binding instead of a code table;
- the W04 meaning in the SDLC policy: promotion has a Plan, a target-document
  and a Task owner, and SDLC phases, document Stages and state axes stay
  separate.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [W00 v14.7 intake](tsk-0059-w00-v14-7-intake.md)
- [W03 templates, metadata and relations](tsk-0058-w03-templates-metadata-relations.md)
- [Pre-W04 conformance](tsk-0062-pre-w04-conformance.md)
- [SDLC policy](../../../../.agents/governance/sdlc.md)

### Inputs and Authority

The owner's request of 2026-11-13 runs the W04 prompt of the v14.7 revision
package (`_workspace/workspace_execution_tasks_v14_7_revision_20261113_r1/`,
read as reference data). It names the remaining W04 work for this workspace
as H-07 and the alignment of the new form with execution, acceptance and
promotion ownership. The package marks W00 to W03 complete for this workspace
(TSK-0058 to TSK-0062, PRs #989 to #992); this run did not repeat them.

The W03 decision recorded in TSK-0058 (Plan role, 2026-11-13) is reused: the
pinned `common` heading values and `lifecycle_generation` 7 stay, because
historical Registries are validated by the same pin code.

The request authorizes the Registry, schema, reader and policy changes named
here, and this Task with criterion 116 and W121. Push, pull request, merge and
runtime operations are not authorized by it.

## Execution Log

### Work Performed

#### W04 run 2026-11-13

Started from `main` `73b1705b6` on branch `docs/w04-sdlc-promotion`.

Gap found: `spec_packages.py` held the legacy-to-common-form mapping in two
code tables (`_COMMON_FORM_PATHS`, `_TASK_COMMON_FORM`), while the Registry
declared the profiles' H2 and H3 and only the Stage 99 README stated the
mapping. A profile heading rename would not have reached the reader.
`sdlc.md` said the Task's `Evidence` owns the promotion receipt, which the
common form moved to the Plan Promotion Map and the Task Handoff, and it did
not separate phases, Stages or state axes.

Changes:

- Registry `common.section_forms` maps each pinned heading value to its
  profile, H2 and, where moved, H3. The schema declares the key.
- `registry.py` `_validate_section_forms` reports `common-section-form` for a
  heading value without a binding, a binding that names no heading value, or
  a section the profile does not register (the H3 must be a registered
  subsection of that H2; an H2-only binding must keep the heading name). A
  Registry without the key predates the binding and is not checked.
- `spec_packages.py` reads both tables from the tracked Registry through
  `registry_module.load_registry()`, as `registry._registered_types` does,
  and raises `RegistryError` when the current Registry lacks the binding.
- `sdlc.md` 1.8.0: promotion owners, the receipt fields, phases versus Stages,
  one record per state axis, and the Registry binding. Glossary 0.5.1 and the
  Task template's Promotion Receipt prompt name the same targets and fields.
  Stage 99 README 2.6.1 states where the mapping is declared.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0063 | draft | ready | #w04-run-2026-11-13 |
| SPEC-0212-TSK-0063 | ready | in-progress | #w04-run-2026-11-13 |

### Blockers and Decisions

- The binding is not pinned per heading in the Registry check: the check
  proves a registered section. `test_common_form_paths_come_from_the_registry`
  pins the exact four moved paths, and the check's rule that an H2-only
  binding keeps its heading name fixes Acceptance Criteria and Corrective
  Actions.
- Not run here and left to their owners: W05 validator items (H-05, H-08,
  H-12), W06 stage-QA cells (H-09, H-10), W07 Skill section. Q-07 runs only
  after W11.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Binding RED | 116 | W121 | red-green-proof | Two new tests against `73b1705b6` plus the tests only | FAIL | `KeyError: 'section_forms'` and no `_common_form_paths` in `spec_packages` | required | - |
| Binding GREEN | 116 | W121 | red-green-proof | The two new tests and `test_common_key_resolves_the_legacy_h2_or_the_common_form_h3` at `459800639` | PASS | 3 tests OK | required | Binding RED |
| Binding review | 116 | W121 | independent-review | Fresh-context code-reviewer of the uncommitted diff on `73b1705b6` | FAIL | CHANGES_REQUIRED: the reader read an absent `section_forms` as no common form, so a removed binding would pass silently; Minor: a correct-but-wrong binding passes the check, a stale binding was reported as unbound, `sdlc.md` and the glossary named different promotion targets, the template receipt prompt lacked the policy fields | required | - |
| Binding re-review | 116 | W121 | independent-review | Same reviewer, commit `459800639` | PASS | Every finding resolved or recorded under Blockers and Decisions; no caller in `spec_packages.py` swallows the reader's `RegistryError`; two Minor notes (message text untested, H2-only bindings pinned by the check), both answered in the follow-up commit | required | Binding review |
| Stage 03 checks | 116 | W121 | document-checks | `check-document-metadata --mode check-changed --base-ref main`, `check-document-links --mode alignment` and `--mode commands`, `check-document-corpus-lifecycle` on the staged `459800639` tree | PASS | metadata selected=7 violations=0; links failures=0 in both modes; lifecycle and occupancy violations=0 | required | - |
| Pre-commit | 116 | W121 | precommit-local-staged | `run-ci-precommit.sh --mode local-staged` on the staged `459800639` tree | PASS | exit 0 | required | - |

### Resolution Links

Binding RED is resolved by Binding GREEN, and Binding review by Binding re-review.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 116 | pending | Binding GREEN, Binding re-review, Stage 03 checks, Pre-commit | Awaiting the regression row and the owner's decision | SPEC-0212 TSK-0063 |

### Remaining Conditions

Owner acceptance of criterion 116; push, pull request and merge on the
owner's approval.

## Handoff

### Promotion Receipt

None yet: the policy and Registry changes are on branch
`docs/w04-sdlc-promotion` and reach their owners on merge.

### Next Owner

The current owner is @buenhyden.
