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

- **Governance SSoT**: `docs/00.agent-governance/` owns policy, provider
  overlays, agent catalog contracts, and validation expectations. Runtime
  directories expose those contracts; they do not define separate governance.
- **Agent**: a named role in `agents/agents/` with a scope, purpose, expected
  inputs/outputs, provider adapter bindings, and model tier.
- **Skill / Function**: a reusable capability in `agents/functions/` and, when
  supported by a runtime, a provider adapter under `.claude/skills/`,
  `.codex/skills/`, or `.agents/skills/`. Shared skill policy defines when a
  skill should be considered, what artifact it may produce, and which provider
  surface exposes it; provider-local skill files may not create separate
  governance.
- **Rule**: a shared policy in `rules/` or `scopes/`. Provider files may bind
  rules to runtime mechanics but may not redefine the policy.
- **Hook**: runtime event wiring that routes to shared scripts or behavioral
  gates. Hooks provide enforcement and advisory context; active policy remains
  in Stage 00.
- **Sub-agent**: a delegated agent invocation governed by
  `subagent-protocol.md`; it imports exactly one primary scope and follows the
  shared model policy.
- **Output Style**: the workspace-wide response contract in
  `rules/output-style.md`, with provider-native bindings only where supported.
- **Workflow**: an ordered execution path in `rules/workflows.md` and related
  stage docs that maps context, planning, implementation, validation, and
  evidence capture. External workflow disciplines such as brainstorming,
  implementation planning, TDD, systematic debugging, verification, and branch
  finalization are adapted into the repository stage taxonomy rather than
  copied into non-canonical active docs paths.
- **Memory**: advisory durable context under `memory/`; it supports recall and
  progress logging but never overrides active governance.
- **QA & CI/CD**: shared verification policy in `rules/github-governance.md`,
  `scopes/qa.md`, scripts, and CI docs. Providers execute the same policy with
  provider-native mechanics.
- **Model Policy**: provider-equivalent model and reasoning-effort mapping in
  `subagent-protocol.md`. Runtime surfaces must use only values permitted by
  that policy.
- **Template Contract**: target-stage documents use the mapped template from
  `docs/99.templates/` before editing and retain required headings, lifecycle
  metadata, target-relative links, and one `## Related Documents` section.
- **Provider Adapter Model**: Stage 00 is the canonical runtime catalog.
  Claude, Codex, and Gemini expose provider-specific adapters that must match
  Stage 00 name sets, roles, scopes, models, and validation rules.
- **Clarification Duty**: when the task is underspecified, constraints conflict,
  or a likely assumption could change the outcome, stop and ask before changing
  state. This duty is blocking before planning, implementation, model/config
  changes, and completion claims. Do not silently choose a risky interpretation.

## Governance Coverage Matrix

This matrix records the current Stage 00 coverage and the desired completion
evidence for the shared governance concepts. It is a routing aid; detailed
policy remains in the linked Stage 00 documents.

| Concept           | Current Canonical Surface                                                                  | Desired State / Evidence                                                                                                |
| ----------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| Agent             | `agents/agents/`, `subagent-protocol.md`                                                   | Role, scope, model tier, provider adapter, and delegated-agent lifecycle stay synchronized across provider surfaces.    |
| Skill / Function  | `agents/functions/`, provider skill adapters, `rules/workflows.md`                         | Work uses the lifecycle: discovery -> applicability -> provider loading -> canonical artifact -> validation evidence.   |
| Rule              | `rules/`, `scopes/`                                                                        | Provider overlays bind rules to runtime mechanics without redefining policy.                                            |
| Hook              | Runtime hook configs and `scripts/hooks/`                                                  | Hooks provide enforcement or advisory context and point back to Stage 00 for policy.                                    |
| Sub-agent         | `subagent-protocol.md`                                                                     | Delegation imports exactly one primary scope and follows the shared communication and model policy.                     |
| Output Style      | `rules/output-style.md`                                                                    | Provider output bindings remain behavioral adapters, not separate writing policy.                                       |
| Workflow          | `rules/workflows.md`, stage docs                                                           | Planning, execution, verification, and evidence land in canonical stage paths.                                          |
| Memory            | `memory/README.md`, `memory/progress.md`                                                   | Memory supports recall and progress logging but never overrides active governance.                                      |
| QA & CI/CD        | `scopes/qa.md`, `rules/github-governance.md`                                               | Each change type has local checks, CI-only gates, hook/script evidence, and skipped-check rationale.                    |
| Model Policy      | `subagent-protocol.md`, provider notes                                                     | Model and reasoning-effort values change only when policy, sync script, and validators agree.                           |
| Template Contract | `rules/documentation-protocol.md`, `rules/stage-authoring-matrix.md`, `docs/99.templates/` | Template deviations are audited with file, expected template, reason, approval/evidence owner, and validation evidence. |

## Structure

- `rules/`: shared governance policies, completion gates, and [JIT Markers](rules/jit-markers.md) (e.g. `[LOAD:MEMORY]`). Includes the cross-provider [Capability Matrix](rules/provider-capability-matrix.md), [Output Style Contract](rules/output-style.md), and [Workflows](rules/workflows.md).
- `scopes/`: layer-specific boundaries, file ownership SSOT, and subagent bridge guidance.
- `providers/`: runtime-specific overlays (`claude`, `gemini`, `codex`, provider-neutral `agents-md`).
- `agents/`: local agent/function catalog of workspace agents and orchestration functions.
- `memory/`: durable governance notes, audit findings, and the agent progress log.
  - `memory/README.md` — memory policy.
  - `memory/progress.md` — mandatory work progress log.
- `subagent-protocol.md`: spawn rules, communication protocol, and agent lifecycle.
- `harness-implementation-map.md`: routing map from harness surfaces to their canonical Stage 00 / script sources.
- `rules/approval-boundaries.md`: protected-surface and approval matrix for harness work.

## How to Work in This Area

1. Resolve layer and load persona before any mutation.
2. Load the pre-task checklist and `[LOAD:RULES:AGENTIC]`.
3. Load exactly one primary scope.
4. Use `subagent-protocol.md` and `workflow-supervisor` for cross-domain or delegated work.
5. For PR-related tasks, load `[LOAD:RULES:GITHUB]` and verify the Completion Gate.
6. Review `memory/progress.md` before editing.
7. Ask for clarification before state changes when the request is underspecified
   or governance constraints conflict.
8. Before changing model/config values, confirm the Stage 00 policy, provider
   sync script, and validators already encode the same permitted value.
9. Run completion checklist and update `memory/progress.md`.

## Related Documents

- `../01.requirements/2026-06-01-agent-governance-standardization.md`
- `../02.architecture/requirements/0027-agent-governance-canonical-adapter.md`
- `../02.architecture/decisions/0027-stage-00-canonical-adapter-model.md`
- `rules/agentic.md`
- `rules/bootstrap.md`
- `rules/jit-markers.md`
- `rules/github-governance.md`
- `rules/approval-boundaries.md`
- `harness-implementation-map.md`
- `subagent-protocol.md`
- `providers/agents-md.md`
