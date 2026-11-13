---
title: "AI Agent Identity Routing"
version: "1.0.3"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# AI Agent Identity Routing

## Purpose

### Objective

Resolve a single canonical role identity before repository work.

### Authority

This policy is the canonical owner of canonical role identity resolution before repository work under [bootstrap precedence](bootstrap.md#authority-and-precedence).

## Scope

### Applies To

Canonical role selection and provider-neutral identity before repository mutation.

### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

Before mutation, resolve exactly one canonical `agent_id` from `.agents/roles/`. Use its
scope, permission profile, work profile, and skill IDs without inventing a
provider-local identity. Provider-native adapters preserve role intent but do
not own names, permissions, or model policy.

If no role matches or multiple roles conflict, stop and route the ambiguity to
`workflow-supervisor`. Multi-role work keeps one supervising owner and separates
implementation from independent review.

### Enforcement

None: this document states no separate check.

## Exceptions

### Exception Conditions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

### Approval and Review

None: no exception exists to approve.

## Ownership

### Responsibilities

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

### Change and Adoption

Changes land in place with Task evidence; related documents:

- [Bootstrap policy](bootstrap.md)
- [Agentic policy](agentic.md)
- [Roles](../roles/)
- [Provider registry](providers/registry.yaml)
