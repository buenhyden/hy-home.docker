---
title: "Software Development Lifecycle"
version: "1.0.0"
type: "governance/sdlc"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
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

Stage 90 supplies evidence and Stage 98 supplies historical path lookup; neither
overrides current lifecycle authority. Stage 99 defines document shapes and
identities. Registered scripts implement gates.

## Authority Boundaries

Every transition requires the smallest applicable validation set, exact Task
evidence, independent review for material changes, and logical Conventional
Commits. Approval boundaries are defined in
[approval-boundaries.md](policies/approval-boundaries.md).

Trace durable requirement IDs through Architecture and Spec packages. Record
implementation and verification against the current Task rather than a parallel
progress or handoff document.

## Related Documents

- [Governance hub](README.md)
- [Approval boundaries](policies/approval-boundaries.md)
- [Documentation protocol](policies/documentation-protocol.md)
- [Stage 99 registry](../99.templates/registry.json)
