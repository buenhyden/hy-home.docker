---
title: "Software Development Lifecycle"
version: "1.4.1"
type: "governance/workflow"
status: "active"
owner: "@buenhyden"
updated: "2026-10-13"
---

# Software Development Lifecycle

## Purpose

Provide one lifecycle for human and agent work without duplicating document
shape rules or executable gates.

## Inputs

An approved change uses its governing Requirements and Architecture, the active
Spec Package, the current Task, and the registered Stage 99 contract.

## Sequence

1. **Requirements** — Stage 01 owns durable, solution-independent needs and
   acceptance criteria.
2. **Architecture** — Stage 02 owns current system structure and consequential,
   long-lived decisions.
3. **Specification** — Stage 03 owns an implementable behavior contract,
   technical approach, plan, tasks, and executable interface contracts.
4. **Implementation** — code and configuration changes are executed from the
   approved Spec Package and recorded in its current Task.
5. **Operations** — Stage 05 owns guides, policies, runbooks, and incidents for
   the running system.

Reuse approved Requirement and Architecture inputs when they already cover the
change. Within Stage 03, clarify unresolved scope before writing the Spec, map
its acceptance criteria into the Plan and Tasks, and analyze their coverage and
consistency before implementation. Verify actual results, promote durable meaning
to its Stage 01/02/05 owner, then bring the package to readiness for archive
review before any separately approved preservation.
This adapts the [Spec Kit workflow](https://github.com/github/spec-kit) while
retaining this repository's separate numbered Task records.

The current Task's `Evidence` owns the promotion receipt: connect
each acceptance criterion to its Plan work unit, actual Task result, and durable
target document, or record why no durable update is needed. Link existing
evidence rather than copying it into a second ledger. Failed acceptance returns
to the current Task; unresolved requirements or decisions return to their owning
stage. Retry and approval boundaries remain in agent governance policy.

Stage 99 assigns document-family states and legal transitions. Requirements use
`draft`, `in-review`, `approved`, `superseded`, and `retired`; architecture
descriptions and operational guidance use `draft`, `in-review`, `active`,
`deprecated`, `superseded`, and `retired`; ADRs use `proposed`, `accepted`,
`rejected`, `superseded`, and `retired`. Specs and Plans record authority
only: `draft`, `in-review`, `approved`, `cancelled`, and `superseded`. Tasks
retain `draft`, `ready`, `in-progress`, `blocked`, `completed`, and
`cancelled`. Navigation READMEs and the current archive
catalog remain `active`; route records use `draft` or `sealed`.

A Plan has one Spec parent and a Task has one Plan parent. A Plan is never
ahead of its Spec and never ends before it. A Task, and each of its items,
runs only while both are `approved`; under a `draft` or `in-review` parent a
remaining Task or item stays `draft` or `blocked`. A `cancelled` or
`superseded` Spec requires a terminal Plan and terminal Tasks. Parent status
never reflects execution.

Execution state has one owner. A single-mode Task keeps one frontmatter
`status`. A multi-item Task has an `Execution Items` table under its Work Log
with at least two rows, owns one status per row, assigns each Work Unit to one
item, and declares no frontmatter `status`; its summary is derived on read.

Evidence rows record observations only: criterion, Work Unit, check, input,
result, location, and `Resolves`, which names earlier `FAIL` rows of the same
Task that a `PASS` row for a shared criterion resolves. Acceptance has one
owner per criterion: exactly one `Criterion Acceptance` row, in one current
Task the Plan assigns it to, holds `pending`, `accepted`, `rejected`, or
`not-required`.
`accepted` requires `PASS` evidence for the criterion and no unresolved `FAIL`;
`rejected` and `not-required` state their decision; only `not-required` closes
a criterion without `PASS`. A completed Task, or completed item, has `PASS`
evidence for every criterion and Work Unit pair assigned to it unless that
criterion is `not-required`, and every criterion that Task decides for that
work is accepted or `not-required`. Task-result vocabulary is exactly `NOT_RUN`, `PASS`, `FAIL`,
`DEFER`, and `NOT_APPLICABLE`. Lifecycle events and generation-migration proof
rows record observed structure only; they do not authenticate approval,
review, or execution.

A package is ready for archive review when its Spec and Plan are `approved`
(or validly `cancelled` or `superseded`), every Task or item is terminal, every
criterion is accepted or `not-required`, and no `FAIL` is unresolved.
Readiness is derived on read, is never stored, and is not archive approval; a
package enters the completed archive only from a ready base revision, whatever
its status there.

The Registry supplies the exact Evidence, Criterion Acceptance, Execution
Items and Work Breakdown shapes. `spec_packages.py` implements their meaning.
A terminal Task unchanged since the current generation's migration source keeps
the reader of the generation that closed it, bound by that migration's exact
Git source proof. That compatibility does not authorize new legacy receipts. A
Task event records only an observed direct registered transition with
same-Task evidence. Structural event validation does not authenticate
approval; current authorization remains manual under the approval boundary.

Stage 90 supplies evidence and Stage 98 supplies historical path lookup; neither
overrides current lifecycle authority. Stage 99 defines document shapes and
identities. Registered scripts implement gates. FAIL, NOT_RUN, DEFER, and
NOT_APPLICABLE results remain valid non-completion evidence; they do not
satisfy acceptance. Stage 99 and its validator own the machine shapes, so
templates refer here for completion meaning.

## Stop Conditions

Every transition requires the smallest applicable validation set, exact Task
evidence, independent review for material changes, and logical Conventional
Commits when committing is authorized. A local-only request may finish with a
reviewed working-tree diff; it does not authorize commit, push, PR, release, or
runtime action. Document lifecycle states do not grant those permissions.
Approval boundaries are defined in
[approval-boundaries.md](approval-boundaries.md).

Trace durable requirement IDs through Architecture and Spec packages. Record
implementation and verification against the current Task rather than a parallel
progress or handoff document.

## Outputs

The current Task records execution evidence, and the durable Requirement,
Architecture, Operations, or governance owner receives any lasting meaning.

## Related Documents

- [Governance hub](../README.md)
- [Approval boundaries](approval-boundaries.md)
- [Documentation protocol](documentation-protocol.md)
- Stage 99 registry (`docs/99.templates/registry.json`)
- [Documentation index](../../docs/README.md)
