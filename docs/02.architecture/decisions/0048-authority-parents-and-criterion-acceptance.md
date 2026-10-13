---
title: "Authority Parents and Criterion Acceptance"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "architecture"
artifact_id: "ADR-0048"
parent_ids:
- "AD-0030"
created: "2026-10-13"
---

# ADR-0048: Authority Parents and Criterion Acceptance

## Context

Lifecycle generation 5 records execution state twice: a Task's frontmatter
`status`, and Spec and Plan statuses that must project it as `in-progress`,
`blocked` or `completed`. ADR-0037 decisions 1 to 3 make a `completed` Spec and
Plan the condition for a package to wait in Stage 03 and check completion
receipts built from per-row acceptance. On `main` `2a57d4122` the Evidence
column held 275 `accepted` and 275 `pending` rows, and a `FAIL` row with
`pending` acceptance blocked nothing. The prompt v9 request (findings F03 and
F06) asks for one owner for execution state, acceptance and readiness.

### Decision Drivers

One writer per fact; no status copied between documents. Acceptance decided
once per criterion. Readiness computed, never stored. Frozen records keep the
meaning of the generation that wrote them.

## Decision

1. Spec and Plan statuses record authority only: `draft`, `in-review`,
   `approved`, `cancelled`, `superseded`. A Plan is never ahead of its Spec,
   and a Task or item runs only under an approved Spec and Plan.
2. A Task owns execution state: one frontmatter `status`, or, in a multi-item
   Task, one status per Execution Items row and no frontmatter `status`.
3. Evidence rows record observations and which earlier `FAIL` rows a `PASS`
   resolves. One Criterion Acceptance row per criterion records `pending`,
   `accepted`, `rejected` or `not-required`; `accepted` needs `PASS` evidence
   and no unresolved `FAIL`.
4. A package is ready for archive review when its parents are `approved` (or
   validly `cancelled` or `superseded`), every Task or item is terminal, every
   criterion is accepted or `not-required`, and no `FAIL` is unresolved. It may
   wait in Stage 03 then and leaves only from a ready base revision. Readiness
   is derived and is not disposition approval.

These replace ADR-0037 decisions 1 to 3. ADR-0037 decisions 4 onward, on
assessments, history-only availability and capture identity, are unchanged.

## Alternatives

### Options Considered

- Keep projected parent statuses and only relax the waiting rule: rejected;
  the duplicate execution state stays.
- Keep per-row acceptance and add an unresolved-`FAIL` check: rejected; a
  criterion would still carry several independent decisions.
- Defer the multi-item mode: rejected by the owner on 2026-10-13.

## Consequences

Lifecycle generation 6 adds a Registry migration and a Git-bound proof. Active
Tasks were rewritten mechanically; terminal Tasks unchanged since the source
revision keep their generation's reader. A branch still writing generation 5
Evidence must take the same rewrite. REQ-0026-FR-0009 and AD-0030 state the
new waiting rule.

### Compliance

SPEC-0231 proves each rule with passing and failing fixtures, loads every
active package under generation 6, and keeps generation 4 and 5 terminal Tasks
byte-identical.

### Follow-up

Accepted on 2026-10-13 by the owner's choice of these options. SPEC-0231
implements and verifies it.

## Related Documents

- [AD-0030](../descriptions/0030-document-lifecycle-governance.md)
- [ADR-0037](0037-package-disposition-wait-and-task-cancellation.md)
- [SPEC-0231](../../03.specs/0231-task-lifecycle-generation-6/spec.md)
