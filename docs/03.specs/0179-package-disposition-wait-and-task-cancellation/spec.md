---
title: "Package Disposition Wait and Task Cancellation Specification"
version: "0.2.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-17"
layer: "specs"
artifact_id: "SPEC-0179"
parent_ids:
- "REQ-0026"
- "AD-0030"
created: "2026-09-17"
---

# Package Disposition Wait and Task Cancellation Specification

## Overview

On `main@2edac5bd6` the occupancy check rejects two states that record true
facts. A `cancelled` Task inside an unfinished package is always a finding, so a
Task that was really cancelled must read `in-progress` or `blocked`, or be
deleted with its evidence. A `completed` Spec or Plan in an active Stage 03 is
always a finding, so completion and disposition are bound into one commit, the
completion receipt check first runs in that moving commit, and the unit's
`Source` cannot be the finished original.

`ADR-0037` proposes the resolution: a completed package whose every member is
terminal may wait for its disposition where it stands, and a cancelled Task is
admitted when a structured `cancellation` records its reason, its approval, and
where each of its acceptance criteria went. This package moves the checks, the
Registry profile, and the governing text onto that decision, and accepts
`ADR-0037`, superseding `ADR-0036`, in one result tree.

This is the first of several changes toward the documentation standard the
operator set on 2026-09-17. The exact identity comparison for a separately
prepared original, post-archive reassessment, citation order, index separation,
and status vocabulary migration are later packages and are not decided here.

## Boundaries and Inputs

- Inputs: `ADR-0037`, `ADR-0036`, the Retention by status and Retirement
  preconditions sections of `.agents/governance/documentation-protocol.md`,
  REQ-0026-FR-0009, and `.agents/governance/task-checklists.md`.
- Precondition: `common.archive_disposition_model` is `adopted` and `ADR-0036`
  is `accepted`. Both held on `main@2edac5bd6`.
- In scope:
  - `scripts/lib/document_governance/archive.py`:
    `validate_active_stage_occupancy`, whose Stage 03 branch reads the `spec`,
    `plan`, and `task` lifecycle terminal statuses from the Registry.
  - `scripts/lib/document_governance/spec_packages.py`: one pure cancellation
    judgment that both package validation and the occupancy check call.
  - The `task` profile in `docs/99.templates/registry.json`: `cancellation` as
    optional frontmatter and as `required_frontmatter_by_status` for
    `cancelled`, with its value shape in
    `docs/99.templates/contracts/document-frontmatter.schema.json`.
  - `docs/99.templates/templates/specs/task.template.md` guidance and the
    Stage 99 README text that describes the Task profile, without seeding a
    `cancellation` value.
  - The tests under `tests/lib/document_governance/` that cover each behavior.
  - The acceptance of `ADR-0037` and its supersession of `ADR-0036`; the
    in-place amendment of REQ-0026-FR-0009 and any `REQ-0026` Acceptance
    Criterion that restates it; the policy paragraphs under Retention by status
    that bind the terminal transition to the move and reject a `cancelled` Task;
    the completion item in `.agents/governance/task-checklists.md`; the
    `AD-0030` statement of occupancy if it restates the rejected rule; the
    Stage 03 README rule for how a waiting package's row reads; and every
    active document that links `ADR-0036` by path or states its status as
    current authority. A dated observation in a Stage 90 record is not
    repointed.
- Out of scope: any edit to a frozen body or sealed record; changing the
  `Source` comparison or `common.frozen_transition_fields`; a disposition wait
  for a package whose Spec is `cancelled` or `superseded`; splitting the
  Stage 03 index into current work and history; renaming any lifecycle status;
  moving any existing package; and the per-document terminal set that
  `TERMINAL_DOCUMENT_STATUSES` in `archive.py` and `_TERMINAL_STATUSES` in
  `spec_packages.py` hold. Those sets mean "a status that leads to a Stage 98
  disposition", which no Registry field states today: the union of the
  Registry lifecycle terminal statuses also holds `rejected`, `resolved`,
  `published`, `sealed`, and the template lifecycle's `draft`, and
  `_TERMINAL_STATUSES` holds `retired`, which no Stage 03 lifecycle lists.
  Replacing either set changes judgments outside this package, so it belongs
  to the later status vocabulary change.

## Behavior Contract

1. Stage 03 occupancy stays a package judgment, and the terminal statuses it
   uses for a Spec, a Plan, and a Task are read from the Registry `spec`,
   `plan`, and `task` lifecycles.
