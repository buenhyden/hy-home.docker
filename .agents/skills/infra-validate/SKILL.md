---
name: "infra-validate"
description: "Use when an approved infrastructure change needs scoped static checks and separately authorized runtime observations with exact evidence. Reach for it when someone asks whether a Compose or infrastructure change is valid, wants only the checks that need no running services, or asks what could not be verified without touching runtime. Do NOT use it to start, restart, or deploy services, or to read secret values; runtime action needs its own approval and this reports what it did not do."
metadata:
  title: "infra-validate"
  version: "1.4.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-09-14"
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

1. Run [`scripts/static-checks.sh`](./scripts/static-checks.sh) with no
   arguments. The only other accepted forms are `--help` and `-h`.
   The helper snapshots reviewed tracked inputs with no-follow reads into an
   invocation-owned repository-local fixture, replaces public environment keys
   with synthetic values, and validates every Compose path edge before Docker.
   It never reads a real `.env`, credential body, ignored host data or Docker
   context.
2. Read every result record. Required Git, Bash, Python/PyYAML, Docker Compose,
   YAML lint and conditional shell lint evidence is `PASS`, `FAIL` or
   `BLOCKED`; zero eligible tracked shell inputs is `NOT_APPLICABLE`.
   Runtime observation and secret access remain `NOT_RUN`. Exit 1 means an
   executed failure, exit 2 means incomplete required evidence, and exit 0
   means every applicable required check passed. Executed failure takes
   precedence over blocked evidence.
   Support tools, isolated Git initialization and owned fixture cleanup are
   required evidence and appear as their own records.
3. If explicitly approved, perform the smallest scoped runtime observation and compare it with declared invariants.
4. Record exact commands, outcomes, skips, and rollback disposition after inspecting the final diff.

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
