---
name: "requirements-to-design-agent"
description: "Use when approved requirements need traceable architecture inputs, coverage analysis, alternatives, and explicit unresolved decision gaps."
metadata:
  title: "requirements-to-design-agent"
  version: "1.1.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-09-06"
  function_id: "requirements-to-design-agent"
  scope: "architecture"
  owner_agent: "rules-engineer"
---

# requirements-to-design-agent

## Preconditions

Invoke this procedure explicitly. Invocation does not select a role or grant the
owning role's permissions. Use the already selected role's permission profile and
approved Task scope; route to the owner when incompatible.

Requirements must be approved, testable, and traceable; unresolved product choices stay upstream rather than becoming architecture assumptions.

## Inputs

- Approved requirements and architecture constraints.
- Quality attributes, current system boundaries, interfaces, and governing decisions.

## Procedure

1. Map every requirement and acceptance criterion to architecture responsibilities, interfaces, data, and quality attributes.
2. Identify design alternatives and decision points while preserving product intent and explicit non-goals.
3. Produce traceable design inputs for ARD/ADR/Spec authors and record uncovered or contradictory requirements.

## Outputs

- Traceable design input with requirement coverage, boundaries, and decision needs.

## Gates

- Every in-scope requirement has an architecture disposition.
- Architecture does not cross approved system or authority boundaries silently.

## Failure Handling

Return ambiguous or conflicting requirements to Stage 01 with concrete questions; do not invent design authority.

## Related Documents

- [Rules engineer](../../roles/rules-engineer.md)
- [ADR writing](../adr-writing/SKILL.md)
- [Architecture scope](../../governance/stage-authoring-matrix.md)
