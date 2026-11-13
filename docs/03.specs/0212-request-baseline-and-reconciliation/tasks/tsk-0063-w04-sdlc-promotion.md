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
Within this subsection's first part, the `sdlc.md` version cited is 1.8.0; the per-ID assessment below raised it to 1.9.0.

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
  one record per state axis, and the Registry binding. Glossary 0.6.0 and the
  Task template's Promotion Receipt prompt name the same targets and fields.
  Stage 99 README 2.6.1 states where the mapping is declared.

#### W04 per-ID assessment 2026-11-13

On the owner's direction of 2026-11-13 to review every remaining, unverified,
unreviewed and conflicting W04 item, three read-only rules-engineer reviews
compared the W04 prompt and its dependency contracts with the branch at
`acef19488`; the controller re-read the cited code lines before changing
anything. Read denominator: the W04 prompt in full; `REQUIREMENTS.json` for
SDLC-01 to SDLC-09; `STAGE-QA-MATRIX.md`, `SPEC-DISPOSITION.md`,
`SEMVER-POLICY.md`; the carry-forward CSVs for hy-home-docker; the 22 current
Spec Packages at status and Intent level (criterion-by-criterion review of
each package is UNVERIFIED).

| ID | Verdict before | Action | Change or owner |
| --- | --- | --- | --- |
| H-07 | GAP | CHANGE | Registry binding and reader, above |
| W04-A | PASS (split), GAP (events) | KEEP, CHANGE | Transition events table in `sdlc.md` |
| W04-B | PASS (Resolves), GAP (promotion) | CHANGE, DEFER W05 | Plan prompt; readiness needs receipts; check to W05 |
| SDLC-01 | GAP | CHANGE, DEFER W05 | Receipt adds the acceptance row and residual owner; Plan `Owner and Receipt` prompt plans and does not receipt; Stage 03 README; typed receipt check to W05 |
| SDLC-02, QA-C03 | GAP | CHANGE, DEFER W05 | Accepted cites at least one PASS row for its criterion and a non-PASS row only when it is resolved (TSK-0047 criterion 88 cites its resolved audit failures, so "only PASS rows" was too strict); Input names revision, environment and tool; other-revision PASS needs recorded equivalence |
| SDLC-03, SDLC-05 | GAP | CHANGE, DEFER W05 | Accepted needs PASS for every assigned pair; a cancelled item's pairs stay open |
| SDLC-04 | GAP | CHANGE | No status copies in Plan, README, Issue or PR text; SPEC-0212 Plan copies replaced by links. SPEC-0204 Plan copies (`plan.md` L151-157, L703-704) are corrected by its own writer when next edited |
| SDLC-06 | GAP | CHANGE, DEFER W05 | Operations currency by event and past `next_review_at`; `stale-active` retarget or removal to W05 |
| SDLC-07 | GAP | ADD | Transition events table |
| SDLC-08 | PASS (separation), GAP (fixtures) | DEFER W05 | Negative tests listed under Handoffs |
| SDLC-09, R147-07 | GAP (readiness) | CHANGE, DEFER W05 | Readiness requires each Promotion Map target document in a receipt or a no-update reason; a removing Task records receipts an older Task lacks |
| Evidence ladder | CONFLICT | CHANGE | SPEC-0212 Spec: the source-evidence ladder is labelled a source-assurance axis, not the `Result` domain (owner: as the requirements say, 2026-11-13) |
| Policy conflict | CONFLICT | CHANGE | `sdlc.md` said a criterion with only cancelled Tasks has no row but readiness needed it accepted; following SDLC-02 and the retirement preconditions, it stays open until the Plan assigns it to a current Task that decides it or the Spec drops it (a draft that let `withdrawal_ref` close it was withdrawn after review) |
| SUP-03 | GAP | CHANGE | `github-governance.md` 1.8.2: any Issue closure; PR template no longer suggests a Project view |
| QA-ALIGN-05 | GAP | CHANGE | Input and Check meaning in `sdlc.md` and the Task template |
| R45-09 | PASS | KEEP | Guards and kept release assets confirmed; name-only guard is H-12 (W05) |
| SemVer boundary | GAP | CHANGE | `documentation-protocol.md` 3.19.0: numbers, baseline resets, completion and merge are not version events |
| SPEC-DISPOSITION | No SUPERSEDE or CANCEL found | KEEP_VALID or REMOVE_AFTER_TRANSFER | 0248, 0249, 0250, 0260, 0264, 0265 have every Task terminal and every criterion decided; they become ready for removal review once their removing Task records the missing Promotion Receipts (W02, owner approval); the rest stay current |
| WP-14, WP-16, WP-22, WP-31 | PASS | KEEP | Owners named in the review; no change |
| WP-15 | PASS (rule), GAP (data) | CHANGE | TSK-0047 and TSK-0055 were `draft` with executed rows; moved to `in-progress` here (H-W04-5) |
| WP-21 | NOT_SELECTED | Handoff | Stage 02 currency against source has no trace since 2026-10-29 |

