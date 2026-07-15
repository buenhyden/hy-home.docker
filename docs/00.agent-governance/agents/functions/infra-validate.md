---
layer: agentic
artifact_type: agent-function
function_id: infra-validate
scope: infra
status: active
---

# infra-validate

## Preconditions

The approved infrastructure change and its validation contract must identify which checks are static and which runtime checks are authorized.

## Inputs

- Approved infrastructure change and validation contract.
- Expected rendered configuration, health behavior, and rollback boundary.

## Procedure

1. Run syntax, schema, Compose rendering, referenced-path, and secret-boundary checks on the exact change.
2. If explicitly approved, perform the smallest scoped runtime observation and compare it with declared invariants.
3. Record exact commands, outcomes, skips, and rollback disposition after inspecting the final diff.

## Outputs

- Infrastructure validation evidence separated into static, runtime-observed, CI-only, and skipped results.

## Gates

- Static validation passes before any runtime action.
- Runtime checks remain within approved service and mutation scope.

## Failure Handling

Stop on invalid rendered configuration, missing authority, or unexpected runtime impact; revert or escalate according to the approved task.

## Related Documents

- [Infrastructure implementer](../agents/infra-implementer.md)
- [Compose stack function](./compose-stack-agent.md)
- [Infrastructure scope](../../scopes/infra.md)
