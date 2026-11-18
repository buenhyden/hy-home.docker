---
name: "ops-runbook-agent"
description: "Use when implemented and verified operational behavior needs an executable runbook with expected signals, recovery, and escalation."
metadata:
  title: "ops-runbook-agent"
  version: "1.4.1"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-11-18"
  function_id: "ops-runbook-agent"
  scope: "ops"
  owner_agent: "doc-writer"
---

# ops-runbook-agent

## Trigger

### When to Use

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

Operational behavior must be implemented and verified; commands, expected outcomes, rollback, and escalation owners must be known.

### When Not to Use

Commands that are unimplemented, destructive without approval or unverifiable are outside this skill, and design gaps route back to the Spec or Plan.

## Procedure

### Steps

1. Define when the runbook applies, required access, safety checks, and the exact starting state.
2. For stateful recovery, route the sanitized contract through [stateful recovery contract review](../stateful-recovery-contract-review/SKILL.md) before documenting executable recovery steps.
3. Write ordered commands with expected observations, decision points, and stop conditions grounded in current implementation.
4. Add validation, rollback or recovery, evidence capture, and escalation steps, then test links and commands safely.

#### Gates

- Procedures are executable and expected outcomes are observable.
- Rollback/recovery and escalation are explicit.
- Recovery readiness, human approval, and operational evidence remain separate.
- Incident packets use `docs/05.operations/incidents/<year>/inc-####-<slug>/`; the paired
  postmortem filename is fixed: Filename: `postmortem.md`.

#### Inputs

- Implemented operational behavior and verification commands.
- Preconditions, safety controls, rollback/recovery steps, and escalation boundary.

### Failure Handling

Do not publish commands that are unimplemented, destructive without approval, or unverifiable; route design gaps back to Spec/Plan. A static readiness review cannot be presented as a successful recovery.

## Outputs

### Artifacts

- One typed runbook at `docs/05.operations/runbooks/<NN-domain>/####-<slug>.md` with executable, topic-specific procedure.

### Handoff

Owning role, policies and related documents:

- [Documentation writer](../../roles/doc-writer.md)
- [Operations scope](../../../docs/00.workspace/03.quality/quality-standards.md)
- [Documentation protocol](../../../docs/00.workspace/02.process/documentation-protocol.md)
- [Stateful recovery contract review](../stateful-recovery-contract-review/SKILL.md)

## Verification

### Checks

- Every command has an expected observation and a stop condition.
- Rollback or recovery and escalation steps are present.
- `scripts/validation/check-document-metadata.py --mode check-changed` and `scripts/validation/check-document-links.py --mode alignment` pass for the runbook.

### Limits

A static readiness review cannot be presented as a successful recovery.
