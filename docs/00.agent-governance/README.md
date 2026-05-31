---
layer: agentic
---

# AI Agent Governance Hub

> Canonical governance system for coding agents in this repository.

## Overview

- Purpose: deterministic, auditable, token-efficient agent execution for a shared harness-engineering and agent-first engineering workspace.
- Entry point: root shims (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) route agents into this hub.
- Compliance boundary: stage-gate lifecycle in `docs/01` to `docs/05`, plus `docs/90` and `docs/99`.

## Audience

- AI Agents
- Documentation Writers
- Repository Maintainers

## Scope

- Language: every file in `docs/00.agent-governance/` must be English-only.
- Root files must stay thin; detailed policy must live under this directory.
- `docs/01` to `docs/99` are read-only by default and require explicit user approval for mutation.

## Core Concepts

- **Governance SSoT**: `docs/00.agent-governance/` owns policy, provider overlays,
  agent catalog contracts, and validation expectations. Runtime directories expose
  those contracts; they do not define separate governance.
- **Provider Parity Model**: Claude remains the canonical runtime surface,
  Codex mirrors `.claude/` content with provider-native model identifiers, and
  Gemini exposes reference-index pointers.
- **Template Contract**: target-stage documents use the mapped template from
  `docs/99.templates/` before editing and retain required headings, lifecycle
  metadata, target-relative links, and one `## Related Documents` section.
- **Clarification Duty**: when the task is underspecified, constraints conflict,
  or a likely assumption could change the outcome, stop and ask before changing
  state. Do not silently choose a risky interpretation.

## Structure

- `rules/`: shared governance policies, completion gates, and [JIT Markers](rules/jit-markers.md) (e.g. `[LOAD:MEMORY]`). Includes the cross-provider [Capability Matrix](rules/provider-capability-matrix.md), [Output Style Contract](rules/output-style.md), and [Workflows](rules/workflows.md).
- `scopes/`: layer-specific boundaries, file ownership SSOT, and subagent bridge guidance.
- `providers/`: runtime-specific overlays (`claude`, `gemini`, `codex`, provider-neutral `agents-md`).
- `agents/`: local agent/function catalog of workspace agents and orchestration functions.
- `memory/`: durable governance notes, audit findings, and the agent progress log.
  - `memory/README.md` — memory policy.
  - `memory/progress.md` — mandatory work progress log.
- `subagent-protocol.md`: spawn rules, communication protocol, and agent lifecycle.

## How to Work in This Area

1. Resolve layer and load persona before any mutation.
2. Load the pre-task checklist and `[LOAD:RULES:AGENTIC]`.
3. Load exactly one primary scope.
4. Use `subagent-protocol.md` and `workflow-supervisor` for cross-domain or delegated work.
5. For PR-related tasks, load `[LOAD:RULES:GITHUB]` and verify the Completion Gate.
6. Review `memory/progress.md` before editing.
7. Ask for clarification before state changes when the request is underspecified
   or governance constraints conflict.
8. Run completion checklist and update `memory/progress.md`.

## Related Documents

- `rules/agentic.md`
- `rules/bootstrap.md`
- `rules/jit-markers.md`
- `rules/github-governance.md`
- `subagent-protocol.md`
- `providers/agents-md.md`
