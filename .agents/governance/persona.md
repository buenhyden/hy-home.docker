---
title: "AI Agent Identity Routing"
version: "1.1.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
---

# AI Agent Identity Routing

## Purpose and Scope

### Objective

Resolve a single canonical role identity before repository work.

#### Authority

This policy is the canonical owner of canonical role identity resolution before repository work under [bootstrap precedence](bootstrap.md#authority-and-precedence).

### Applies To

Canonical role selection and provider-neutral identity before repository mutation.

#### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| PERSONA-R1 | Before repository mutation | Required: resolve exactly one canonical `agent_id` from `.agents/roles/` | none | none |
| PERSONA-R2 | Before repository mutation | Required: use the resolved role's scope, permission profile, work profile and skill IDs | none | none |
| PERSONA-R3 | Before repository mutation | Forbidden: inventing a provider-local identity | none | none |
| PERSONA-R4 | Always | Required: provider-native adapters preserve role intent | none | none |
| PERSONA-R5 | Always | Forbidden: provider-native adapters owning names, permissions or model policy | none | none |
| PERSONA-R6 | No role matches or multiple roles conflict | Required: stop and route the ambiguity to `workflow-supervisor` | none | none |
| PERSONA-R7 | Multi-role work | Required: keep one supervising owner | none | none |
| PERSONA-R8 | High-risk multi-role work | Required: separate implementation from independent review | none | none |

Before mutation, resolve exactly one canonical `agent_id` from `.agents/roles/`. Use its
scope, permission profile, work profile, and skill IDs without inventing a
provider-local identity. Provider-native adapters preserve role intent but do
not own names, permissions, or model policy.

If no role matches or multiple roles conflict, stop and route the ambiguity to
`workflow-supervisor`. Multi-role work keeps one supervising owner and, for
high-risk work, separates implementation from independent review.

### Exceptions

#### Exception Conditions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

#### Approval and Review

None: no exception exists to approve.

## Enforcement

### Mechanisms

None: this document states no separate check.

### Limits

This policy states no separate check, so none of its rules is mechanically enforced:

- Role identity and adapter limits: R1-R5.
- Ambiguity routing: R6.
- Multi-role ownership and review separation: R7-R8.

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- [Bootstrap policy](bootstrap.md)
- [Agentic policy](agentic.md)
- [Roles](../roles/)
- [Provider registry](providers/registry.yaml)
