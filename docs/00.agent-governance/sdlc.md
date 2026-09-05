---
title: "Software Development Lifecycle"
version: "1.1.0"
type: "governance/sdlc"
status: "active"
owner: "@buenhyden"
updated: "2026-09-05"
---

# Software Development Lifecycle

## Purpose

Provide one lifecycle for human and agent work without duplicating document
shape rules or executable gates.

## Lifecycle

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

The current Task's `Verification Evidence` owns the promotion receipt: connect
each acceptance criterion to its Plan work unit, actual Task result, and durable
target document, or record why no durable update is needed. Link existing
evidence rather than copying it into a second ledger. Failed acceptance returns
to the current Task; unresolved requirements or decisions return to their owning
stage. Retry and approval boundaries remain in Stage 00 policy.

Stage 90 supplies evidence and Stage 98 supplies historical path lookup; neither
overrides current lifecycle authority. Stage 99 defines document shapes and
identities. Registered scripts implement gates.

## Authority Boundaries

Every transition requires the smallest applicable validation set, exact Task
evidence, independent review for material changes, and logical Conventional
Commits when committing is authorized. A local-only request may finish with a
reviewed working-tree diff; it does not authorize commit, push, PR, release, or
runtime action. Document lifecycle states do not grant those permissions.
Approval boundaries are defined in
[approval-boundaries.md](policies/approval-boundaries.md).

Trace durable requirement IDs through Architecture and Spec packages. Record
implementation and verification against the current Task rather than a parallel
progress or handoff document.

## Related Documents

- [Governance hub](README.md)
- [Approval boundaries](policies/approval-boundaries.md)
- [Documentation protocol](policies/documentation-protocol.md)
- [Stage 99 registry](../99.templates/registry.json)
