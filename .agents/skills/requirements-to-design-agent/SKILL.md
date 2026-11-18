---
name: "requirements-to-design-agent"
description: "Use when approved requirements need traceable architecture inputs, coverage analysis, alternatives, and explicit unresolved decision gaps."
metadata:
  title: "requirements-to-design-agent"
  version: "1.3.1"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-11-18"
  function_id: "requirements-to-design-agent"
  scope: "architecture"
  owner_agent: "rules-engineer"
---

# requirements-to-design-agent

## Trigger

### When to Use

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

Requirements must be approved, testable, and traceable; unresolved product choices stay upstream rather than becoming architecture assumptions.

### When Not to Use

Unresolved product choices and ambiguous or conflicting requirements are outside this skill; they return to Stage 01.

## Procedure

### Steps

1. Map every requirement and acceptance criterion to architecture responsibilities, interfaces, data, and quality attributes.
2. Identify design alternatives and decision points while preserving product intent and explicit non-goals.
3. Produce traceable design inputs for ARD/ADR/Spec authors and record uncovered or contradictory requirements.

#### Gates

- Every in-scope requirement has an architecture disposition.
- Architecture does not cross approved system or authority boundaries silently.

#### Inputs

- Approved requirements and architecture constraints.
- Quality attributes, current system boundaries, interfaces, and governing decisions.

### Failure Handling

Return ambiguous or conflicting requirements to Stage 01 with concrete questions; do not invent design authority.

## Outputs

### Artifacts

- Traceable design input with requirement coverage, boundaries, and decision needs.

### Handoff

Owning role, policies and related documents:

- [Rules engineer](../../roles/rules-engineer.md)
- [ADR writing](../adr-writing/SKILL.md)
- [Architecture scope](../../../docs/00.workspace/01.project/stage-authoring-matrix.md)

## Verification

### Checks

- Every in-scope requirement and acceptance criterion has an architecture disposition.
- Uncovered or contradictory requirements are listed rather than dropped.
- No design input crosses an approved system or authority boundary without saying so.

### Limits

This skill records no limit on what its checks prove.
