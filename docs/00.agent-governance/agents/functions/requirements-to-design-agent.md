---
layer: agentic
artifact_type: agent-function
function_id: requirements-to-design-agent
scope: architecture
status: active
---

# requirements-to-design-agent

## Preconditions

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

- [Rules engineer](../agents/rules-engineer.md)
- [ADR writing](./adr-writing.md)
- [Architecture scope](../../scopes/architecture.md)
