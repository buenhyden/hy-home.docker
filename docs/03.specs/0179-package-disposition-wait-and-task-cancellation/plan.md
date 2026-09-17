---
title: "Package Disposition Wait and Task Cancellation Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-17"
layer: "specs"
artifact_id: "SPEC-0179-PLAN-0001"
parent_ids:
- "SPEC-0179"
created: "2026-09-17"
---

# Package Disposition Wait and Task Cancellation Implementation Plan

## Objective

Admit a completed Stage 03 package whose every member is terminal to wait for
its disposition, admit a `cancelled` Task that carries a valid structured
`cancellation`, read the Stage 03 terminal statuses from the Registry, and
accept `ADR-0037` in the result tree that makes each of those checks live.

## Dependencies

- `common.archive_disposition_model` is `adopted` and `ADR-0036` is `accepted`,
  which held on `main@2edac5bd6`.
- The operator approved the design and the Spec on 2026-09-17, and answered the
  Spec's Open Question by default: `ADR-0036` is preserved under
  `docs/98.archive/superseded/` in the result tree that accepts `ADR-0037`, as
  SPEC-0178 did for `ADR-0035`.
- Each document admits one lifecycle transition per integration, judged against
  the upstream base, and no forward edge skips a state. The Spec moves `draft`,
  `review`, `approved`, `active`, `completed`; this Plan moves `draft`,
  `approved`, `active`, `completed`; and the Task moves `draft`, `ready`,
  `in-progress`, `completed`. The package therefore takes four integrations:
  review with W1; approval with W2; activation and acceptance with W3 to W7; and
  completion with W8. Under Behavior Contract 2, which W3 makes live, the
  completed package waits in Stage 03 after W8, and its move under the archive
  is a fifth integration that needs its own disposition approval.
- An integration reaches the upstream base only through a route the operator
  authorizes for it. No push is authorized when this Plan is written, so W2 does
  not start until the route for W1 is decided.

## Execution Sequence

Two steps precede the sequence and carry no acceptance criterion, so they are
recorded here rather than numbered as work units: W1, which narrows the Spec's
Registry scope after measuring the lifecycle terminal sets, adds this Plan and
its Task as drafts, and puts the Spec to review once the proposal commit is
integrated upstream, because the metadata check requires a package new to the
upstream base to start at `draft`; and W2, which obtains an
independent approval review, settles its findings, approves the Spec and this
Plan, and makes the Task `ready`. The registered completion contract requires a
receipt for every numbered work unit, and neither produces acceptance evidence.

1. W3: Occupancy reads the `spec`, `plan`, and `task` lifecycle terminal
   statuses from the Registry and judges a package whose Spec is `completed`.
   `validate_active_stage_occupancy(root, registry=None)` gains the optional
   `DocumentRegistry` argument; `None` loads `docs/99.templates/registry.json`
   under `root`, falling back to the repository Registry when the fixture has
   none. Tests first, in `test_stage_03_occupancy_is_judged_per_package`: extend
   the fixture helper to write `artifact_id` and an optional `cancellation`
   block, then add a subtest per row of Behavior Contracts 2 to 5, and a new
   `test_stage_03_occupancy_reads_registry_lifecycles` that passes a Registry
   whose `task` lifecycle drops `cancelled` from `terminal_statuses` and expects
   a Stage 03 result change with an unchanged Stage 02 result. Run
   `python3 -m unittest tests.lib.document_governance.test_archive` and record
   the failure before editing `archive.py`. Files:
   `scripts/lib/document_governance/archive.py`,
   `tests/lib/document_governance/test_archive.py`.
2. W4: One pure cancellation judgment. Add
   `task_cancellation_findings(task_id: str, cancellation: object, criteria:
   frozenset[int], task_statuses: Mapping[str, str]) -> tuple[str, ...]` and
   `acceptance_criterion_numbers(spec_body: str, heading: str) ->
   tuple[int, ...]` to `spec_packages.py`; make
   `_validate_completion_evidence` call the second instead of its inline
   pattern; call the first from `_load_package` and raise `SpecPackageError`
   on its first finding; and call it from the W3 occupancy branch for every
   `cancelled` Task. Tests first in `test_spec_packages.py`: one subtest per
   invalid form in acceptance criterion 3, one for the empty `criteria` list,
   one for criterion 4 (a `withdrawn`-only criterion still fails completion),
   and one for criterion 5 (a waiting completed package with a malformed
   receipt reports the receipt finding). Files:
   `scripts/lib/document_governance/spec_packages.py`,
   `scripts/lib/document_governance/archive.py`,
   `tests/lib/document_governance/test_spec_packages.py`,
   `tests/lib/document_governance/test_archive.py`.
