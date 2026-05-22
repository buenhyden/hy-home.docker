---
layer: agentic
---

# AI Agent Governance Hub

> Canonical governance system for coding agents in this repository.

## Overview

- Purpose: deterministic, auditable, token-efficient agent execution for a shared harness-engineering and agent-first engineering workspace.
- Entry point: root shims (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) route agents into this hub; Codex uses `AGENTS.md` plus `.codex/`.
- Compliance boundary: stage-gate lifecycle in `docs/01` to `docs/05`, plus `docs/90` and `docs/99`.

## Audience

This README is for:

- AI Agents
- Documentation Writers
- Repository Maintainers

## Scope

### In Scope

- Language: every file in `docs/00.agent-governance/` must be English-only.
- Root files must stay thin; detailed policy must live under this directory.
- `docs/01` to `docs/99` are read-only by default and require explicit user approval for mutation.

### Out of Scope

- Product, architecture, operation, runbook, or incident content owned by `docs/01` to `docs/05`.
- User-global runtime settings and personal credentials.
- Provider-specific policy duplicated outside the provider overlays.

## Structure

- `rules/`: shared governance policies and completion gates.
  - `bootstrap.md` · `persona.md` · `task-checklists.md` · `stage-authoring-matrix.md`
  - `documentation-protocol.md` (§6 DOCS 3 RULES HALT)
  - `postflight-checklist.md` — run after every task before declaring completion
  - `github-governance.md` — GitHub-aligned policy baseline (branch protection, PR contracts, Actions security, local-instruction boundary)
- `scopes/`: layer-specific boundaries, file ownership SSOT, and subagent bridge (§6 §7 per scope).
- `providers/`: runtime-specific overlays (`claude`, `gemini`, `codex`, provider-neutral `agents-md`).
- `agents/`: local agent/function catalog of workspace agents and orchestration functions.
  - Runtime mirror: 9 Claude agents in `.claude/agents/` and 10 functions in `.claude/skills/`.
- `.claude/`: Claude runtime enforcement layer (`CLAUDE.md`, `settings.json`, hooks, agent files, nested skills).
- `.codex/`: Codex runtime hook/context layer (`hooks.json`, `README.md`).
- `.agents/`: compatibility surface for tools that read `.agents/`; not a policy
  source of truth and not a parallel runtime catalog.
- `memory/`: durable governance notes, audit findings, and the agent progress log.
  - `progress.md` — mandatory work progress log, verification index, and durable memory pointer list
  - `template.md` — local mirror of `docs/99.templates/memory.template.md`
- `subagent-protocol.md` — spawn rules, communication protocol, and agent lifecycle.

## 4. JIT Markers

### Stage Markers

| Marker               | Target                          | Purpose                         |
| :------------------- | :------------------------------ | :------------------------------ |
| `[LOAD:PRD]`         | `docs/01.requirements/README.md`         | Product intent and requirements |
| `[LOAD:ARD]`         | `docs/02.architecture/requirements/README.md`         | Architecture reference          |
| `[LOAD:ADR]`         | `docs/02.architecture/decisions/README.md`         | Decision history                |
| `[LOAD:SPECS]`       | `docs/03.specs/README.md`       | Technical source of truth       |
| `[LOAD:PLANS]`       | `docs/04.execution/plans/README.md`       | Implementation planning         |
| `[LOAD:TASKS]`       | `docs/04.execution/tasks/README.md`       | Execution evidence              |
| `[LOAD:OPERATIONS]`  | `docs/05.operations/README.md`   | Operations knowledge base        |
| `[LOAD:INCIDENTS]`   | `docs/05.operations/incidents/README.md`   | Incident records and postmortems |
| `[LOAD:REFERENCES]`  | `docs/90.references/README.md`  | Stable references               |
| `[LOAD:TEMPLATES]`   | `docs/99.templates/README.md`   | Document templates              |
| `[LOAD:MEMORY]`      | `docs/00.agent-governance/memory/README.md` | Advisory governance memory       |

### Rule Markers

| Marker                      | Rule                              |
| :-------------------------- | :-------------------------------- |
| `[LOAD:RULES:BOOTSTRAP]`    | `rules/bootstrap.md`              |
| `[LOAD:RULES:PERSONA]`      | `rules/persona.md`                |
| `[LOAD:RULES:CHECKLISTS]`   | `rules/task-checklists.md`        |
| `[LOAD:RULES:STAGE-MATRIX]` | `rules/stage-authoring-matrix.md` |
| `[LOAD:RULES:STANDARDS]`    | `rules/standards.md`              |
| `[LOAD:RULES:DOCS]`         | `rules/documentation-protocol.md` |
| `[LOAD:RULES:QUALITY]`      | `rules/quality-standards.md`      |
| `[LOAD:RULES:AGENTIC]`      | `rules/agentic.md`                |
| `[LOAD:RULES:GIT]`          | `rules/git-workflow.md`           |
| `[LOAD:RULES:GITHUB]`       | `rules/github-governance.md`      |

## How to Work in This Area

1. Resolve layer and load persona before any mutation.
2. Load the pre-task checklist and `[LOAD:RULES:AGENTIC]`.
3. Load exactly one primary scope.
4. Run pre-task checklist before implementation.
5. Use `subagent-protocol.md` and `workflow-supervisor` for cross-domain or delegated work.
6. Use stage authoring matrix for any documentation authoring/refactoring task.
7. For PR-related tasks, load `[LOAD:RULES:GITHUB]` and verify GitHub completion gate (§6 of that rule) before declaring done.
8. Review `memory/README.md` and `memory/progress.md` before editing; retrieve one or more relevant memory notes for governance, docs, runtime, or repeated-failure work.
9. Run completion checklist, update `memory/progress.md`, and record durable out-of-scope findings in `memory/` from `docs/99.templates/memory.template.md`.

## Maintenance and Safety

- Keep policy concise and non-contradictory.
- Remove stale links and nonexistent command references immediately in editable scope.
- For out-of-scope breakages, record findings in an English memory note with remediation guidance.

## Related Documents

- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/agentic.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/standards.md`
- `docs/00.agent-governance/subagent-protocol.md`
- `docs/00.agent-governance/providers/codex.md`
- `.claude/CLAUDE.md`
- `.codex/README.md`
