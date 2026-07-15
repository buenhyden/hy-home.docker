---
layer: agentic
artifact_type: agent-function
function_id: code-reviewer
scope: common
status: active
---

# code-reviewer

## Preconditions

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

- [Code reviewer role](../agents/code-reviewer.md)
- [Code review dimensions](./code-review-dimensions.md)
- [Subagent protocol](../../subagent-protocol.md)