3. W5: Register `cancellation`. Add it to the `task` profile's
   `optional_frontmatter` and to `required_frontmatter_by_status` under
   `cancelled`, and declare its object shape (`reason`, `approved_by`,
   `approved_at` as `date`, `criteria` as an array of objects with integer
   `criterion` and exactly one of `reassigned_to` or `withdrawn`) in the
   frontmatter schema. Tests first in `test_registry.py`: missing key, null,
   empty string, and whitespace-only value at `cancelled` each report
   `status-frontmatter-required`; a Task at `in-progress` without the key
   passes; and a scalar value fails the schema. Files:
   `docs/99.templates/registry.json`,
   `docs/99.templates/contracts/document-frontmatter.schema.json`,
   `tests/lib/document_governance/test_registry.py`.
4. W6: Template and Stage 99 guidance. Add an author-prompt comment to
   `task.template.md` that names `cancellation` and when it is required, seed
   no value, and describe the field where the Stage 99 README describes the
   Task profile. Test first: render the Task template with `status:
   "cancelled"` into a temporary tree and expect the metadata check to fail
   until `cancellation` is supplied. Files:
   `docs/99.templates/templates/specs/task.template.md`,
   `docs/99.templates/README.md`,
   `tests/lib/document_governance/test_registry.py`.
5. W7: In the result tree that lands W3 to W6: accept `ADR-0037` with
   `supersedes: ["ADR-0036"]` and the retained rules restated; add
   `superseded_by: "ADR-0037"` to `ADR-0036` and preserve it under
   `docs/98.archive/superseded/02.architecture/decisions/` with its Retention
   Catalog row; repoint every active document that links `ADR-0036` by path or
   labels its status; amend REQ-0026-FR-0009 and any Acceptance Criterion that
   restates it, the Retention by status paragraphs of
   `.agents/governance/documentation-protocol.md`, the completion item of
   `.agents/governance/task-checklists.md`, any `AD-0030` restatement, and the
   Stage 03 README rule for a waiting package's row; and search the active
   corpus for "cancelled Task stays a finding" and for text binding the
   terminal transition to the move, so that none remains.
6. W8: Run the changed profile, obtain an independent exact-diff review, write
   the completion receipt, and set the Spec, this Plan, and the Task to
   `completed`. The package then waits in Stage 03 under Behavior Contract 2.

| Acceptance criterion | Work unit |
| --- | --- |
| 1 | W3 |
| 2 | W5 |
| 3 | W4 |
| 4 | W4 |
| 5 | W4 |
| 6 | W3 |
| 7 | W6 |
| 8 | W7 |
| 9 | W7 |
| 10 | W8 |

## Risk and Rollback

| Risk | Guard | Recovery |
| --- | --- | --- |
| A check goes live before `ADR-0037` is accepted | W3 to W7 land in one result tree | Revert that integration; `ADR-0037` stays `proposed` |
| Occupancy fixtures without a Registry break | `registry=None` falls back to the repository Registry | Pass an explicit fixture Registry |
| A Registry-wide terminal union is used by mistake | Behavior Contract 5 and criterion 6 keep the Stage 02 result unchanged | Restore the per-document set |
| Local commits stack two lifecycle transitions against the base | Each integration waits for its authorized route | Squash back to one transition per document, never rewrite a pushed commit |
| A frozen body is edited while preserving `ADR-0036` | The Retention Catalog `Source` comparison | Restore the body from its `Source` object |

## Verification

Each work unit records its failing test run before the implementation and its
passing run after, with command, snapshot, place, and exit code, in the Task.
The W3 to W7 integration runs `python3 scripts/validation/run-ci-gate.py
--profile changed` on the index snapshot. An all-files run needs its own
approval. Hosted CI and live checks are not run by this Plan and are recorded
as NOT_RUN with that reason. W1 and W2 carry no acceptance criterion and are
evidenced by their Work Log entries alone.

## Rulings

- No sealed record or frozen body is edited.
- Tests are written first and fail first for every rule W3 to W6 add.
- `TERMINAL_DOCUMENT_STATUSES` and `_TERMINAL_STATUSES` stay unchanged.
