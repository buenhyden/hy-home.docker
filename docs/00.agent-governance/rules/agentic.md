---
layer: agentic
title: "AI Agent-first Engineering Rule"
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
- Use persona routing, checklist routing, this rule, and one primary scope before
  task execution.
- Use the local harness catalog as the runtime boundary:
  - `.claude/agents/*.md` mirrors `docs/00.agent-governance/agents/agents/*.md`.
  - `.claude/skills/*/skill.md` mirrors `docs/00.agent-governance/agents/functions/*.md`.
  - `docs/00.agent-governance/subagent-protocol.md` defines delegation rules.
- Do not import external harness identities or create GitHub-native instruction
  layers for local execution policy.
- Keep governance text in English and user-facing responses in Korean by default.

## 3. Implementation Flow

1. Bootstrap via `rules/bootstrap.md`.
2. Load persona via `rules/persona.md` and announce active persona/layer.
3. Load `rules/task-checklists.md` and run pre-task gate.
4. Load this Agent-first rule.
5. Load one primary scope from `scopes/<layer>.md`.
6. Discover current repository state with read-only commands.
7. Plan the smallest scoped change and name the verification gate.
8. Execute the change in place.
9. Verify with the smallest checks that prove the contract.
10. Report changed files, checks run, and any residual risk or out-of-scope gap.

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
- Keep the runtime harness mirror synchronized across `.claude/` and
  `docs/00.agent-governance/agents/`.
- Record historical notes under `docs/00.agent-governance/memory/`; do not use
  memory notes as active policy.
