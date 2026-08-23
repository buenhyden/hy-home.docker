---
profile_id: governance-skill
layer: agentic
function_id: ops-runbook-agent
scope: ops
status: active
owner_agent: doc-writer
---

# ops-runbook-agent

## Preconditions

Operational behavior must be implemented and verified; commands, expected outcomes, rollback, and escalation owners must be known.

## Inputs

- Implemented operational behavior and verification commands.
- Preconditions, safety controls, rollback/recovery steps, and escalation boundary.

## Procedure

1. Define when the runbook applies, required access, safety checks, and the exact starting state.
2. Write ordered commands with expected observations, decision points, and stop conditions grounded in current implementation.
3. Add validation, rollback or recovery, evidence capture, and escalation steps, then test links and commands safely.

## Outputs

- One typed runbook at `docs/05.operations/catalog/<domain>/####-<slug>/runbook.md` with executable, topic-specific procedure.

## Gates

- Procedures are executable and expected outcomes are observable.
- Rollback/recovery and escalation are explicit.
- Incident packets use `docs/05.operations/incidents/<year>/inc-####-<slug>/`; the paired
  postmortem filename is fixed: Filename: `postmortem.md`.

## Failure Handling

Do not publish commands that are unimplemented, destructive without approval, or unverifiable; route design gaps back to Spec/Plan.

## Related Documents

- [Documentation writer](../roles/doc-writer.md)
- [Operations scope](../roles/ops.md)
- [Documentation protocol](../policies/documentation-protocol.md)
