---
layer: agentic
title: 'AI Agent-first Engineering Rule'
---

# AI Agent-first Engineering Rule

Standard behavior contract for repo-local, auditable agent execution.

## 1. Context and Objective

- Treat AI agents as first-class engineering workers with explicit routing,
  scoped ownership, and verification evidence.
- Keep outcomes deterministic, auditable, verifiable, and context-efficient.
- Prefer repository evidence, explicit assumptions, and traceable decisions over
  implicit behavior.

## 2. Requirements and Constraints

- Start with non-mutating discovery before any change.
- Produce implementation plans for multi-step work before edits, unless the user
  already supplied an implementation-ready plan.
- Keep audit, planning, implementation, and verification roles separate when a
  workflow prompt defines those phases.
- Do not execute implementation-agent changes until the approved plan path
  required by the workflow exists and the requested edits map to that plan.
- Use persona routing, checklist routing, this rule, and one primary scope before
  task execution.
- Use the local agent/function catalog as the runtime boundary:
  - The active provider's runtime agent directory (e.g., `.claude/agents/`, `.agents/agents/`) is the executable runtime surface; each file must have a same-named catalog entry under `docs/00.agent-governance/agents/agents/`.
  - The active provider's runtime skill directory (e.g., `.claude/skills/`, `.agents/skills/`) is the executable runtime surface; each skill must have a same-named catalog entry under `docs/00.agent-governance/agents/functions/`.
  - Runtime baselines: Claude uses `.claude/`, Gemini uses `.agents/` as a shared surface/moderate-shim, Codex uses `.codex/`.
  - `docs/00.agent-governance/subagent-protocol.md` defines delegation rules.
- Do not import external harness identities or create GitHub-native instruction
  layers for local execution policy.
- Use `docs/00.agent-governance/memory/` as advisory retrieval context and
  `memory/progress.md` as the running work log. Memory notes must not
  override current rules, scopes, provider overlays, direct user instructions,
  or live repository evidence.
- Keep governance text in English and user-facing responses in Korean by default.

## 3. Implementation Flow

1. Bootstrap via `rules/bootstrap.md`.
2. Load persona via `rules/persona.md` and announce active persona/layer.
3. Load `rules/task-checklists.md` and run pre-task gate.
4. Load this Agent-first rule.
5. Load one primary scope from `scopes/<layer>.md`.
6. Review governance memory and `memory/progress.md`; use `rg` to retrieve
   only relevant notes when the task matches memory triggers.
7. Discover current repository state with read-only commands.
8. Plan the smallest scoped change and name the verification gate.
9. Execute the change in place.
10. Verify with the smallest checks that prove the contract.
11. Update `memory/progress.md` with final progress, verification evidence,
    and durable memory pointers.
12. Report changed files, checks run, and any residual risk or out-of-scope gap.

## 4. Operational Procedures

- Provide concise progress updates during long operations.
- Stop and request clarification when constraints conflict.
- Prefer root-cause analysis over symptom patching.
- Route cross-domain or multi-agent work through `workflow-supervisor`.
- Delegate only to workers listed in `subagent-protocol.md`; do not invent
  runtime teams or untracked roles.
- Prefer existing repository validators before adding new checks.

## 5. Maintenance and Safety

- Keep policy text short and actionable.
- Remove contradictory guidance immediately.
- Keep provider-specific behavior in provider files, not in generic scope/rule files.
- Keep runtime behavior synchronized across the active provider's runtime surface and the corresponding
  `docs/00.agent-governance/agents/` catalog entries.
- Record work progress in `docs/00.agent-governance/memory/progress.md`.
- Record historical notes under `docs/00.agent-governance/memory/` from
  `docs/99.templates/memory.template.md`; do not use memory notes as active policy.

## Related Documents

- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/persona.md`
- `docs/00.agent-governance/rules/task-checklists.md`
- `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- `docs/00.agent-governance/subagent-protocol.md`
