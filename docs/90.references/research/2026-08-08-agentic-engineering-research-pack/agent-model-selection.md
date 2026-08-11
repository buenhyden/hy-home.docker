---
status: draft
artifact_id: reference:agentic-engineering-research:agent-model-selection
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-08
review_cycle: on-source-change
---

# Reference: Task-Aware Agent Model Selection

## Overview

The workspace selects models by role work profile, not by per-prompt model
shopping. A task first routes to a canonical role; that role declares one of
five profiles; the typed provider contract then supplies the exact native
model and effort/thinking value. This provides deterministic configuration but
does not prove runtime acceptance, entitlement, execution, quality, cost, or
latency.

## Purpose

Satisfy REQ-29 with task-characteristic selection rules covering role/tier,
model, effort, settings, evaluation, fallback, and atomic change surfaces.

## Repository Role

This Stage 90 analysis explains the existing Model Policy. The policy owners
remain `provider-models.yaml`, `agent-catalog.yaml`, `subagent-protocol.md`, the
renderer, and validators. Recommendations here require a later approved
Stage 03/04 change before they can alter a value.

## Scope

### In scope

- Task characteristics, five work profiles, and provider-native controls.
- Evidence required before selection, fallback, or override changes.
- Evaluation and rollback rules for a proposed model-policy change.

### Out of scope

- Live provider calls, entitlement inspection, price comparison, or benchmarks.
- Direct edits to generated adapters or session-only model overrides.
- Automatic fallback not encoded by the typed contract.

## Definitions / Facts

### Deterministic selection sequence

1. Classify the task by outcome, complexity, reversibility, sensitivity,
   volume, latency tolerance, and required independent challenge.
2. Route to the canonical agent whose scope and permission profile own it.
3. Read that role's single `work_profile` from `agent-catalog.yaml`.
4. Resolve the provider-native exact model/control from
   `provider-models.yaml`; never translate an effort label across providers.
5. Confirm lifecycle, repository disposition, runtime acceptance, entitlement,
   and activation eligibility separately.
6. If acceptance/entitlement evidence is missing, keep `needs_revalidation`;
   do not silently substitute or invent a fallback.
7. Validate repository semantics and, for a policy change, run an approved
   comparative evaluation before updating all coupled surfaces atomically.

### Task-characteristic mapping

| Work profile | Task characteristics | Claude | Codex | Gemini | Selection boundary |
| --- | --- | --- | --- | --- | --- |
| `long-horizon-supervision` | Architecture, planning, orchestration, final synthesis, long context | `claude-opus-5` / `xhigh` | `gpt-5.6-sol` / `xhigh` | `gemini-3.6-flash` / `high` | Supervisor-only; not a generic escalation for workers. |
| `complex-implementation` | Multi-step implementation, tool use, bounded mutation, verification depth | `claude-sonnet-5` / `high` | `gpt-5.6-sol` / `high` | `gemini-3.6-flash` / `high` | Requires workspace-write role and approved scope. |
| `adversarial-review` | Correctness, policy, security, infrastructure, edge cases | `claude-opus-5` / `high` | `gpt-5.6-sol` / `xhigh` | `gemini-3.6-flash` / `high` | Read-only reviewer distinct from implementer. |
| `evidence-research` | Primary-source retrieval, documentation, bounded synthesis | `claude-sonnet-5` / `low` | `gpt-5.6-terra` / `medium` | `gemini-3.5-flash-lite` / `medium` | Source quality and claim calibration matter more than model branding. |
| `routine-validation` | Deterministic checks, drift classification, repetitive bounded work | `claude-haiku-4-5-20251001` / no effort field | `gpt-5.6-terra` / `low` | `gemini-3.5-flash-lite` / `minimal` | Use only when completion is decided by deterministic evidence. |

These are configured repository defaults. The official pages support the
general task-fit hypotheses, but no tracked comparative benchmark establishes
cross-provider equivalence.

### Effort and setting rules

- Use the lowest registered effort that meets the profile; never lower a
  review/supervision gate for convenience.
- Claude `effort`, Codex `model_reasoning_effort`, and Gemini scoped
  `thinkingLevel` are different native mechanisms.
- Claude/Codex product-level orchestration modes such as ultracode/Ultra are
  not ordinary per-agent effort values and are not in the local policy.
- A provider default, user setting, organization cap, allowlist, alias,
  resumed session, or safety fallback can change the effective runtime model.
  Repository validation cannot observe that substitution.
- Model configuration is not authorization to access tools, mutate protected
  surfaces, or bypass sandbox/approval controls.

### Evaluation gate

