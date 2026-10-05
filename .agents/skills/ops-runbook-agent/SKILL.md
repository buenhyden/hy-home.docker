---
name: "ops-runbook-agent"
description: "Use when implemented and verified operational behavior needs an executable runbook with expected signals, recovery, and escalation."
metadata:
  title: "ops-runbook-agent"
  version: "1.2.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-10-05"
  function_id: "ops-runbook-agent"
  scope: "ops"
  owner_agent: "doc-writer"
---

# ops-runbook-agent

## Purpose

### Preconditions

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

Operational behavior must be implemented and verified; commands, expected outcomes, rollback, and escalation owners must be known.

## Inputs

- Implemented operational behavior and verification commands.
- Preconditions, safety controls, rollback/recovery steps, and escalation boundary.

## Procedure

1. Define when the runbook applies, required access, safety checks, and the exact starting state.
2. For stateful recovery, route the sanitized contract through [stateful recovery contract review](../stateful-recovery-contract-review/SKILL.md) before documenting executable recovery steps.
3. Write ordered commands with expected observations, decision points, and stop conditions grounded in current implementation.
4. Add validation, rollback or recovery, evidence capture, and escalation steps, then test links and commands safely.

### Gates

- Procedures are executable and expected outcomes are observable.
- Rollback/recovery and escalation are explicit.
- Recovery readiness, human approval, and operational evidence remain separate.
- Incident packets use `docs/05.operations/incidents/<year>/inc-####-<slug>/`; the paired
  postmortem filename is fixed: Filename: `postmortem.md`.

## Outputs

- One typed runbook at `docs/05.operations/runbooks/####-<slug>.md` with executable, topic-specific procedure.

## Failure Handling

Do not publish commands that are unimplemented, destructive without approval, or unverifiable; route design gaps back to Spec/Plan. A static readiness review cannot be presented as a successful recovery.

## References

- [Documentation writer](../../roles/doc-writer.md)
- [Operations scope](../../governance/quality-standards.md)
- [Documentation protocol](../../governance/documentation-protocol.md)
- [Stateful recovery contract review](../stateful-recovery-contract-review/SKILL.md)
