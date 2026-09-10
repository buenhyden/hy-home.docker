---
name: "infra-validate"
description: "Use when an approved infrastructure change needs scoped static checks and separately authorized runtime observations with exact evidence. Reach for it when someone asks whether a Compose or infrastructure change is valid, wants only the checks that need no running services, or asks what could not be verified without touching runtime. Do NOT use it to start, restart, or deploy services, or to read secret values; runtime action needs its own approval and this reports what it did not do."
metadata:
  title: "infra-validate"
  version: "1.3.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-09-10"
  function_id: "infra-validate"
  scope: "infra"
  owner_agent: "infra-implementer"
---

# infra-validate

## Preconditions

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

The approved infrastructure change and its validation contract must identify which checks are static and which runtime checks are authorized.

## Inputs

- Approved infrastructure change and validation contract.
- Expected rendered configuration, health behavior, and rollback boundary.
- The registered validators that implement the checks below, named once in
  `scripts/manifest.yaml`; which of them this change type requires is owned by
  the [verification matrix](../../governance/quality-standards.md#5-change-type-verification-matrix).
  Naming a command here instead would copy both owners into a third place.

## Procedure

1. Run `scripts/static-checks.sh`. It reports every check it ran and, just as
   importantly, names the ones it did not: an omitted line reads like a passing
   one, so runtime observation and secret access appear as `NOT_RUN` rather
   than disappearing.
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