2. A package whose Spec is `completed` passes occupancy when its Plan, if
   present, is `completed` and every Task is `completed` or is a `cancelled`
   Task with a valid `cancellation`. In such a package a Plan that is not
   `completed`, a Task that is not terminal, and a `cancelled` Task without a
   valid `cancellation` are each a finding.
3. A package whose Spec is `cancelled` or `superseded` keeps no member in an
   active Stage 03, as before.
4. Inside a package whose Spec is not terminal, a `completed` Task passes, a
   `cancelled` Task with a valid `cancellation` passes, a `cancelled` Task
   without one is a finding, and a terminal Plan is a finding.
5. A standalone document in Stages 01, 02, 05, or 90 is judged per document, as
   before.
6. A `cancelled` Task without `cancellation`, or with a null, empty, or
   whitespace-only value, is a `status-frontmatter-required` finding. A Task in
   any other status is not required to carry `cancellation`.
7. A `cancellation` is valid only when `reason` and `approved_by` are nonempty
   strings, `approved_at` is a valid `YYYY-MM-DD` date, and `criteria` is a
   list whose every entry has an integer `criterion` present in the Spec's
   Acceptance Contract numbering and exactly one of `reassigned_to` or
   `withdrawn`. `reassigned_to` names a Task identity in the same package that is
   not the cancelled Task and is not itself `cancelled`. `withdrawn` is a
   nonempty reason. An empty `criteria` list is valid and states that the Task
   held no criterion.
8. `withdrawn` does not exempt the completion receipt: a completed Spec still
   needs PASS evidence for every criterion its Acceptance Contract numbers.
9. The completion receipt check runs on a completed package that waits in
   Stage 03, so its findings surface before any move.
10. No template seeds `cancellation`, and a document generated from the Task
    template in `cancelled` status fails until an author supplies it.

## Technical Approach

`validate_active_stage_occupancy` already groups Stage 03 members by package
and reads the Spec status once. It gains an optional `registry` argument that
defaults to the repository Registry, classifies a member as Spec, Plan, or Task
by the package-relative path it already uses, reads the terminal statuses of the
matching lifecycle from `DocumentRegistry.lifecycle_terminal_statuses`, and
replaces the fixed branch that rejects a terminal Spec with the table in
Behavior Contracts 2 to 4.

`spec_packages.py` gains one public pure function,
`task_cancellation_findings(task_id, cancellation, criteria, task_statuses)`,
which takes the Task identity, the `cancellation` value, the criterion numbers
of the Spec's Acceptance Contract, and a mapping of every Task identity in the
package to its status, and returns a tuple of finding strings. Package
validation calls it from `_load_package` and raises `SpecPackageError` on the
first finding. The occupancy check calls the same function with the values it
reads from frontmatter and the Spec body, so the rule lives in one function and
the occupancy fixtures need no complete package. The criterion numbers come from
one section reader, `acceptance_criterion_numbers(spec_body, heading)`, factored
out of `_validate_completion_evidence` so both call it rather than copying the
pattern.

The presence rule in Behavior Contract 6 uses the Registry's existing
`required_frontmatter_by_status` contract, which `incident` applies to
`resolved_at` and `postmortem` applies to `reviewed_at`. The value shape is an
object in the frontmatter schema so that the metadata check rejects a scalar
before the package check reads it.

The per-document branch for Stages 01, 02, 05, and 90 keeps
`TERMINAL_DOCUMENT_STATUSES` unchanged, for the reason Boundaries and Inputs
gives.

Every behavior lands in the result tree that accepts `ADR-0037`. No Registry
switch is added.

## Interfaces and Data

`check-document-corpus-lifecycle.py` and `check-document-metadata.py` keep their
arguments and exit contract. The `task` profile gains:

```yaml
# doc-paths: illustrative
status: "cancelled"
cancellation:
  reason: "Merged into the scope of TSK-0003"
  approved_by: "@buenhyden"
  approved_at: "2026-09-17"
  criteria:
  - criterion: 3
    reassigned_to: "SPEC-0179-TSK-0003"
  - criterion: 5
    withdrawn: "Criterion 5 is amended out of the Spec in the same change"
```

