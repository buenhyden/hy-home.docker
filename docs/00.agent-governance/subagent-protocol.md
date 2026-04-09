---
layer: agentic
---

# Subagent Protocol

Spawning, communication, and lifecycle rules for subagents in `hy-home.docker`.

## 1. Spawn Rules

- Spawn subagents via the **Task tool** only — never via inline prompt embedding.
- Each subagent MUST `@import` exactly one primary scope file before acting.
- Pass the scope path explicitly in the task prompt; do not rely on ambient context.
- All subagent model calls use `model: "opus"` for production quality.

## 2. Required Preamble (per agent)

```text
@import docs/00.agent-governance/scopes/<layer>.md
# Role: <agent-name> — <one-line purpose>
# H100 Pattern: <pattern-id> <pattern-name>
```

## 3. Agent Catalog Reference

| Agent File                             | Scope Import         | Task Tool Name       |
| -------------------------------------- | -------------------- | -------------------- |
| `.claude/agents/infra-implementer.md`  | `scopes/infra.md`    | `infra-implementer`  |
| `.claude/agents/security-auditor.md`   | `scopes/security.md` | `security-auditor`   |
| `.claude/agents/incident-responder.md` | `scopes/ops.md`      | `incident-responder` |
| `.claude/agents/code-reviewer.md`      | `scopes/common.md`   | `code-reviewer`      |
| `.claude/agents/doc-writer.md`         | `scopes/docs.md`     | `doc-writer`         |

## 4. Communication Protocol

- **Data handoff**: write intermediate artifacts to `_workspace/<phase>_<agent>_<artifact>.<ext>`.
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
- `AGENTS.md` §3 Agent Catalog · §4 Orchestration Protocol
