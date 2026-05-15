---
layer: agentic
---

# Subagent Protocol

Spawning, communication, and lifecycle rules for subagents in `hy-home.docker`.

## 1. Spawn Rules

- Spawn subagents through the active runtime's delegated-agent facility — never via inline prompt embedding.
- The local runtime supervisor is `.claude/agents/workflow-supervisor.md`.
- Each subagent MUST `@import` exactly one primary scope file before acting.
- Pass the scope path explicitly in the task prompt; do not rely on ambient context.
- All subagent model calls use `model: "sonnet"` for cost-efficient execution.
- The supervising/orchestrating agent uses `model: "opus"` for routing, final decisions, and coordination.

## 2. Required Preamble (per agent)

```text
@import docs/00.agent-governance/scopes/<layer>.md
# Role: <agent-name> — <one-line purpose>
# Pattern: <pattern-name>
```

## 3. Agent Catalog Reference

### Supervising Runtime Agent

| Agent File                                  | Scope Import          | Runtime Role |
| ------------------------------------------- | --------------------- | ------------ |
| `.claude/agents/workflow-supervisor.md`     | `scopes/agentic.md`   | Final routing and synthesis |

The supervisor coordinates workers and should not be treated as a generic worker replacement.

### Worker Agents

| Agent File                             | Scope Import         | Delegated Agent Name |
| -------------------------------------- | -------------------- | -------------------- |
| `.claude/agents/infra-implementer.md`  | `scopes/infra.md`    | `infra-implementer`  |
| `.claude/agents/security-auditor.md`   | `scopes/security.md` | `security-auditor`   |
| `.claude/agents/incident-responder.md` | `scopes/ops.md`      | `incident-responder` |
| `.claude/agents/code-reviewer.md`      | `scopes/common.md`   | `code-reviewer`      |
| `.claude/agents/doc-writer.md`         | `scopes/docs.md`     | `doc-writer`         |
| `.claude/agents/wiki-curator.md`       | `scopes/docs.md`     | `wiki-curator`       |
| `.claude/agents/iac-reviewer.md`       | `scopes/infra.md`    | `iac-reviewer`       |
| `.claude/agents/drift-detector.md`     | `scopes/infra.md`    | `drift-detector`     |

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
- `AGENTS.md` §3 Runtime Surfaces
- `docs/00.agent-governance/agents/README.md`
- `.claude/agents/workflow-supervisor.md`
