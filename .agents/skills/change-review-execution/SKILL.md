---
name: "change-review-execution"
description: "Use when an exact diff or commit range needs independent specification-compliance and quality verdicts backed by verification evidence."
metadata:
  title: "change-review-execution"
  version: "1.3.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-11-17"
  function_id: "change-review-execution"
  scope: "common"
  owner_agent: "code-reviewer"
---

# change-review-execution

## Trigger

### When to Use

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

The review package must identify the base/head range, task requirements, and observed verification evidence.

### When Not to Use

Editing the implementation under review is outside this skill; the reviewer never edits it.

## Procedure

### Steps

1. Confirm the reviewed range and read the task requirements before inspecting implementation details.
2. Test each candidate finding against repository evidence, then classify it with a precise remediation condition.
3. Issue separate specification-compliance and quality verdicts and identify any forward dependency that cannot be verified in this task.

#### Gates

- Review remains read-only and independent.
- No claim is made without reproducible evidence.

#### Inputs

- Exact diff and commit list.
- Verification evidence, task report, and governing constraints.

### Failure Handling

Return `cannot verify` with the missing evidence when the package is incomplete; never edit the implementation while acting as reviewer.

## Outputs

### Artifacts

- Actionable findings and explicit PASS/APPROVED or correction-required verdicts.

### Handoff

Owning role, policies and related documents:

- [Code reviewer role](../../roles/code-reviewer.md)
- [Code review dimensions](../code-review-dimensions/SKILL.md)
- [Subagent protocol](../../governance/agentic.md)

## Verification

### Checks

- The review cites the exact reviewed range and leaves the working tree unchanged.
- Each finding names a file and line that reproduces it, or it is dropped.
- The specification-compliance verdict and the quality verdict are recorded separately.

### Limits

This skill records no limit on what its checks prove.