This run changed `sdlc.md` 1.9.0, `documentation-protocol.md` 3.19.0,
`github-governance.md` 1.8.2, the Stage 03 README 1.3.14, the Task and Plan
templates, the PR template and the SPEC-0212 Spec and Plan. The validator still
accepts a criterion with a PASS on any one pair and does not read promotion
content; until W05 changes it, those two rules are held by review.

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
- Owner choices of 2026-11-13: the evidence ladder follows the requirements
  (a separate labelled axis); TSK-0047 and TSK-0055 text is refreshed now;
  validator enforcement of the new acceptance and readiness rules is W05's.
- The Plan H3 `Owner and Receipt` keeps its W03-pinned name; its prompt now
  says it plans and points to the Task receipt.
- Handoffs, one writer each:

| ID | Writer | Exact difference |
| --- | --- | --- |
| H-W04-1 | W05 | `spec_packages.py` acceptance for decisions under `sdlc.md` 1.9.0 or later: a PASS for every pair assigned to a current, non-cancelled Task (L1752-1763); at least one cited PASS row for the criterion and a cited non-PASS row only when resolved (L1724-1730); cancelled-item pairs stay open; a criterion with a historical PASS on one pair and another pair on a cancelled Task counts under the older-format rule, where the reader now requires every pair historical (L1821-1826); negative tests for each |
| H-W04-2 | W05 | A promotion check: each target document the Promotion Map names appears in a Task receipt or has a no-update reason, and readiness reads it |
| H-W04-3 | W05 | `stale-active` (`lifecycle.py` L708-715) never fires: retarget it to a past `next_review_at` or remove it, with a test |
| H-W04-4 | W05 | Untested branches: Plan ending before its Spec (`spec_packages.py` L676-677), the generation 6 cancelled-Spec path (L668-674), the orphan-Task messages (L1564, L2000, L2539) |
| H-W04-5 | Done here | On the owner's choice of 2026-11-13, TSK-0047 and TSK-0055 moved from `draft` to `in-progress` with Lifecycle Events, and TSK-0055's criterion 108 text, Remaining Conditions and Next Owner and TSK-0047's Next Owner were refreshed; no evidence row changed and criterion 108 stays `pending` |
| H-W04-6 | W11 | WP-21: a Stage 02 currency trace against source and Compose |
| H-W04-7 | W02 | Removal review of 0248, 0249, 0250, 0260, 0264, 0265 after the promotion check |
| H-W04-8 | W01 | Glossary Not-to-Confuse entry for "promotion" used as a status or LAB move (0259, 0261, 0263) |

- Earlier handoffs stay with their owners: W05 H-05, H-08, H-12, OPEN-11;
  W06 H-09, H-10; W07 the Skill section. Q-07 runs only after W11.

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
| Reader regression | 116 | W121 | unit-regression | `test_registry`, `test_spec_packages`, `test_template_definition`, `test_operations_catalog`, `test_surface_ownership` and `check-script-manifest` at `459800639`, Python 3 local | PASS | 413 tests OK in 1075 s; script manifest valid. An earlier run on the uncommitted tree had 4 errors because the Plan named TSK-0063 before its file existed | required | - |
| Policy review | 116 | W121 | independent-review | Fresh-context rules-engineer of the staged policy change on `acef19488` | FAIL | CHANGES_REQUIRED: withdrawal closure contradicted `documentation-protocol.md` and the checklist; readiness had no rule for receipts older Tasks lack; new acceptance rules would have retroactively broken accepted criteria; Start and Block shared one precondition; PR text rule clashed with the PR template; enforcement overstated; receipt commit and terminal Tasks did not fit; Stage 03 README, template, glossary not updated; ten Minor | required | - |
| Policy re-review | 116 | W121 | independent-review | Same reviewer, the staged tree on `acef19488` after the first review's fixes | FAIL | Every earlier finding resolved and TSK-0047/0055 evidence and decisions unchanged; new: the historical-criterion sentence contradicted the older-format rule and the reader, TSK-0063 handoffs and receipt were stale, glossary version not bumped | required | - |

### Resolution Links

Binding RED is resolved by Binding GREEN, and Binding review by Binding re-review.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 116 | pending | Binding GREEN, Binding re-review, Stage 03 checks, Pre-commit, Reader regression | Awaiting the owner's decision | SPEC-0212 TSK-0063 |

### Remaining Conditions

Owner acceptance of criterion 116; push, pull request and merge on the
owner's approval.

## Handoff

### Promotion Receipt

| Criterion | Work Unit | Task result | Target | Consumer update and check |
| --- | --- | --- | --- | --- |
| 116 | W121 | Binding GREEN, Reader regression | `docs/99.templates/registry.json` `common.section_forms` (commit `459800639`) | `spec_packages.py` reader; Reader regression row |
| 116 | W121 | Policy final review, Final checks | `.agents/governance/sdlc.md`, `documentation-protocol.md`, `github-governance.md`, `.agents/knowledge/glossary.md` (this run's policy commit) | Stage 03 README, Task and Plan templates, PR template; Final checks row |

Acceptance row: criterion 116, still `pending`. Residuals: H-W04-1 to H-W04-8.

### Next Owner

The current owner is @buenhyden.