New `SpecPackageError` messages name `cancellation` and the invalid field.
Occupancy findings keep the form `<path>: <reason>`, with a new reason for a
nonterminal member of a completed package.

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| --- | --- |
| A completed package takes new work while waiting | Behavior Contract 2 makes any nonterminal member a finding |
| A Task is marked `cancelled` to drop an unmet criterion | Behavior Contract 8 keeps the completion receipt over every Spec criterion |
| A criterion is reassigned to a Task that does not exist or is cancelled | Behavior Contract 7 checks identity, package membership, self, and status |
| Two cancelled Tasks reassign to each other | Neither target may be `cancelled`, so the cycle has no valid edge |
| A template or status alias produces an approval | Behavior Contract 10 keeps `cancellation` out of every template |
| A cancelled Spec package waits indefinitely without a withdrawal record | Behavior Contract 3 keeps it a finding |
| A terminal status is added to a Stage 03 lifecycle and occupancy misses it | Behavior Contract 1 reads the Registry, and a test changes a fixture Registry to prove it |
| A Registry-wide terminal union is used for standalone documents and rejects resolved Incidents or rejected ADRs | The per-document set is out of scope and unchanged |
| A waiting package is read as disposition approval | `ADR-0037` Decision 2 and the Stage 03 README row rule state it is not |

## Acceptance Contract

1. Tests written first and failing first prove Behavior Contracts 2 to 5 for
   each row: a waiting completed package passes; a completed package with a
   `draft`, `ready`, `in-progress`, or `blocked` Task, or with an `active` Plan,
   fails; a `cancelled` or `superseded` Spec package fails; in an unfinished
   package a `completed` Task passes, a validly cancelled Task passes, a
   cancelled Task without `cancellation` fails, and a terminal Plan fails; a
   superseded standalone decision in Stage 02 fails.
2. Tests prove Behavior Contract 6 for a missing key, null, empty string, and
   whitespace-only value, and prove a non-cancelled Task needs no
   `cancellation`.
3. Tests prove Behavior Contract 7 for each invalid form: missing or empty
   `reason` or `approved_by`, an invalid `approved_at`, a non-list `criteria`,
   an unknown criterion number, an entry with both or neither of
   `reassigned_to` and `withdrawn`, a reassignment to a missing Task, to itself,
   and to a cancelled Task; and prove an empty `criteria` list passes.
4. A test proves Behavior Contract 8: a completed package whose only coverage of
   a criterion is a `withdrawn` entry fails completion.
5. A test proves Behavior Contract 9: a waiting completed package with a
   malformed completion receipt reports the receipt finding from Stage 03.
6. A test proves Behavior Contract 1 by passing a Registry whose `task`
   lifecycle lists different terminal statuses and observing the Stage 03
   occupancy result change, while the Stage 02 per-document result does not.
7. Rendering the Task template with `status: "cancelled"` fails the metadata
   check until `cancellation` is supplied, proving Behavior Contract 10.
8. REQ-0026-FR-0009, the Retention by status section, the completion item in
   `task-checklists.md`, and any `AD-0030` restatement describe the waiting
   state and the cancellation contract, and no active document still states that
   a `cancelled` Task is always a finding or that the terminal transition and
   the move must share one change.
9. `ADR-0037` is `accepted` with `supersedes: ["ADR-0036"]`, `ADR-0036` carries
   `superseded_by: "ADR-0037"` and is preserved under the archive's
   `superseded/` class with its catalog row, and every active document that
   linked `ADR-0036` as current authority links `ADR-0037`.
10. The Stage 03, Stage 02 decisions, and Stage 98 README entries for this
    package and both decisions match the tree, and the corpus lifecycle,
    metadata, and link checks pass on the result tree, recorded in the Task
    with command, snapshot, place, and exit code.

## Traceability

- [REQ-0026 문서 보존 및 은퇴](../../01.requirements/0026-document-retention-and-retirement.md)
- [AD-0030 문서 Lifecycle 거버넌스](../../02.architecture/descriptions/0030-document-lifecycle-governance.md)
- [ADR-0037 완료 package의 처분 대기와 Task 취소](../../02.architecture/decisions/0037-package-disposition-wait-and-task-cancellation.md)
- [ADR-0036 보존 대기 package, route 기록 인용, frozen 동일성](../../02.architecture/decisions/0036-archive-occupancy-citation-and-frozen-identity.md)

## Open Questions

None. On 2026-09-17 the operator settled the one question this Spec raised:
`ADR-0036` is preserved under `superseded/` in the result tree that accepts
`ADR-0037`, as SPEC-0178 did for `ADR-0035`, because the waiting state covers
Stage 03 packages only and a standalone decision keeps the per-document rule.

## Operational Impact

None at runtime. No Compose service, container, volume, network, secret, or
remote system is read or changed. The change affects document authors and the
local and hosted document governance checks only.
