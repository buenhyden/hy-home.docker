---
layer: agentic
---

# Subagent Protocol

Spawning, communication, and lifecycle rules for subagents in `hy-home.docker`.

## 1. Spawn Rules

- Spawn subagents through the active runtime's delegated-agent facility — never via inline prompt embedding.
- The Stage 00 catalog entry for the supervisor is
  `docs/00.agent-governance/agents/agents/workflow-supervisor.md`; each
  provider exposes a runtime adapter for that role.
- Each subagent MUST load exactly one primary scope file through the active
  runtime's supported context or delegation mechanism before acting.
- Pass the scope path explicitly in the task prompt; do not rely on ambient context.
- Resolve every delegated role's registered work profile through
  `contracts/agent-catalog.yaml`; provider-native values are generated from the
  typed provider contract.

### Model Policy Routing

`contracts/provider-models.yaml` is the sole owner of model identifiers,
reasoning controls, lifecycle, disposition, runtime acceptance, fallbacks, and
source evidence. `contracts/agent-catalog.yaml` assigns one work profile to
each registered role. Human protocol prose does not copy either mapping;
native adapters are renderer outputs.

### Model and Provider Adapter Change Protocol

User approval may authorize model policy or provider adapter changes, but those
changes remain governed by the typed path authority and provider renderer.
Record the approved typed value, target role, source evidence, and provider
sync result in the co-located Task; do not create a protocol-local override.

If the task does not name a concrete model value, role, provider, and validation
path, the approval is recorded as verified-only and existing model/provider
adapter values remain unchanged.

## 2. Required Delegation Envelope

```text
Primary scope: docs/00.agent-governance/scopes/<layer>.md
# Role: <agent-name> — <one-line purpose>
# Pattern: <pattern-name>
```

## 3. Agent Catalog Reference

### Supervising Runtime Agent

| Governance Role | Scope Import | Stage 00 Catalog | Claude Adapter | Codex Adapter | Compatibility Projection |
| --- | --- | --- | --- | --- | --- |
| `workflow-supervisor` | `scopes/agentic.md` | `agents/agents/workflow-supervisor.md` | `.claude/agents/workflow-supervisor.md` | `.codex/agents/workflow-supervisor.toml` | `.agents/agents/workflow-supervisor.md` |

The supervisor coordinates workers and should not be treated as a generic worker replacement.

### Worker Agents

All worker agents use the same adapter pattern:

| Governance Role | Scope Import | Stage 00 Catalog | Claude Adapter | Codex Adapter | Compatibility Projection |
| --- | --- | --- | --- | --- | --- |
| `infra-implementer` | `scopes/infra.md` | `agents/agents/infra-implementer.md` | `.claude/agents/infra-implementer.md` | `.codex/agents/infra-implementer.toml` | `.agents/agents/infra-implementer.md` |
| `security-auditor` | `scopes/security.md` | `agents/agents/security-auditor.md` | `.claude/agents/security-auditor.md` | `.codex/agents/security-auditor.toml` | `.agents/agents/security-auditor.md` |
| `incident-responder` | `scopes/ops.md` | `agents/agents/incident-responder.md` | `.claude/agents/incident-responder.md` | `.codex/agents/incident-responder.toml` | `.agents/agents/incident-responder.md` |
| `code-reviewer` | `scopes/common.md` | `agents/agents/code-reviewer.md` | `.claude/agents/code-reviewer.md` | `.codex/agents/code-reviewer.toml` | `.agents/agents/code-reviewer.md` |
| `doc-writer` | `scopes/docs.md` | `agents/agents/doc-writer.md` | `.claude/agents/doc-writer.md` | `.codex/agents/doc-writer.toml` | `.agents/agents/doc-writer.md` |
| `iac-reviewer` | `scopes/infra.md` | `agents/agents/iac-reviewer.md` | `.claude/agents/iac-reviewer.md` | `.codex/agents/iac-reviewer.toml` | `.agents/agents/iac-reviewer.md` |
| `drift-detector` | `scopes/infra.md` | `agents/agents/drift-detector.md` | `.claude/agents/drift-detector.md` | `.codex/agents/drift-detector.toml` | `.agents/agents/drift-detector.md` |
| `qa-engineer` | `scopes/qa.md` | `agents/agents/qa-engineer.md` | `.claude/agents/qa-engineer.md` | `.codex/agents/qa-engineer.toml` | `.agents/agents/qa-engineer.md` |
| `eval-engineer` | `scopes/qa.md` | `agents/agents/eval-engineer.md` | `.claude/agents/eval-engineer.md` | `.codex/agents/eval-engineer.toml` | `.agents/agents/eval-engineer.md` |
| `ci-cd-engineer` | `scopes/ops.md` | `agents/agents/ci-cd-engineer.md` | `.claude/agents/ci-cd-engineer.md` | `.codex/agents/ci-cd-engineer.toml` | `.agents/agents/ci-cd-engineer.md` |
| `skill-creator` | `scopes/agentic.md` | `agents/agents/skill-creator.md` | `.claude/agents/skill-creator.md` | `.codex/agents/skill-creator.toml` | `.agents/agents/skill-creator.md` |
| `hook-developer` | `scopes/agentic.md` | `agents/agents/hook-developer.md` | `.claude/agents/hook-developer.md` | `.codex/agents/hook-developer.toml` | `.agents/agents/hook-developer.md` |
| `rules-engineer` | `scopes/agentic.md` | `agents/agents/rules-engineer.md` | `.claude/agents/rules-engineer.md` | `.codex/agents/rules-engineer.toml` | `.agents/agents/rules-engineer.md` |

Per the Stage 00 Canonical Adapter Model (`providers/agents-md.md` §5): Stage 00
is canonical, provider surfaces are adapters, and all surfaces carry the same
agent name set.

## 4. Communication Protocol

- **Data handoff**: write non-secret runtime intermediate artifacts to `_workspace/repo-support/<phase>_<agent>_<artifact>.<ext>`.
- **Audit handoff**: write orchestration reports, matrices, plans, and approval handoffs to `.agent-work/report/` when a workflow prompt requires that location.
- **Status updates**: use the active runtime's status mechanism and the shared
  `in_progress` → `completed` or `failed` semantics.
- **Conflict**: if file ownership conflicts arise, halt and escalate to user — do not overwrite.
- **Prohibited data**: do not store diagnostics dumps, local logs, raw logs,
  auth files, tokens, credentials, private keys, shell history, secret values,
  or token-bearing command output in `_workspace`.

## 5. Error Handling

Use the exact semantic loop values and evidence bounds in
`contracts/provider-models.yaml`. Delegation does not define another retry,
stop, escalation, permission, or evidence policy.

## 6. Lifecycle

`rules/workflows.md` is the sole human-readable lifecycle owner. Delegation and
scope loading occur inside its applicable state; typed loop transitions remain
in `contracts/provider-models.yaml`.

## Related Documents

- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/task-checklists.md`
- `docs/00.agent-governance/rules/postflight-checklist.md`
- `docs/01.requirements/prd-0024-agent-governance-standardization.md`
- `docs/02.architecture/descriptions/ad-0027-agent-governance-canonical-adapter.md`
- `docs/02.architecture/decisions/adr-0027-stage-00-canonical-adapter-model.md`
- `AGENTS.md` — Runtime Surfaces
- `docs/00.agent-governance/agents/README.md`
- `.claude/agents/workflow-supervisor.md`
