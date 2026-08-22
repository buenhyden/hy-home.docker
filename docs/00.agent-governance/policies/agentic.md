---
profile_id: governance-policy
layer: agentic
---

# Agentic Engineering Policy

Stage 00 defines auditable, provider-neutral AI-agent execution. Canonical
roles live in `roles/`, reusable procedures live in `skills/`, and provider
selection and permission mappings live in `providers/registry.yaml`.

## Execution Rules

- Discover repository evidence and the approved Spec, Plan, and Task before mutation.
- Keep one primary owner for each logical unit and independent review separate.
- Delegation cannot broaden approval, mutation scope, runtime access, or permissions.
- Record commands, results, recovery, skipped checks, and blockers in the Task.
- Generated `.agents/`, `.claude/`, and `.codex/` files are adapters and never
  own policy, role intent, or procedure content.

## Delegation Contract

Delegate only to a role declared in `roles/` and mapped by the provider
registry. Each envelope names the role and primary responsibility, exact owned
files or read-only scope, governing Spec/Plan/Task, acceptance checks, mutation
and external-action boundaries, shared-worktree non-reversion rule, and required
return evidence.

Workers report `working`, `blocked`, or `done`. A supervisor may request one
narrower retry after a failed check. Repeated failure, conflicting authority,
missing approval, or expanding blast radius stops and escalates. Provider
delivery and hook events are neither approval nor completion evidence.

## Lifecycle

The sequence is discovery, applicability, approved execution, focused
verification, independent review, and completion evidence. Failed verification
returns to implementation; rejected design stays in planning; missing authority
stops at approval. Retry bounds and provider controls come from the provider
registry, not prompt-local policy.

## Related Documents

- [Bootstrap policy](bootstrap.md)
- [Workflows](workflows.md)
- [Task checklists](task-checklists.md)
- [Provider registry](../providers/registry.yaml)
- [Workflow supervisor](../roles/workflow-supervisor.md)
