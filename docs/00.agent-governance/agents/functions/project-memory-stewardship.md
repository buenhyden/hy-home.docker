---
layer: agentic
artifact_type: agent-function
function_id: project-memory-stewardship
scope: docs
status: active
---

# project-memory-stewardship

## Preconditions

The active Stage 04 Task, verified Git state, durable evidence links, and
current-memory bounds must be known before the shared handoff is updated.

## Inputs

- The fixed `memory/current.md` section and label contract.
- Current repository state corroborated against the active Stage 04 Task.
- Durable, value-free evidence links and the next bounded handoff.

## Procedure

1. Verify that the current Task is active and the recorded commit is an
   ancestor of `HEAD`.
2. Replace stale current-state facts in place, preserve the fixed section
   envelope and bounds, and link durable evidence instead of copying it.
3. Check that the result contains no policy body, raw command output, private
   provider state, or duplicated historical progress.

## Outputs

- `bounded-current-state-update`
- `durable-evidence-links`
- `policy-duplication-check`

## Gates

- The record stays within 32 KiB and 400 lines and preserves the registered
  seven-section envelope.
- Evidence remains value-free and resolves to canonical Stage 03 or Stage 04
  owners.
- Active policy remains in rules, scopes, provider overlays, and typed
  contracts rather than Memory.

## Failure Handling

Leave the current record unchanged and report the value-free blocker when Task
state, Git ancestry, evidence ownership, bounds, or material-safety checks do
not pass.

## Related Documents

- [Documentation writer role](../agents/doc-writer.md)
- [Governance memory contract](../../memory/README.md)
- [Current project memory](../../memory/current.md)
- [Spec 134](../../../03.specs/134-agent-governance-canonical-convergence/spec.md)
