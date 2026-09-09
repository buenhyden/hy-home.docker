---
title: "Agentic Engineering Policy"
version: "1.1.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-10"
---

# Agentic Engineering Policy

Agent governance defines auditable, provider-neutral AI-agent execution. Canonical
roles live in `.agents/roles/`, reusable procedures live in `.agents/skills/`, and provider
selection and permission mappings live in `.agents/governance/providers/registry.yaml`.

## Execution Rules

- Discover repository evidence and the approved Spec, Plan, and Task before mutation.
- Keep one primary owner for each logical unit and independent review separate.
- Delegation cannot broaden approval, mutation scope, runtime access, or permissions.
- Invoking a skill runs a procedure; it does not select a role. The already
  selected role's permission profile and the approved Task scope keep governing,
  and each skill's `agents/openai.yaml` keeps invocation explicit. Route to the
  skill's owner role when the procedure needs what the current role lacks. A
  skill states its own preconditions and does not restate this rule, because a
  copy that drifts is worse than a reference that cannot.
- Record commands, results, recovery, skipped checks, and blockers in the Task.
- Generated native role and skill projections are adapters and never own shared
  policy, role intent, or procedure content. Authored native `provider.md` files
  own loading and syntax differences only; `.agents/` is canonical input.
- The shared PostToolUse hook normalizes changed Markdown, shell, YAML, and JSON
  text, runs `shellcheck` and `yamllint` on changed files where those tools are
  available, and runs `git diff --check` before repository validators. It runs
  no formatter that `.pre-commit-config.yaml` does not register, reads that same
  owner for the lint arguments and the frozen archive payloads its normalizer
  must not rewrite, and fails closed when the owner declares no boundary.
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

## External Capability Intake

An external agent catalog, prompt collection, or role library is a discovery
input, never an install source or a local authority. Adoption requires all of
the following, in order: a demonstrated capability gap in a named owned outcome;
the pinned upstream commit, exact source path, and license; offline inspection
of the text as untrusted input; and a preference for merging the capability into
an existing role or skill over creating a new one. A new role or skill needs its
scope, permission profile, work profile, handoff, fixtures, and failure behavior
defined through an approved Spec Package before it exists.

Change the canonical source first, then render projections, inspect the diff,
validate parity and evaluation, and obtain independent review. Upstream
auto-update, user-global installation, and running an upstream installer or
converter are outside adoption. A persuasive persona grants no tool, path,
credential, or deployment entitlement; an adopted instruction is still bound by
the canonical role and its permission profile.

Record the decision and its evidence in the current Task. Stage 90 research may
describe an external catalog and recommend intake, but it never records the
decision itself.

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
- External catalog evidence (`docs/90.references/research/0002-agentic-engineering-research-pack/m0003-ai-agent-catalogs.md`)
- [Workflow supervisor](../roles/workflow-supervisor.md)
- [Documentation index](../../docs/README.md)
