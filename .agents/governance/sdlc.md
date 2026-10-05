---
title: "Software Development Lifecycle"
version: "1.3.0"
type: "governance/workflow"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
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
to its Stage 01/02/05 owner, then complete and preserve the execution package.
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
`rejected`, `superseded`, and `retired`. Specs and Plans use `draft`,
`in-review`, `approved`, `in-progress`, `blocked`, `completed`, `cancelled`,
and `superseded`; Tasks retain `draft`, `ready`, `in-progress`, `blocked`,
`completed`, and `cancelled`. Navigation READMEs and the current archive
catalog remain `active`; route records use `draft` or `sealed`.

A Plan has one Spec parent and a Task has one Plan parent. Task frontmatter is
the only execution-status source, including Tasks with multiple evidence rows.
Each row identifies the existing criterion and Plan work unit; it carries a
result and acceptance, never another status or item identity. Over nonterminal Task
summaries, any in-progress summary makes the Spec and Plan in-progress; a
nonempty set of all blocked summaries makes both blocked. A mixed ready/blocked
set, or a zero/terminal-only set, retains the actual contract status and never
auto-closes it. An evidence row can record `PASS` while acceptance
remains pending in a blocked or otherwise nonterminal Task. At Task
and Spec closure, every numbered criterion requires `PASS` and accepted
evidence; `not-required` does not waive that requirement. Task-result vocabulary
is exactly `NOT_RUN`, `PASS`, `FAIL`, `DEFER`, and `NOT_APPLICABLE`. Lifecycle
events and generation-migration proof rows record observed structure only; they
do not authenticate approval, review, or execution.

The Registry supplies the exact eight-column Evidence and six-column Work
Breakdown shapes. `spec_packages.py` implements their coverage and completion
meaning. Frozen or already-terminal Task bodies retain their source-generation
reader, bound by the current migration's exact Git source proof. That
compatibility does not authorize new legacy receipts. A Task event records only an observed
direct registered transition with same-Task evidence. Structural event
validation does not authenticate approval; current authorization remains manual
under the approval boundary.

Stage 90 supplies evidence and Stage 98 supplies historical path lookup; neither
overrides current lifecycle authority. Stage 99 defines document shapes and
identities. Registered scripts implement gates. Terminal package completion requires observed
PASS evidence for every numbered acceptance criterion and its Plan work unit.
FAIL, NOT_RUN, DEFER, and NOT_APPLICABLE results remain valid non-completion
evidence; they do not satisfy terminal acceptance. Stage 99 and its validator own the
receipt's machine shape, so templates refer here for completion meaning.
Spec and Plan closure require their registered terminal conditions; Task
completion evidence alone does not close a package with nonterminal members.

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
