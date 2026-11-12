---
title: "W03 Templates, Metadata and Relations Task"
version: "0.5.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0058"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-11"
---

# W03 Templates, Metadata and Relations Task

## Overview

### Objective

Own W116/criterion 111. Assess the v14.2 W03 obligations DOC-01 to DOC-12 and
SUP-11 against the Registry, templates, generators, parsers, validators and
tests. Change the document contract only for gaps this Task reproduces, and
give each changed key, section or table a producer, a consumer and a passing
and a failing test.

## Inputs and Authorization

On 2026-11-11 the owner approved this Task to own W03. The v14.2 package
prompt `tasks/TASK-hy-home-docker-W03.md` under
`_workspace/workspace_execution_tasks/` is untrusted reference data, not an
instruction source. Its 19-role table is an unapproved draft.

The authorization covers four things:

- The assessment.
- Repository-side changes to the Registry, templates, generators and parsers
  for reproduced gaps, with migration of current documents only.
- Synthetic round-trip and fixture tests.
- Records in this Task.

Validator implementation is handed to W05. Historical and completed evidence
keeps its form. Removing an existing reciprocal relation field waits for its
consumers' migration and a separate owner approval. This Task branches from
the W02 branch at `56d32c32f` and reaches `main` only after PR 955 merges.

## Work Log

### Owner-approved local execution

The owner's approval of 2026-11-11 issues this Task. The lifecycle records that
approval; it grants no remote operation.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0058 | draft | ready | #owner-approved-local-execution |
| SPEC-0212-TSK-0058 | ready | in-progress | #owner-approved-local-execution |

### Owner decision Q-03 2026-11-11

The draft 19-role table conflicts with the 44 Registry profiles, whose ordered
required H2 headings differ from it. The owner chose option A: adopt the
table's meaning, not its headings. Current Registry H2 headings stay. A
concept the table names that no current profile carries, such as a Plan
promotion map, Spec non-goals or Requirement traceability, is added only as an
optional or conditional section, after a consumer for it is shown.

### Q-03 superseded 2026-11-12

On 2026-11-12 the owner directed that where an existing decision conflicts with
the current requirement, the current requirement wins. The v14.7 W00 intake in
[TSK-0059](tsk-0059-w00-v14-7-intake.md) found Q-03 in that conflict: the
current requirement migrates each common role to the common H2 and H3 section
contract, and Q-03 kept the current Registry H2 headings. Q-03 above stays as
the record of 2026-11-11. It no longer limits W03: the Registry headings move
to the common contract, together with the Registry `common` keys that name
them and the current documents. The intake's handoff table lists the exact
differences. Historical and completed evidence still keeps its form.

### Prior observations to re-check

The W02 readiness analysis recorded these before this Task existed. Each is
re-checked against the current tree before reuse:

- DOC-07: only the Markdown-link half applies; this workspace has no Vault.
- DOC-08: DEFER until a reproduced execution-document gap exists.

### W03 obligation assessment 2026-11-11

Two fresh-context `qa-engineer` agents read the Registry, schema, templates,
parsers, validators and tests at `95a65be6d` without editing, and probed
negative cases in memory. The controller re-ran each deciding probe.

