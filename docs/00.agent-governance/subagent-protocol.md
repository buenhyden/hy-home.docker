---
layer: agentic
---

# Subagent Protocol

Spawning, communication, and lifecycle rules for subagents in `hy-home.docker`.

## 1. Spawn Rules

- Spawn subagents through the active runtime's delegated-agent facility — never via inline prompt embedding.
- The Claude runtime supervisor implementation is `.claude/agents/workflow-supervisor.md`.
- Each subagent MUST `@import` exactly one primary scope file before acting.
- Pass the scope path explicitly in the task prompt; do not rely on ambient context.
- All subagent model calls use `model: "sonnet"` (or provider equivalent) for cost-efficient execution.
- The supervising/orchestrating agent uses `model: "opus"` (or provider equivalent) for routing, final decisions, and coordination.

## 2. Required Preamble (per agent)

```text
@import docs/00.agent-governance/scopes/<layer>.md
# Role: <agent-name> — <one-line purpose>
# Pattern: <pattern-name>
```

## 3. Agent Catalog Reference

### Supervising Runtime Agent

| Governance Role | Scope Import | Claude Implementation | Gemini Implementation |
| --- | --- | --- | --- |
| `workflow-supervisor` | `scopes/agentic.md` | `.claude/agents/workflow-supervisor.md` | `.agents/agents/workflow-supervisor.md` |

The supervisor coordinates workers and should not be treated as a generic worker replacement.

### Worker Agents

| Governance Role | Scope Import | Claude Implementation | Gemini Implementation |
| --- | --- | --- | --- |
| `infra-implementer` | `scopes/infra.md` | `.claude/agents/infra-implementer.md` | `.agents/agents/infra-implementer.md` |
| `security-auditor` | `scopes/security.md` | `.claude/agents/security-auditor.md` | `.agents/agents/security-auditor.md` |
| `incident-responder` | `scopes/ops.md` | `.claude/agents/incident-responder.md` | `.agents/agents/incident-responder.md` |
| `code-reviewer` | `scopes/common.md` | `.claude/agents/code-reviewer.md` | `.agents/agents/code-reviewer.md` |
| `doc-writer` | `scopes/docs.md` | `.claude/agents/doc-writer.md` | `.agents/agents/doc-writer.md` |
| `wiki-curator` | `scopes/docs.md` | `.claude/agents/wiki-curator.md` | `.agents/agents/wiki-curator.md` |
| `iac-reviewer` | `scopes/infra.md` | `.claude/agents/iac-reviewer.md` | `.agents/agents/iac-reviewer.md` |
| `drift-detector` | `scopes/infra.md` | `.claude/agents/drift-detector.md` | `.agents/agents/drift-detector.md` |

Note: Codex/GPT uses the governance catalog directly without native agent file support.

## 4. Communication Protocol

- **Data handoff**: write runtime intermediate artifacts to `_workspace/<phase>_<agent>_<artifact>.<ext>`.
- **Audit handoff**: write orchestration reports, matrices, plans, and approval handoffs to `.agent-work/report/` when a workflow prompt requires that location.
- **Status updates**: use TaskUpdate (`in_progress` → `completed` | `failed`).
- **Conflict**: if file ownership conflicts arise, halt and escalate to user — do not overwrite.

## 5. Error Handling

1. On first failure: retry once with narrower scope.
2. On second failure: mark task `failed`, report findings, continue without that result.
3. Never silently discard output — record gaps in completion notes.

## 6. Lifecycle

```text
Spawn → @import scope → execute → write artifact → TaskUpdate(completed) → cleanup _workspace
```

Dead `_workspace/` files are preserved for audit; do not delete without user approval.

## Related Documents

- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/task-checklists.md`
- `docs/00.agent-governance/rules/postflight-checklist.md`
- `AGENTS.md` — Runtime Surfaces
- `docs/00.agent-governance/agents/README.md`
- `.claude/agents/workflow-supervisor.md`
