---
title: "Postflight Routing"
version: "1.1.2"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# Postflight Routing

## Purpose

### Objective

Route completion verification to the actual changed authority surface.

### Authority

- [Task checklists](task-checklists.md)
- [Quality standards](quality-standards.md#4-execution-boundary)

## Scope

### Applies To

Completion verification selected for the changed canonical and protected surfaces.

### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

Completion evidence belongs in the co-located Stage 03 Task. Git history is the
recovery boundary. Do not create a second handoff or progress authority.

For an approved all-files gate, the
[execution boundary](quality-standards.md#4-execution-boundary) owns direct
pre-commit prohibition and every wrapper condition. Postflight records only
the concise result and hook-managed fallout; the controlled wrapper reports
exit 20 for unexpected paths.

### Enforcement

`task-checklists.md` is the completion authority. Apply only validators mapped
to the changed canonical source and protected surface. For provider projections,
run the agent governance contract and renderer check; write mode is used only through
the registered renderer.

## Exceptions

### Exception Conditions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

### Approval and Review

The [approval boundaries](approval-boundaries.md) policy governs a separately authorized operation.

## Ownership

### Responsibilities

This policy is owned by `@buenhyden`.

### Change and Adoption

Related documents:

- [Documentation protocol](documentation-protocol.md)
- [Provider registry](providers/registry.yaml)
