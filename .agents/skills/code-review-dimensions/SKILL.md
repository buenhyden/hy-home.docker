---
name: "code-review-dimensions"
description: "Use when a scoped diff needs evidence-backed correctness, security, maintainability, performance, and governance review with calibrated severity."
metadata:
  title: "code-review-dimensions"
  version: "1.3.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-11-17"
  function_id: "code-review-dimensions"
  scope: "common"
  owner_agent: "code-reviewer"
---

# code-review-dimensions

## Trigger

### When to Use

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

An exact diff and governing specification must be available; review scope and non-goals must be explicit.

### When Not to Use

None: this skill states no exclusion.

## Procedure

### Steps

1. Evaluate correctness, security, maintainability, performance, and governance only where the diff and specification make each dimension relevant.
2. Reproduce candidate defects against tracked code or tests and cite the narrowest useful file-and-line location.
3. Calibrate Critical, Important, and Minor severity from impact, reachability, and remediation urgency.

#### Gates

- Every finding has a concrete evidence citation.
- Severity is calibrated and does not inflate style preferences into blockers.

#### Inputs

- Exact diff or commit range.
- Governing specification, risk boundaries, and implementation evidence.

### Failure Handling

Mark unverifiable requirements explicitly and request the missing artifact; do not infer either pass or failure.

## Outputs

### Artifacts

- A dimensioned review with evidence-backed findings and a bounded verdict.

### Handoff

Owning role, policies and related documents:

- [Code reviewer](../../roles/code-reviewer.md)
- [Change review execution](../change-review-execution/SKILL.md)
- [Common scope](../../governance/quality-standards.md)

## Verification

### Checks

- Every finding cites a file and line and carries one calibrated severity.
- A dimension the diff does not touch is stated as not assessed rather than passed.
- The verdict is bounded to the reviewed diff and specification.

### Limits

The verdict covers only the reviewed diff and specification; a dimension
the diff does not touch is not assessed.
