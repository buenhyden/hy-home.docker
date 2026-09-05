---
name: "infra-validate"
description: "Use when an approved infrastructure change needs scoped static checks and separately authorized runtime observations with exact evidence."
metadata:
  title: "infra-validate"
  version: "1.1.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-09-06"
  function_id: "infra-validate"
  scope: "infra"
  owner_agent: "infra-implementer"
---

# infra-validate

## Preconditions

Invoke this procedure explicitly. Invocation does not select a role or grant the
owning role's permissions. Use the already selected role's permission profile and
approved Task scope; route to the owner when incompatible.

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

- [Infrastructure implementer](../../roles/infra-implementer.md)
- [Compose stack function](../compose-stack-agent/SKILL.md)
- [Infrastructure scope](../../governance/environment-constraints.md)
