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
- Each subagent MUST `@import` exactly one primary scope file before acting.
- Pass the scope path explicitly in the task prompt; do not rely on ambient context.
- The supervising/orchestrating agent uses the top-spec model; worker subagents use the right-sized model per the Model Policy below.
- Each runtime's agent frontmatter MUST carry that provider's own model identifier; never copy another provider's model name across surfaces.

### Model Policy (provider-equivalent mapping)

| Tier                  | Role                                | Claude       | Gemini             | GPT / Codex       |
| --------------------- | ----------------------------------- | ------------ | ------------------ | ----------------- |
| Supervisor (top spec) | routing, final decisions, synthesis, planning, architecture, refactoring | `opus-4.8`   | `gemini-3.1-pro`   | `gpt-5.5`         |
| Worker (right-sized)  | scoped task execution, repetitive editing, doc organizing, summarization | `sonnet-4.6` | `gemini-3.5-flash` | `gpt-5.4-mini` |

- This table is the single source of truth for the "provider equivalent" model tiers. The
  Claude column uses human-readable version names; `.claude/agents/*.md` carry the Claude
  Code model aliases `opus` (Supervisor) and `sonnet` (Worker), which resolve to `opus-4.8`
  and `sonnet-4.6`. `.codex/agents/*.toml` and `.agents/` carry the literal identifiers shown.
- `workflow-supervisor` is the only Supervisor-tier role; all other catalog agents are Worker tier.
- The model mapping is enforced by `scripts/validation/check-repo-contracts.sh`.
- The Model Policy baseline date is 2026-05-29. The table is enforced as
  repository policy, but local validation does not prove provider availability
  on that date. Do not treat newer provider docs as proof of the 2026-05-29
  baseline. Baseline evidence is recorded in the Phase 3 implementation task.
  `gpt-5.3-codex` may be introduced only as an explicit code-specialized
  worker override after official archived/provider evidence or a
  repository-approved evidence note is linked and the same provider-adapter
  checks are updated; it is not the default worker model.
- **Codex Reasoning Effort Policy**: Codex TOML adapters MUST include
  `model_reasoning_effort`. `workflow-supervisor` uses `xhigh` for governance,
  planning, architecture, and complex refactors. Default workers use `medium`
  unless an approved task requires `high`; repetitive formatting-only work may
  use `low` through a task-specific override.
- **Gemini Reasoning Policy**: Antigravity IDE manages reasoning effort strictly via model selection. `gemini-3.1-pro` is mandated for tasks requiring high reasoning effort (planning, complex refactors), while `gemini-3.5-flash` is used for standard/low reasoning effort (repetitive edits, text classification).

## 2. Required Preamble (per agent)

```text
@import docs/00.agent-governance/scopes/<layer>.md
# Role: <agent-name> — <one-line purpose>
# Pattern: <pattern-name>
```

## 3. Agent Catalog Reference

### Supervising Runtime Agent

| Governance Role | Scope Import | Stage 00 Catalog | Claude Adapter | Codex Adapter | Gemini Adapter |
| --- | --- | --- | --- | --- | --- |
| `workflow-supervisor` | `scopes/agentic.md` | `agents/agents/workflow-supervisor.md` | `.claude/agents/workflow-supervisor.md` | `.codex/agents/workflow-supervisor.toml` | `.agents/agents/workflow-supervisor.md` |

The supervisor coordinates workers and should not be treated as a generic worker replacement.

### Worker Agents

All worker agents use the same adapter pattern:

| Governance Role | Scope Import | Stage 00 Catalog | Claude Adapter | Codex Adapter | Gemini Adapter |
| --- | --- | --- | --- | --- | --- |
| `infra-implementer` | `scopes/infra.md` | `agents/agents/infra-implementer.md` | `.claude/agents/infra-implementer.md` | `.codex/agents/infra-implementer.toml` | `.agents/agents/infra-implementer.md` |
| `security-auditor` | `scopes/security.md` | `agents/agents/security-auditor.md` | `.claude/agents/security-auditor.md` | `.codex/agents/security-auditor.toml` | `.agents/agents/security-auditor.md` |
| `incident-responder` | `scopes/ops.md` | `agents/agents/incident-responder.md` | `.claude/agents/incident-responder.md` | `.codex/agents/incident-responder.toml` | `.agents/agents/incident-responder.md` |
| `code-reviewer` | `scopes/common.md` | `agents/agents/code-reviewer.md` | `.claude/agents/code-reviewer.md` | `.codex/agents/code-reviewer.toml` | `.agents/agents/code-reviewer.md` |
| `doc-writer` | `scopes/docs.md` | `agents/agents/doc-writer.md` | `.claude/agents/doc-writer.md` | `.codex/agents/doc-writer.toml` | `.agents/agents/doc-writer.md` |
| `wiki-curator` | `scopes/docs.md` | `agents/agents/wiki-curator.md` | `.claude/agents/wiki-curator.md` | `.codex/agents/wiki-curator.toml` | `.agents/agents/wiki-curator.md` |
| `iac-reviewer` | `scopes/infra.md` | `agents/agents/iac-reviewer.md` | `.claude/agents/iac-reviewer.md` | `.codex/agents/iac-reviewer.toml` | `.agents/agents/iac-reviewer.md` |
| `drift-detector` | `scopes/infra.md` | `agents/agents/drift-detector.md` | `.claude/agents/drift-detector.md` | `.codex/agents/drift-detector.toml` | `.agents/agents/drift-detector.md` |
| `qa-engineer` | `scopes/qa.md` | `agents/agents/qa-engineer.md` | `.claude/agents/qa-engineer.md` | `.codex/agents/qa-engineer.toml` | `.agents/agents/qa-engineer.md` |
| `ci-cd-engineer` | `scopes/ops.md` | `agents/agents/ci-cd-engineer.md` | `.claude/agents/ci-cd-engineer.md` | `.codex/agents/ci-cd-engineer.toml` | `.agents/agents/ci-cd-engineer.md` |
| `skill-creator` | `scopes/agentic.md` | `agents/agents/skill-creator.md` | `.claude/agents/skill-creator.md` | `.codex/agents/skill-creator.toml` | `.agents/agents/skill-creator.md` |
| `hook-developer` | `scopes/agentic.md` | `agents/agents/hook-developer.md` | `.claude/agents/hook-developer.md` | `.codex/agents/hook-developer.toml` | `.agents/agents/hook-developer.md` |
| `rules-engineer` | `scopes/agentic.md` | `agents/agents/rules-engineer.md` | `.claude/agents/rules-engineer.md` | `.codex/agents/rules-engineer.toml` | `.agents/agents/rules-engineer.md` |
| `style-enforcer` | `scopes/agentic.md` | `agents/agents/style-enforcer.md` | `.claude/agents/style-enforcer.md` | `.codex/agents/style-enforcer.toml` | `.agents/agents/style-enforcer.md` |

Per the Stage 00 Canonical Adapter Model (`providers/agents-md.md` §5): Stage 00
is canonical, provider surfaces are adapters, and all surfaces carry the same
agent name set.

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
