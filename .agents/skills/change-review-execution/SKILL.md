---
name: "change-review-execution"
description: "Use when an exact diff or commit range needs independent specification-compliance and quality verdicts backed by verification evidence."
metadata:
  title: "change-review-execution"
  version: "1.2.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-10-29"
  function_id: "change-review-execution"
  scope: "common"
  owner_agent: "code-reviewer"
---

# change-review-execution

## Purpose

### Preconditions

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

The review package must identify the base/head range, task requirements, and observed verification evidence.

## Inputs

- Exact diff and commit list.
- Verification evidence, task report, and governing constraints.

## Procedure

1. Confirm the reviewed range and read the task requirements before inspecting implementation details.
2. Test each candidate finding against repository evidence, then classify it with a precise remediation condition.
3. Issue separate specification-compliance and quality verdicts and identify any forward dependency that cannot be verified in this task.

### Gates

- Review remains read-only and independent.
- No claim is made without reproducible evidence.

## Outputs

- Actionable findings and explicit PASS/APPROVED or correction-required verdicts.

## Verification

- The review cites the exact reviewed range and leaves the working tree unchanged.
- Each finding names a file and line that reproduces it, or it is dropped.
- The specification-compliance verdict and the quality verdict are recorded separately.

## Failure Handling

Return `cannot verify` with the missing evidence when the package is incomplete; never edit the implementation while acting as reviewer.

## References

- [Code reviewer role](../../roles/code-reviewer.md)
- [Code review dimensions](../code-review-dimensions/SKILL.md)
- [Subagent protocol](../../governance/agentic.md)
