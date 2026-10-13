---
title: "Task Lifecycle Generation 6 Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0231-TSK-0001"
parent_ids:
- "SPEC-0231-PLAN-0001"
created: "2026-10-13"
---

# Task Lifecycle Generation 6 Task

## Objective

Give execution state, acceptance and archive readiness one owner each, as
SPEC-0231 states, and move the active Stage 03 corpus to that contract.

## Inputs and Authorization

On 2026-10-13 the owner asked to proceed with the Task status structure
change (prompt v9 findings F03 and F06) and chose, when asked: Spec and Plan
keep authority statuses only; acceptance moves to a per-criterion table; the
multi-item Task mode is included now. The prompt v9 request authorizes
repository source, test, document and governance changes, logical commits,
the branch push, its pull request and per-Spec integration. Baseline `main`
`2a57d4122`. Archive approval is not part of this request.

## Work Log

### Starting State

Read on `2a57d4122`:

- `docs/99.templates/registry.json` sets `lifecycle_generation` 5. The `spec`
  and `plan` lifecycles include `in-progress`, `blocked` and `completed`, and
  `_validate_execution_states` in `spec_packages.py` makes them project Task
  execution.
- `_v5_evidence_contract` reads the eight-column Evidence table and treats a
  `PASS` and `accepted` row as closing its criterion and Work Unit pair. A
  `FAIL` row with `pending` acceptance blocks nothing.
- `_validate_completion_evidence` runs only for a `completed` Spec and
  requires a `completed` Plan; `archive.validate_active_stage_occupancy`
  lets a package wait in Stage 03 only with a `completed` Spec and Plan.
- Generation 4 already had per-row item status and a per-criterion review
  table; generation 5 folded both into the Evidence row.
- The generation migration proof and `_generation_normalizations` are
  written for generations 4 and 5 only.
- Corpus: 52 Tasks (draft 23, completed 16, in-progress 10, blocked 3), 44
  of them with the eight-column table; 8 completed Tasks are generation 4
  historical bodies. Spec and Plan: draft 18, completed 4, in-progress 3,
  blocked 1 each.

### Contract Migration

| Date | Source revision | Evidence |
| --- | --- | --- |
| 2026-10-13 | 2a57d4122dc8dac954afca364b838e4bf97fd44a | #starting-state: generation 5 Registry and corpus read before the migration |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Contract | 1 | W1 | Registry, schema and template checks | Branch | NOT_RUN | Work Log | - |
| Reader | 1, 2 | W2 | Generation 6 fixtures RED then GREEN | Branch | NOT_RUN | Work Log | - |
| Readiness | 3 | W3 | Shared predicate fixtures | Branch | NOT_RUN | Work Log | - |
| Migration | 4 | W4 | Corpus reader run; byte comparison | Branch | NOT_RUN | Work Log | - |
| Text | 5 | W5 | Document checks | Branch | NOT_RUN | Work Log | - |
| Gate | 6 | W6 | Changed gate; candidate quality | Branch | NOT_RUN | Work Log | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | pending | - | - |
| 2 | pending | - | - |
| 3 | pending | - | - |
| 4 | pending | - | - |
| 5 | pending | - | - |
| 6 | pending | - | - |

## Review and Completion

No row is accepted until the owner accepts it.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
