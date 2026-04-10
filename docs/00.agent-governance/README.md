---
layer: agentic
---

# AI Agent Governance Hub

This directory is the canonical governance system for coding agents in this repository.

## 1. Context and Objective

- Purpose: deterministic, auditable, token-efficient agent execution.
- Entry point: root shims (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) route agents into this hub.
- Compliance boundary: stage-gate lifecycle in `docs/01` to `docs/11`, plus `docs/90` and `docs/99`.

## 2. Requirements and Constraints

- Language: every file in `docs/00.agent-governance/` must be English-only.
- Root files must stay thin; detailed policy must live under this directory.
- `docs/01` to `docs/99` are read-only by default and require explicit user approval for mutation.

## 3. Directory Structure

- `rules/`: shared governance policies and completion gates.
  - `bootstrap.md` · `persona.md` · `task-checklists.md` · `stage-authoring-matrix.md`
  - `documentation-protocol.md` (§6 DOCS 3 RULES HALT)
  - `postflight-checklist.md` — run after every task before declaring completion
  - `github-governance.md` — GitHub-aligned policy baseline (branch protection, PR contracts, Actions security, AI instruction hierarchy)
- `scopes/`: layer-specific boundaries, file ownership SSOT, and subagent bridge (§6 §7 per scope).
- `providers/`: runtime-specific overlays (`claude`, `gemini`, provider-neutral `agents-md`).
- `memory/`: durable governance notes and audit findings.
  - `progress.md` — phase tracker and L1–L7 layer audit status
- `subagent-protocol.md` — spawn rules, communication protocol, and agent lifecycle.

## 4. JIT Markers

### Stage Markers

| Marker               | Target                          | Purpose                         |
| :------------------- | :------------------------------ | :------------------------------ |
| `[LOAD:PRD]`         | `docs/01.prd/README.md`         | Product intent and requirements |
| `[LOAD:ARD]`         | `docs/02.ard/README.md`         | Architecture reference          |
| `[LOAD:ADR]`         | `docs/03.adr/README.md`         | Decision history                |
| `[LOAD:SPECS]`       | `docs/04.specs/README.md`       | Technical source of truth       |
| `[LOAD:PLANS]`       | `docs/05.plans/README.md`       | Implementation planning         |
| `[LOAD:TASKS]`       | `docs/06.tasks/README.md`       | Execution evidence              |
| `[LOAD:GUIDES]`      | `docs/07.guides/README.md`      | Human-facing guidance           |
| `[LOAD:OPS]`         | `docs/08.operations/README.md`  | Operational policy              |
| `[LOAD:RUNBOOKS]`    | `docs/09.runbooks/README.md`    | Operational procedures          |
| `[LOAD:INCIDENTS]`   | `docs/10.incidents/README.md`   | Incident records                |
| `[LOAD:POSTMORTEMS]` | `docs/11.postmortems/README.md` | Lessons learned                 |
| `[LOAD:REFERENCES]`  | `docs/90.references/README.md`  | Stable references               |
| `[LOAD:TEMPLATES]`   | `docs/99.templates/README.md`   | Document templates              |

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

## 5. Operational Procedure

1. Resolve layer and load persona before any mutation.
2. Load exactly one primary scope.
3. Run pre-task checklist before implementation.
4. Use stage authoring matrix for any documentation authoring/refactoring task.
5. For PR-related tasks, load `[LOAD:RULES:GITHUB]` and verify GitHub completion gate (§6 of that rule) before declaring done.
6. Run completion checklist and record out-of-scope findings in `memory/`.

## 6. Maintenance and Safety

- Keep policy concise and non-contradictory.
- Remove stale links and nonexistent command references immediately in editable scope.
- For out-of-scope breakages, record findings in an English memory note with remediation guidance.

## Related Documents

- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/standards.md`
- `docs/00.agent-governance/subagent-protocol.md`