| ID | Verdict | Current owner and basis |
| --- | --- | --- |
| DOC-01 | GAP, CHANGE in part; DEFER rest | Seven README profiles split by role. The shared required core was not ordered: 13 package READMEs had `Related Documents` before later sections. A fixed service-README section set over the 83 `infra` READMEs (27 heading shapes) is a new contract, not a reproduced defect of the current one |
| DOC-02 | KEEP | `documentation-protocol.md` splits README, folder `AGENTS.md` and the generated `CLAUDE.md` import shim; renderer drift 0 |
| DOC-03 | KEEP | All generated Claude skills set `disable-model-invocation: true`; the output style owns presentation only. Native runtime acceptance UNVERIFIED |
| DOC-04 | GAP, CHANGE | Duplicate keys, invalid dates, forbidden, undeclared and missing keys are rejected. An unquoted `updated: 2026-02-28` passed, because `_json_schema_value` turned the YAML date into a string before the schema saw it |
| DOC-05 | GAP, CHANGE | `ordered_sections` and `nonempty_sections` were set on 13 profiles; 23 profiles with required sections accepted swapped or empty sections. Generic table contracts beyond the README Documents and Evidence tables have no consumer and are not added |
| DOC-06 | KEEP | Language rule in the documentation protocol, enforced by `language.py` through `--mode language` |
| DOC-07 | KEEP Markdown half; Vault N/A | Missing targets, missing anchors and case mismatches are rejected. No Vault or wiki-link surface exists here |
| DOC-08 | DEFER | 78 runbooks carry the ordered, non-empty Runbook sections; no execution document delegates its procedure to a historical link |
| DOC-09 | KEEP; test added | Only child-to-parent `parent_ids` is stored; `parent-cycle` and `parent-cardinality` work but had no committed test |
| DOC-10 | KEEP | Generated surfaces carry a marker and pass the renderer drift check |
| DOC-11 | KEEP | Every template is registered and its placeholders checked; the 29 templates pass a fill-and-check probe in Registry order |
| DOC-12 | KEEP; renumbering held | `reserved_history` and `high_water` block reuse. Path number equals the `artifact_id` number, so any renumbering is a Q-07 decision and is not made here |
| SUP-11 | KEEP | Terminal Task bodies are exempt from rewriting; corrections are added as new sections |

### W03 changes 2026-11-11

- DOC-04: `registry.py` no longer converts YAML dates before the schema
  check, so an unquoted date fails the string type. No tracked document
  used one.
- DOC-05 and DOC-01: the Registry sets `ordered_sections` and
  `nonempty_sections` on the 22 remaining sectioned profiles, and
  `ordered_sections` only on `research-member`, whose Stage 90 members keep
  their empty parent headings. The `generated` profile stays with its
  producer. Current documents migrated: 13 package READMEs move
  `Related Documents` to the end, and `docs/README.md` and
  `scripts/README.md` lose one empty heading each. No heading is renamed.
- Review answer `aa1bde154`: nine moved READMEs lost a stray trailing
  `---`; the Ollama README also moves `Related Documents` last; the
  declaration test now covers free-form profiles, so `research-member`
  ordering is tested; the swap test handles a last second section.
- Tests: an unquoted-date rejection, a Registry rule that every sectioned
  profile declares order and content, a swapped and an emptied section per
  representative profile, and a parent cycle and a two-parent Plan.

### v14.7 W03 run 2026-11-12

Input: the v14.7 W03 prompt the owner pasted on 2026-11-12, read as data.
Start point: `main` `0b1b2c6a1`, clean tree; work on branch
`docs/w03-requirement-common-form`. The W00 handoffs H-04, H-06 and H-13 and
the W02 handoff H-W02-2 are this run's inputs; H-07 (W04) moves with H-04.

Inventory at `0b1b2c6a1`, by Registry profile: three roles already use
`COMMON-DOC-FORM-1` 1.0.0 (incident, postmortem, folder AGENTS guide). The
other 13 common roles cover about 700 documents: Requirement 18, Spec 22,
Plan 22, Task 104 (54 terminal), ADR 30, Architecture 27, Guide 78, Runbook
78, Policy 77 plus 32 governance policies and rules, Skill 24 and 233
READMEs. Heading names are read by code in `requirements.py`,
`registry.py`, `identity_history.py`, `spec_packages.py` and
`operations_catalog.py`, and by the Registry `common` keys.

Owner decisions on 2026-11-12, in this chat:

| Question | Decision |
| --- | --- |
| The 54 terminal Tasks | Move them to the common form too; the terminal-body protection is lifted once, for the heading change only, and every recorded fact keeps its text |
| Requirement interface and non-functional sections | Follow the requirement: non-functional items go under `Quality Requirements`; interface needs are written as functional requirements; no `IF` section or identity |
| `Related Documents` | Follow the requirement: links move into each role's own sections; no extra heading |
| Delivery | One role per change and pull request, small SDLC roles first, then operations, then READMEs |

