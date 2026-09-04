---
title: "code-review-dimensions"
version: "1.0.0"
type: "governance/skill"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
function_id: "code-review-dimensions"
scope: "common"
owner_agent: "code-reviewer"
---

# code-review-dimensions

## Preconditions

An exact diff and governing specification must be available; review scope and non-goals must be explicit.

## Inputs

- Exact diff or commit range.
- Governing specification, risk boundaries, and implementation evidence.

## Procedure

1. Evaluate correctness, security, maintainability, performance, and governance only where the diff and specification make each dimension relevant.
2. Reproduce candidate defects against tracked code or tests and cite the narrowest useful file-and-line location.
3. Calibrate Critical, Important, and Minor severity from impact, reachability, and remediation urgency.

## Outputs

- A dimensioned review with evidence-backed findings and a bounded verdict.

## Gates

- Every finding has a concrete evidence citation.
- Severity is calibrated and does not inflate style preferences into blockers.

## Failure Handling

Mark unverifiable requirements explicitly and request the missing artifact; do not infer either pass or failure.

## Related Documents

- [Code reviewer](../roles/code-reviewer.md)
- [Change review execution](change-review-execution.md)
- [Common scope](../policies/quality-standards.md)
