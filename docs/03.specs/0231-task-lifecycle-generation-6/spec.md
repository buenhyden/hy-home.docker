---
title: "Task Lifecycle Generation 6"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0231"
parent_ids:
- "REQ-0024"
- "AD-0030"
- "ADR-0048"
created: "2026-10-13"
---

# Task Lifecycle Generation 6

## Overview

Lifecycle generation 5 records execution state twice. A Task's frontmatter
`status` is the execution state, and the Spec and Plan statuses must project
it: `in-progress` while any Task runs, `blocked` when every remaining Task is
blocked, and `completed` before a package may wait in Stage 03 for archive
review. Acceptance is the last column of every Evidence row, so one criterion
can carry many independent decisions, and a `FAIL` row with `pending`
acceptance blocks nothing. On `main` `2a57d4122` the 52 Stage 03 Tasks hold
560 Evidence rows: 275 `accepted`, 275 `pending`, 9 `rejected`, 1
`not-required`; 60 rows are `FAIL`.

The prompt v9 request (findings F03 and F06) and the owner's decisions on
2026-10-13 ask for one execution-state owner, one acceptance decision per
criterion, an optional multi-item Task mode, and archive readiness that reads
those owners instead of a `completed` parent status.

## Scope

In scope: the Registry common contract and the `spec`, `plan` and `task`
lifecycles and profiles; the frontmatter and profile schemas; the Task
template; the Stage 03 reader in `scripts/lib/document_governance/`
(`spec_packages.py`, `archive.py` and their callers); the governance and
README text that states these rules; REQ-0026-FR-0009, AD-0030 and a new
ADR-0048 that replaces ADR-0037 decisions 1 to 3; the migration of active
Stage 03 documents; and the tests that pin these behaviors.

Out of scope: frozen archive bodies under `docs/98.archive/`, which keep the
meaning of the generation that wrote them; generation 4 historical Task
bodies, which must stay byte-identical; Issue and Project projection; and
archive approval itself, which stays a separate owner decision.

## Contracts

1. **Parent authority.** Spec and Plan statuses are `draft`, `in-review`,
   `approved`, `cancelled` and `superseded`. Allowed edges: `draft` to
   `in-review`, `approved`, `cancelled` or `superseded`; `in-review` to
   `draft`, `approved`, `cancelled` or `superseded`; `approved` to
   `in-review`, `cancelled` or `superseded`. A Plan cannot be `approved`
   while its Spec is not. Parent status never reflects Task execution.
2. **Single-mode Task.** A Task without an Execution Items table keeps one
   frontmatter `status` from the unchanged Task lifecycle.
3. **Multi-item Task.** A Task whose Work Log holds an `Execution Items`
   table with at least two rows (`Item | Work Unit | Scope | Owner | Status |
   Blocker`) must not declare a frontmatter `status`. Each row owns its
   status from the Task lifecycle, and each Work Unit belongs to one item. A
   summary status is derived on read and never written.
4. **Evidence.** The Evidence table is `Evidence | Criteria | Work Unit |
   Check | Input | Result | Location | Resolves`. Evidence names are unique in
   the Task. `Resolves` is `-` or names earlier `FAIL` rows of the same Task
   that this row, a `PASS` for a shared criterion, resolves. Evidence records
   observations only.
5. **Criterion acceptance.** A `Criterion Acceptance` section holds `Criterion
   | Acceptance | Evidence | Decision`. Every Spec criterion has exactly one
   row in exactly one Task of the package that the Plan assigns it to.
   `accepted` requires at least one `PASS` row for that criterion in the
   package and no unresolved `FAIL` row for it; `not-required` and `rejected`
   need a nonempty Decision; `pending` is the default.
6. **Task completion.** A single-mode Task, or an item, may be `completed`
   only when every Work Unit it owns has a `PASS` row and every criterion row
   it owns is `accepted` or `not-required`. Cancellation keeps the generation
   5 `cancellation` record.
7. **Archive readiness.** A package is ready for archive review, a derived
   view that is never stored, when its Spec and Plan are `approved` (or
   validly `cancelled` or `superseded`), every Task or item is terminal, every
   criterion row is `accepted` or `not-required`, and no `FAIL` row is
   unresolved. Readiness is not archive approval. Archive holds stay where
   they are recorded today, on archived units in the archive assessments;
   Stage 03 has no hold source, so readiness reads none. A package leaves
   Stage 03 for the completed archive only when this predicate held on its
   base revision; Stage 03 occupancy keeps checking only that members are
   consistent.
8. **Migration.** The Registry moves to lifecycle generation 6 and declares
   its status normalizations: Spec and Plan `in-progress`, `blocked` and
   `completed` become `approved`. A Contract Migration record in this
   package's Task binds the source revision. A terminal Task whose bytes
   equal that source keeps the reader of the generation that closed it and
   is not edited. Nonterminal generation 5 Tasks are rewritten mechanically:
   `Acceptance` becomes `Resolves`, a later `PASS` on the same Work Unit and a
   shared criterion resolves earlier `FAIL` rows, duplicate Evidence names get
   a numeric suffix, and the lowest-numbered Task carrying evidence for a
   criterion records its decision (`rejected` if any row was rejected,
   `accepted` if it had a `PASS` and accepted row and no unresolved `FAIL`,
   otherwise `pending`). Archive bodies are not edited.

## Acceptance Criteria

1. The Registry, schemas and template state contracts 1 to 5, and the
   generation 6 reader enforces them with a passing and a failing fixture for
   each rule.
2. Single-mode and multi-item Tasks reach the same completion and readiness
   judgment for equivalent work.
3. Archive readiness is computed by one predicate that gates departure from
   Stage 03, and no check requires a `completed` parent.
4. Every active Stage 03 document passes the generation 6 reader after
   migration, generation 4 historical Tasks are byte-identical, and archive
   bodies are unchanged.
5. Governance and README text states the generation 6 rules once, and the
   repeated `### Usage` heading in the Stage 01, 02 and 03 READMEs is gone.
6. The changed gate and `candidate-quality` pass.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-task-lifecycle-generation-6.md)