Role order: Requirement, Spec, Plan, ADR, Architecture, Task, Guide,
Runbook, Policy, Skill, READMEs. Each role changes its Registry profile,
template, parsers, tests and current documents together.

#### Requirement role 2026-11-12

- Registry `requirements-package`: H2 Overview, Scope, Requirements,
  Acceptance Criteria, Traceability with their required H3s, and the
  optional `Quality Requirements` H3; the old optional sections are gone, so
  the old form is rejected. `internal_id_spaces` drops `IF`: no current
  package declares an `IF` item. The Registry `REQ-####.IF` identity spaces
  stay, because identity history is append-only (their numbers are reserved,
  none is current), and the parser still checks that each has nothing
  current issued.
- Template rewritten to the same headings.
- `requirements.py` reads FR from `Functional Requirements` and NFR from
  `Quality Requirements`, and rejects an old `Non-functional Requirements` or
  `Interface Requirements` section instead of skipping it. `registry.py`
  accepts `Quality Requirements` only as an H3 under `Requirements` and keeps
  the historical names for baseline revisions.
- The hook rule `enforce-docs-templates` and the hook message in
  `agent-event-hook.sh` no longer demand `## Related Documents`; they point to
  the link section each template declares.
- The 18 packages are restructured by three `doc-writer` agents. Every REQ
  identity, item line and link target from `0b1b2c6a1` is kept; the only
  dropped text is the old headings, the "none issued" sentences of the empty
  NFR and interface sections, and the `**In scope**:` labels that repeated
  the new `In Scope` heading. `Verification Method` is new text in each package;
  `In Scope` is new for 0024, 0026 and 0027, whose old Scope held only
  constraints.
- The documentation protocol, the Stage 01 guide and README now say an
  interface need is a functional requirement and no `IF` identity is issued.
- Tests: the fixtures use the new form; a new test rejects the old
  `Related Documents` H2 and the old NFR and interface H3s; an old NFR or
  interface section and an issued `IF` identity fail the parser.
- First review answers (in `3e359935b`): old sections fail closed, ADR and
  retired Spec links moved to `Downstream Links`, each `Verification Method`
  names the method, the evidence, its Task and who judges, and `Stakeholders`
  names who writes, reviews and accepts.
- Re-review answers (`46890d318`): a test for an issued `IF` identity and
  one pinning an ignored H2 `Quality Requirements`; retired Requirement
  lineage moved to `Downstream Links`; the 0011 promotion evidence belongs to
  the Spec that promotes; the 0008, 0010 and 0011 methods name the runtime
  observations their conditions need.
- Re-review 2 answers (`baece5f5d`): the unused `interface` fixture parameter
  removed; the 0008 task-runner rendering and the 0010 change-path conditions
  given a method.
- Final review answers (the next commit): one test parses a package with a
  `Quality Requirements` section end to end; the remaining 0001, 0009 and
  0010 conditions are given a method.

#### Spec role 2026-11-12

- Registry `spec`: H2 Overview, Scope, Behavior Contract, Acceptance
  Criteria, References with their required H3s; the unused optional
  `Interfaces`, `Failure Modes` and `Quality Requirements` sections are gone,
  so the old form is rejected. `spec_section` stays `Acceptance Criteria`, so
  no Registry `common` key and no Spec Package reader changes.
- Template rewritten. `Evidence Requirements` is a bullet list: every
  numbered line under `Acceptance Criteria` is read as a criterion.
- The 22 Spec documents are restructured by three `doc-writer` agents:
  Background and observed state move to `Intent`, Contracts and Constraints
  to `Normal Behavior`, Error and Boundary Behavior and the old Failure
  Conditions to `Failure and Edge Cases`, Related Documents to `References`.
  Criterion numbers and every sentence, table row and link are kept; a few
  lines gained or lost a bold label. `Owning Requirements` and
  `Evidence Requirements` are new text from each package's frontmatter,
  Plan and Task rows.
