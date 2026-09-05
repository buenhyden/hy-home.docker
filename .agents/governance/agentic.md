---
title: "Agentic Engineering Policy"
version: "1.0.1"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
---

# Agentic Engineering Policy

Agent governance defines auditable, provider-neutral AI-agent execution. Canonical
roles live in `.agents/roles/`, reusable procedures live in `.agents/skills/`, and provider
selection and permission mappings live in `.agents/governance/providers/registry.yaml`.

## Execution Rules

- Discover repository evidence and the approved Spec, Plan, and Task before mutation.
- Keep one primary owner for each logical unit and independent review separate.
- Delegation cannot broaden approval, mutation scope, runtime access, or permissions.
- Record commands, results, recovery, skipped checks, and blockers in the Task.
- Generated native role and skill projections are adapters and never own shared
  policy, role intent, or procedure content. Authored native `provider.md` files
  own loading and syntax differences only; `.agents/` is canonical input.
- The shared PostToolUse hook normalizes changed Markdown, shell, YAML, and JSON
  text, runs `shfmt`, `shellcheck`, and `yamllint` on changed files where those
  tools are available, and runs `git diff --check` before repository validators.
  Inspect the resulting diff before committing.

## Delegation Contract

Delegate only to a role declared in `.agents/roles/` and mapped by the provider
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
stops at approval. Retry bounds come from [workflows.md](workflows.md); provider
controls come from the provider registry. Neither may be replaced by
prompt-local policy.

## Related Documents

- [Bootstrap policy](bootstrap.md)
- [Workflows](workflows.md)
- [Task checklists](task-checklists.md)
- [Provider registry](providers/registry.yaml)
- [Workflow supervisor](../roles/workflow-supervisor.md)