The existing 11 synthetic fixtures and 16 regressions check repository
semantics such as routing, closure, model-status honesty, and provider
boundaries. They do not compare live models. A proposed default/profile change
therefore needs versioned representative tasks, the current value as baseline,
an explicit rubric/scorer and threshold, failure cases, privacy boundary,
latency/token observations where permitted, reviewer calibration, and a
rollback literal. Provider prose is a hypothesis, not an acceptance test.

### Fallback policy

The typed workspace contract defines no automatic model fallback graph.
Claude Code can perform provider-native availability or safety fallbacks, but
that capability is external behavior and may substitute a model without a
repository change. Codex product/config sources cited here do not establish a
local automatic fallback. Any desired repository fallback must name trigger,
ordered exact values, entitlement/acceptance evidence, quality floor,
observability, rollback, and coupled changes before adoption.

### Atomic change surface

A model, effort, profile, or fallback change is incomplete unless the same
approved unit updates or verifies all applicable owners:

1. `contracts/provider-models.yaml` and `subagent-protocol.md`;
2. `contracts/agent-catalog.yaml` when role/profile routing changes;
3. provider renderer logic and every generated adapter/config output;
4. validators, deterministic fixtures, and regression expectations;
5. Stage 04 approval, exact source/date, evaluation, validation, and rollback;
6. provider-surface sync and independent specification/quality review.

## Scope Implications

| Scope | Application and disposition |
| --- | --- |
| `agentic` | Owns work profiles, provider mapping, renderer, and change protocol; only `workflow-supervisor` uses the supervisor tier. |
| `architecture` | Route architecture judgment to the supervisor profile, but first resolve the scope's missing agent record and lifecycle owner. |
| `backend` | Not applicable today; a future backend role/model requires an approved surface, Spec, evaluation, and typed route. |
| `common` | `code-reviewer` uses adversarial review; shared work cannot self-upgrade or bypass independent review. |
| `docs` | `doc-writer` uses evidence research; source traceability and calibration remain mandatory at a lower effort. |
| `entry` | Current gateway work routes through infra profiles; model choice does not authorize runtime gateway mutation. |
| `frontend` | No typed frontend role exists; use the current owner for the QA fixture and require a policy decision before adding one. |
| `infra` | Implementers use complex implementation and reviewers adversarial/routine profiles; runtime evidence stays separate. |
| `meta` | Metadata work routes through docs until the missing typed scope is resolved; deterministic validators decide completion. |
| `mobile` | Not applicable to the current corpus; no model selection is inferred for a nonexistent mobile role. |
| `ops` | Operational implementation uses complex profiles; incident/runtime outcomes and rate limits require direct evidence. |
| `product` | No typed product role exists; stakeholder judgment and product approval cannot be delegated to a model tier. |
| `qa` | Owns comparative evaluation design and routine/complex test execution; synthetic scores are not live-model scores. |
| `security` | Security review uses adversarial profile and read-only permissions; specialized-provider labels never imply entitlement. |

## Sources

| Source | Accessed | Class | Verification state |
| --- | --- | --- | --- |
| [Anthropic models overview](https://platform.claude.com/docs/en/about-claude/models/overview) | 2026-08-08T16:18:04+09:00 | External mutable | HTTP 200 via canonical redirect; task-fit/lifecycle facts only. |
| [Claude Code model configuration](https://code.claude.com/docs/en/model-config) | 2026-08-08T16:18:04+09:00 | External mutable | HTTP 200; effort, alias, restriction, and fallback mechanics. |
| [Codex models](https://learn.chatgpt.com/docs/models) | 2026-08-08T16:18:04+09:00 | External mutable | HTTP 200; task-fit and reasoning guidance. |
| [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) | 2026-08-08T16:18:04+09:00 | External mutable | HTTP 200; `model` and native configuration fields. |
| [Provider model contract](../../../00.agent-governance/contracts/provider-models.yaml) | 2026-08-08 | Workspace tracked | Five profiles, 11 model rows, and separated status axes at Task 4 baseline. |
| [Agent catalog contract](../../../00.agent-governance/contracts/agent-catalog.yaml) | 2026-08-08 | Workspace tracked | Fourteen role-to-profile assignments and evaluation owner. |
| [Provider model evaluation function](../../../00.agent-governance/agents/functions/provider-model-evaluation.md) | 2026-08-08 | Workspace tracked | Source, native-schema, regression, and `needs_revalidation` gate. |

## Maintenance

Revalidate when task taxonomy, roles, profiles, exact IDs, provider reasoning
controls/defaults, evaluation fixtures, fallback capability, renderer, or
validators change. Never update a generated adapter alone.

## Related Documents

- [Provider model landscape](./provider-model-landscape.md)
- [AI agent catalogs](./ai-agent-catalogs.md)
- [Agent instructions](./agent-instructions-vibe-coding.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md)