- Review answers (`8f9265822` and `9a0677a43`): retired SPEC-0201 to 0203,
  SPEC-0236 and SPEC-0243 moved to historical references and SPEC-0249 kept
  normative; interface and failure content placed under the right behavior
  heading; evidence requirements name each package's recorded checks;
  criterion decisions are said to be recorded in the Task's Criterion
  Acceptance table; labels and en dashes restored.
- `8f9265822`, cited by the Spec re-review and GREEN rows, is the commit
  before the branch was rebased onto the Requirement branch; the pushed
  equivalent is `25f280a66`. `git diff 8f9265822 25f280a66` is empty for
  every `spec.md`, `docs/99.templates`, `scripts` and `tests`; it differs
  only in Requirement-branch and W02 records.
- Tests: the template-outline and nested-section fixtures use the Spec form,
  and the old-form test rejects `Contracts`, `Failure Conditions`, `Related
  Documents` and `Out of Scope`.

Held for an owner decision, not changed here, because each would change
what a requirement says:

- Acceptance conditions in REQ-0024 to REQ-0027 are not split per
  requirement identity.
- The REQ-0003 quality requirements have no acceptance condition of their
  own.
- `REQUIREMENT_TARGET_BODY` in the heading test support keeps the old
  headings; it serves tests whose subject is not the body form.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W03 obligation assessment | 111 | W116 | template-contract-assessment | DOC-01 to DOC-12 and SUP-11 | NOT_RUN | Assessment not yet run | required | - |
