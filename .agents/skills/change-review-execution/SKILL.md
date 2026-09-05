---
name: "change-review-execution"
description: "Use when an exact diff or commit range needs independent specification-compliance and quality verdicts backed by verification evidence."
metadata:
  title: "change-review-execution"
  version: "1.1.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-09-06"
  function_id: "change-review-execution"
  scope: "common"
  owner_agent: "code-reviewer"
---

# change-review-execution

## Preconditions

Invoke this procedure explicitly. Invocation does not select a role or grant the
owning role's permissions. Use the already selected role's permission profile and
approved Task scope; route to the owner when incompatible.

The review package must identify the base/head range, task requirements, and observed verification evidence.

## Inputs

- Exact diff and commit list.
- Verification evidence, task report, and governing constraints.

## Procedure

1. Confirm the reviewed range and read the task requirements before inspecting implementation details.
2. Test each candidate finding against repository evidence, then classify it with a precise remediation condition.
3. Issue separate specification-compliance and quality verdicts and identify any forward dependency that cannot be verified in this task.

## Outputs

- Actionable findings and explicit PASS/APPROVED or correction-required verdicts.

## Gates

- Review remains read-only and independent.
- No claim is made without reproducible evidence.

## Failure Handling

Return `cannot verify` with the missing evidence when the package is incomplete; never edit the implementation while acting as reviewer.

## Related Documents

- [Code reviewer role](../../roles/code-reviewer.md)
- [Code review dimensions](../code-review-dimensions/SKILL.md)
- [Subagent protocol](../../governance/agentic.md)
