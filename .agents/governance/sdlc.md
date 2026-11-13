---
title: "Software Development Lifecycle"
version: "1.9.1"
type: "governance/workflow"
status: "active"
owner: "@buenhyden"
updated: "2026-11-14"
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
5. **Operations** — Stage 05 owns guides, policies, runbooks, incidents, and
   their postmortems for the running system.

Research, design drafts, and isolated trials never require a future
approval, commit, or digest before they start. Activating a new shared norm,
switching a numbering scheme, or applying a retention policy needs the
approval for that scope first; reusing an approval follows
[approval boundaries](approval-boundaries.md#authorization-source-and-records).

Reuse approved Requirement and Architecture inputs when they already cover the
change. Within Stage 03, clarify unresolved scope before writing the Spec, map
its acceptance criteria into the Plan and Tasks, and analyze their coverage and
consistency before implementation. Verify actual results, promote durable meaning
to its Stage 01/02/05 or governance owner, then bring the package to readiness for removal
review before any separately approved retirement.
This adapts the [Spec Kit workflow](https://github.com/github/spec-kit) while
retaining this repository's separate numbered Task records.

Promotion has three owners. The Plan's Promotion Map plans it: each durable
meaning names its target owner document, the intended change and the handoff
condition. The target Stage 01, 02 or 05 document, or the governance owner,
owns the promoted content itself. The current Task's Handoff records the
Promotion Receipt: for each acceptance criterion, the Plan work unit, the
actual Task result, the target document and the commit that changed it, the
consumer update and its verification, the criterion's Criterion Acceptance
row, and any residual with its owner, or why no durable update is needed. The
commit is the one that carries the target change, not a later merge commit. A
Task that ended without a receipt gets one from the Task that removes its
package. Link existing
evidence rather than copying it into a second ledger. Failed acceptance returns
to the current Task; unresolved requirements or decisions return to their owning
stage. Retry and approval boundaries remain in agent governance policy.

The numbered steps above are SDLC phases; document Stages are folders. One
phase can write into several Stages, and a Stage folder carries no phase state.
Each state axis keeps its own record: approval of a document or change in its
lifecycle status and the approval record, execution and its blockers in the
Task, check results in Task evidence, acceptance per criterion in the Task's
Criterion Acceptance, completion in the Task status, promotion as above, Git
integration in the merge, operation in Stage 05, and retirement in the removing
Task. No axis is inferred from another: a PASS check is not acceptance, an
accepted ADR or approved Spec is not execution, and a merge is not acceptance
or deployment. These terms follow the
[glossary](../knowledge/glossary.md). Plan, README and Issue text link the
Task; they do not restate its status, results or acceptance. A pull request
reports the checks of its own candidate and links the Task for the rest.

| Event | Actor | Precondition | Changed record | Evidence |
| --- | --- | --- | --- | --- |
| Create | Author | A request, a parent or a detected event | New document at its initial Registry status | The request, parent or event link |
| Review | Reviewer | A complete draft | Review record; the family's review status where registered | Review findings with revision |
| Approve | The approver the [approval boundaries](approval-boundaries.md) name | Any required review passed | Lifecycle status and approval record | The approval source |
| Start | Task writer | Spec and Plan `approved` | Task or item status | Lifecycle Event with same-Task anchor |
| Block | Task writer | A blocker, or a parent no longer `approved` | Task or item status, Blocker | Lifecycle Event with same-Task anchor |
| Verify | Task writer | Executed work | Evidence row | Check, Input, Result, Location |
| Accept | Owner of the criterion | Required evidence PASS, none unresolved | Criterion Acceptance row | The cited PASS rows |
| Promote | Target owner, then Task writer | PASS evidence for the target change | Target document; Promotion Receipt | Target commit and consumer check |
| Complete | Task writer | Every assigned pair PASS or not-required; each criterion it decides accepted or not-required | Task or item status `completed` | Lifecycle Event |
| Cancel | The document's writer with authorization | An authorization record | Status and, where registered, `cancellation` frontmatter; an item's Blocker | `authorization_ref`, successor or `withdrawal_ref` |
| Retire | Removing Task with approval, or the owner of a Stage 05 or governance document | Readiness and retirement preconditions, or a successor owner | Package removed and number reserved, or `retired` status | The removing Task's record or the retirement record |

The Registry `transitions` own the legal edges; this table names who moves an
edge and what proves it. A transition outside the Registry edges, an approval
without its source, and a second completion of a terminal Task or item are
invalid.

Stage 99 assigns document-family states and legal transitions in the
Registry `lifecycles` and `transitions`; this policy does not restate them.
Specs and Plans record authority only. Stage 01 to 03 documents never use
`deprecated`, `superseded`, `retired`, or `archived`: a replaced or withdrawn
document is summarized into its current owner and deleted, and its number is
reserved.

A Plan has one Spec parent and a Task has one Plan parent. A Plan is never
ahead of its Spec and never ends before it. A Task, and each of its items,
runs only while both are `approved`; under a `draft` or `in-review` parent a
remaining Task or item stays `draft` or `blocked`. A `cancelled` Spec requires
a terminal Plan and terminal Tasks. Parent status
never reflects execution.

Execution state has one owner. A single-mode Task keeps one frontmatter
`status`. A multi-item Task has an `Execution Items` table under Work Performed
in its Execution Log with at least two rows, owns one status per row, assigns
each Work Unit to one item, and declares no frontmatter `status`; its summary is
derived on read. A cancelled item leaves its criterion/Work Unit pairs open
until a PASS in a current item or Task or a `not-required` decision closes
them.

Evidence rows record observations only: criterion, Work Unit, Check, Input,
Result, Location, Required, and Resolves. Required is either `required` or
`optional`. A required non-PASS observation remains open until a later PASS
row in the same Task explicitly resolves it for a shared criterion with the
same Check and Work Unit. An optional observation does not itself block
acceptance. Input names the revision or candidate examined and, where they
affect the result, the environment and tool version. Check names what was
proved: a document or contract check and a checker's own regression test are
different Checks. A PASS on another revision supports acceptance only when that
PASS row records why the same input and guarantee hold.

Acceptance has one owner per criterion. A criterion the Plan assigns to at
least one current, non-cancelled Task has exactly one Criterion Acceptance row
in one such Task. Current Owner records a durable owner or an evidence-backed
N/A disposition. A criterion whose assigned Tasks are all historical or
cancelled has no acceptance row. One whose historical Tasks record it as PASS
or accepted counts as described for older Task formats below. Any other, such
as one held only by cancelled Tasks, stays open while the Spec holds it, until
the Plan assigns it to a current Task that decides it or the Spec drops it, as
the [retirement preconditions](documentation-protocol.md#retirement-preconditions)
require. Decisions are `pending`, `accepted`, `rejected`, or `not-required`. An
accepted criterion requires PASS evidence and no unresolved required
observation. A decision recorded under this policy's 1.9.0 or later also needs
a PASS for every criterion/Work Unit pair the Plan assigns to a current,
non-cancelled Task, cites at least one PASS row for that criterion, and cites a
non-PASS row only when a later row resolves it; earlier decisions stand as
recorded. Rejected and not-required decisions state their rationale; only
`not-required` closes a criterion without PASS.

A completed Task or item has PASS evidence for every criterion/Work Unit pair
assigned to it unless that criterion is not-required. Each criterion the Task
decides for that work is also accepted or not-required. The current Task
Result vocabulary is the Registry's `PASS`, `FAIL`, `ERROR`, `NOT_RUN`,
`CANCELLED`, and `NOT_APPLICABLE`. Lifecycle Events and generation-migration
proof rows record observed structure only; they do not authenticate approval,
review, or execution.

A package is ready for removal review when its Spec and Plan are `approved`
(or validly `cancelled`), every Task or item is terminal, every
criterion is accepted or `not-required`, each target document the Promotion
Map names appears in a Promotion Receipt or has a stated reason no update is
needed, and no required non-PASS observation is unresolved;
an older Task format that predates the typed Criterion Acceptance table counts
when it records every criterion as PASS or accepted and leaves no required
non-PASS observation unresolved.
Readiness is derived on read, is never stored, and is not removal approval.
A ready package with an approved Spec may wait in Stage 03 until its removal is
approved; a user instruction to delete completed packages approves that batch,
and the deleting Task records the approval and each package's criterion state.
A cancelled Spec keeps no member there. A package leaves Stage 03 only under
the [retirement preconditions](documentation-protocol.md#retirement-preconditions);
version history keeps its body.

The Registry supplies the exact Evidence, Criterion Acceptance, Execution
Items and Work Breakdown shapes, and its `common.section_forms` places each
named section in the common form, for example Evidence under Verification
Evidence as Results. `spec_packages.py` checks their structure, reads those
places from the Registry and derives readiness. The corpus lifecycle check
applies the 1.9.0 acceptance rules, including cancelled-item pairs, to each
Criterion Acceptance row that is new or changed against the lifecycle base;
an unchanged older row stands as recorded. The readiness derivation also
requires every repository path a Plan's Promotion Map names in a code span to
appear in a Task's Promotion Receipt, but no entrypoint runs the readiness
derivation yet, so readiness and every Promotion Map target named only in
prose stay with review, and a validator PASS does not show them.
A terminal Task unchanged since the current generation's migration source keeps
the reader of the generation that closed it, bound by that migration's exact
Git source proof. That compatibility does not authorize new legacy receipts. A
Task event records only an observed direct registered transition with
same-Task evidence. Structural event validation does not authenticate
approval; current authorization remains manual under the approval boundary.

Stage 90 supplies evidence and version history supplies removed bodies; neither
overrides current lifecycle authority. Stage 99 defines document shapes and
identities. Registered scripts implement gates. `FAIL`, `ERROR`, `NOT_RUN`, `CANCELLED`,
and `NOT_APPLICABLE` remain valid non-completion observations; they do not
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
