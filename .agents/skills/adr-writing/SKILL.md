---
name: "adr-writing"
description: "Use when an approved material architecture choice needs one ADR with alternatives, consequences, and traceable decision status."
metadata:
  title: "adr-writing"
  version: "1.2.1"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-11-13"
  function_id: "adr-writing"
  scope: "architecture"
  owner_agent: "doc-writer"
---

# adr-writing

## Purpose and Trigger

### When to Use

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

Use only when a material architecture choice has approved context, explicit drivers, and at least one viable alternative.

### When Not to Use

None: this skill states no exclusion.

## Procedure

### Steps

1. Frame one decision, its status, scope, and traceable drivers without mixing implementation evidence into the record.
2. Compare credible alternatives against the named quality attributes and document consequences, risks, and reversibility.
3. Link the selected outcome to its parent ARD/PRD and the downstream Spec or superseded ADR.

#### Gates

- Architecture traceability resolves upstream and downstream links.
- Decision status and supersession semantics match the metadata contract.

### Failure Handling

If the choice, authority, or alternatives are not decision-ready, return a decision-gap report instead of fabricating an accepted ADR.

## Inputs and Outputs

### Inputs

- Approved architecture context and decision drivers.
- Alternatives, quality attributes, constraints, and affected parent artifacts.

### Outputs

- One typed ADR in `docs/02.architecture/decisions/` with decision rationale and consequences.

## Verification

### Checks

- `scripts/validation/check-document-metadata.py --mode check-changed` reports no violation for the new ADR.
- `scripts/validation/check-document-links.py --mode alignment` resolves its upstream and downstream links.
- The ADR names at least two alternatives and states its consequences and reversibility.

### Completion and Handoff

Owning role and policies:

- [Documentation protocol](../../governance/documentation-protocol.md)
- [Documentation scope](../../governance/documentation-protocol.md)
- [Agent catalog](../../README.md)