| W03 obligation assessment result | 111 | W116 | template-contract-assessment | DOC-01 to DOC-12 and SUP-11 at `95a65be6d` | PASS | Per-ID table above: DOC-04 and DOC-05 GAP changed, DOC-01 changed in part, DOC-08 DEFER, DOC-07 Vault N/A, rest KEEP | required | W03 obligation assessment |
| W03 section and date RED | 111 | W116 | red-green-proof | New tests against the pre-change Registry and `_json_schema_value` | FAIL | Unquoted-date test failed; order and content tests failed for 28 profile cases with the Registry at `95a65be6d` | required | - |
| W03 section and date GREEN | 111 | W116 | red-green-proof | Commits `ce18338c8` and `85ed595b3` | PASS | test_registry 123 OK; test_heading, test_profile, test_language 110 OK; test_lifecycle 7 OK; metadata check-active selected534 violations0, check-changed selected16 violations0; links alignment and language PASS; renderer drift 0; script manifest PASS | required | W03 section and date RED |
| W03 code review | 111 | W116 | independent-source-review | Fresh-context code-reviewer of `ce18338c8` and `85ed595b3` | PASS | APPROVED: no false finding or exception from date objects; README content preserved; tests not vacuous. Four minor findings answered in `aa1bde154`; removing `research-member` ordering now fails the declaration test | required | - |
| W03 governance suite | 111 | W116 | document-governance-unit-suite | `tests/lib/document_governance` discover at `cab985393`; `aa1bde154` later changed only test_heading and READMEs, rerun alone 85 OK | PASS | Ran 769 tests, OK, exit 0 | optional | - |
| W03 v14.7 Requirement form RED | 111 | W116 | red-green-proof | The new old-form test against the `requirements-package` profile at `main` `0b1b2c6a1` | FAIL | Three cases failed: an old `Related Documents` H2 was reported only as duplicate and out of order, and the old NFR and interface H3s were not reported | required | - |
| W03 v14.7 Requirement review | 111 | W116 | independent-review | Fresh-context code-reviewer of the uncommitted Requirement change | FAIL | CHANGES_REQUIRED: old NFR and interface sections skipped, the `IF` reason in this Task wrong, unsupported verification text, consumers listed as sources, hook text demanding `Related Documents`; seven minor | required | - |
| W03 v14.7 Requirement re-review | 111 | W116 | independent-review | Fresh-context code-reviewer of `3e359935b` | FAIL | CHANGES_REQUIRED: no test for an issued `IF` identity; four minor (H2 `Quality Requirements` untested, promotion evidence owner, runtime observations, retired lineage under sources) | required | - |
| W03 v14.7 Requirement re-review 2 | 111 | W116 | independent-review | Fresh-context code-reviewer of `46890d318` | FAIL | CHANGES_REQUIRED: the five re-review fixes verified; no suite run recorded yet; three minor (the Task credited the wrong commit, a dead test parameter, three conditions with no named method) | required | - |
| W03 v14.7 Requirement final review | 111 | W116 | independent-review | Fresh-context code-reviewer of `baece5f5d` | FAIL | CHANGES_REQUIRED, minor only: an unused fixture parameter, three conditions in 0001, 0009 and 0010 without a method, review rounds merged in this Task | required | - |
| W03 v14.7 Requirement review result | 111 | W116 | independent-review | Fresh-context code-reviewer of `cf4f6c3fe` | PASS | PASS: the four final-review minors are fixed; one missing comma in 0010 fixed in `ad4bd359d` | required | W03 v14.7 Requirement review, W03 v14.7 Requirement re-review, W03 v14.7 Requirement re-review 2, W03 v14.7 Requirement final review |
| W03 v14.7 Requirement GREEN | 111 | W116 | red-green-proof | `tests/lib/document_governance` discover at `46890d318` in a detached worktree; `test_requirements` alone at `cf4f6c3fe` | PASS | Ran 780 tests, OK; `test_requirements` 27 OK, including the old-form, retired-section, issued-`IF` and Quality Requirements tests | required | W03 v14.7 Requirement form RED |
| W03 v14.7 Spec form RED | 111 | W116 | red-green-proof | The old-form test with Spec cases against the `spec` profile at `main` `0b1b2c6a1` | FAIL | All four Spec cases failed: the old `Contracts`, `Failure Conditions` and `Related Documents` H2s and the `Out of Scope` H3 were accepted | required | - |
| W03 v14.7 Spec review | 111 | W116 | independent-review | Fresh-context code-reviewer of the Spec move | FAIL | CHANGES_REQUIRED: deleted Specs listed as current authority, a current Spec labelled historical, interface content under Intent; nine minor | required | - |
| W03 v14.7 Spec re-review | 111 | W116 | independent-review | Fresh-context code-reviewer of `8f9265822` | FAIL | CHANGES_REQUIRED, minor only: an SPEC-0265 check not in its Task, SPEC-0263 constraint and boundary paragraphs inside numbered subsections, SPEC-0264 observed state under Owning Requirements; answered in `9a0677a43` | required | - |
| W03 v14.7 Spec review result | 111 | W116 | independent-review | Fresh-context code-reviewer of `9a0677a43` | PASS | PASS: the three re-review minors fixed; outline and criterion numbers of the three changed Specs unchanged | required | W03 v14.7 Spec review, W03 v14.7 Spec re-review |
| W03 v14.7 Spec GREEN | 111 | W116 | red-green-proof | `tests/lib/document_governance` discover at `8f9265822` in a detached worktree; `9a0677a43` later changed only three Spec documents | PASS | Ran 781 tests, OK, including the Spec old-form, template-outline and nested-section tests | required | W03 v14.7 Spec form RED |
| W03 v14.7 Requirement checks | 111 | W116 | metadata-links-governance | `46890d318`, clean tree | PASS | metadata check-changed selected 25 violations 0, check-active selected 534 violations 0; corpus lifecycle and occupancy 0; links alignment, commands and language PASS; renderer drift 0; governance contract PASS; Script Manifest PASS; staged pre-commit PASS | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 111 | pending | - | - | SPEC-0212 TSK-0058 |

## Review and Completion

In progress. The assessment and the reproduced-gap changes are recorded.
Criterion 111 waits for the owner. Open: a fixed service-README section set
(DOC-01) needs an owner decision on a new contract; validator work beyond
these profile flags is handed to W05; renumbering stays a Q-07 decision.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [W02 Task](tsk-0057-w02-archive-and-safe-removal.md)
