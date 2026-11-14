---
title: "Agent Governance Canonical Adapter Architecture"
version: "1.6.3"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-14"
layer: "architecture"
artifact_id: "AD-0027"
parent_ids:
- "REQ-0024"
created: "2026-06-01"
---

# Agent Governance Canonical Adapter Architecture

## Overview

### Purpose and Readers

Policy, provider translation, document shape and execution evidence have
separate canonical owners. Both providers read the same repository-owned
instructions through their native adapters and share one memory store through
`scripts/operations/agent_memory.py`; native Claude memory is off.
Even when several AI providers modify the same repository, policy, roles,
skills, SDLC, and approval boundaries must stay single. The maintainer
reviews the norm in `.agents/`, the agent consumes the same norm through the
provider adapter in native runtime form, and the reviewer independently
verifies projection drift.

### System Boundary

- `.agents/` owns policy, workflow, canonical roles/skills, and the provider
  boundary.
- Stage 99 owns the typed contract for docs profile, path, identity,
  lifecycle, and template.
- `.agents/governance/`, `.agents/roles/`, `.agents/skills/`,
  `.agents/knowledge/`, `.agents/prompts/` are the authored canonical source,
  not generated output or a compatibility copy.
- `.agents/knowledge/` owns verified navigational knowledge that routes to the
  canonical owner and bounded durable facts with invalidation, and
  `.agents/prompts/` owns the input/output contract for reusable prompts. Neither category duplicates mandatory rules or procedure
  bodies, and neither owns execution progress state.
- `.claude/provider.md` and `.codex/provider.md` own each provider's loading
  and syntax differences. Generated README, role, and Claude skill adapters,
  and existing runtime mechanics, neither define shared policy nor overwrite
  the canonical source.
- The current Task owns the execution result. After completion, its durable
  meaning moves to current owners, the package is deleted, and version history
  keeps its body.
- User-global configuration, credentials, provider availability, and
  deployment state are outside this architecture. `.agents/evaluations/README.md`
  routes paired Skill task, raw output, scoring and aggregate evidence. Current
  quality policy owns QA admission; agentic policy owns evaluation authority and
  the current Task owns execution and acceptance. New evidence requires bounded
  Stage 99 classification; representative scores grant no runtime authority.

## Context and Constraints

### Context

The maintainer reviews the norm in `.agents/`, the agent consumes it through the provider adapter in native runtime form, and the reviewer verifies projection drift. Claude and Codex read the same repository-owned instructions and share one memory store through `scripts/operations/agent_memory.py`.

### Constraints

Policy, roles, skills, SDLC and approval boundaries must stay single even when several AI providers modify the same repository. The canonical `.agents/` sources are never generated output, native Claude memory is off, and user-global configuration, credentials and deployment state are outside this architecture.

## Current Structure

### Building Blocks

| Component | Responsibility |
| --- | --- |
| canonical agent governance bootstrap and policies | authority resolution, safety, workflow |
| canonical agent governance roles and skills | reusable provider-neutral behavior |
| canonical agent governance knowledge | verified surface-to-authority routing and repository vocabulary |
| paired Skill evaluation evidence | task/output/scoring/aggregate relationship; no recurring scoring or runtime authority |
| canonical agent governance prompts | reusable input and output contracts for recurring agent work |
| Provider Registry | provider identity and translation facts |
| Authored native provider documents | provider-specific loading and syntax |
| Generated native adapters | role translation and thin Claude skill pointers |
| Stage 99 Registry | document shape and lifecycle machine contract |
| Validators and suites | focused predicate execution and routing |

Governance, role, skill, knowledge and prompt documents are English and every
`README.md` is Korean; each profile's Registry `language` field decides, and
the documentation protocol owns the rule. Native adapters consume the same
meaning without creating another language or policy authority.

### Runtime and Deployment

#### Runtime View

Bootstrap moves from the root shim to the shared agent governance policy and
the matching provider adapter. It selectively loads only the canonical
role/skill and the active Spec/Task the request needs. The canonical
`SKILL.md` uses `name`, `description`, and `metadata` that carries the
existing contract. Codex's skill-local `allow_implicit_invocation: false` and
Claude's `disable-model-invocation: true` require explicit invocation, and
discovery itself is neither an approval nor observed runtime acceptance.
The Provider Registry's translation facts generate and verify the native
surface, and the Stage 99 Registry verifies the profile and lifecycle of
repository documents. The execution result returns to the current Task and
the reviewed Git diff. Handoff is a derived Task view that rechecks repository
and worktree identity,
approval, evidence, and bounded shared allocations before resumption.

#### Deployment View

The implementation surface is tracked Markdown, YAML, JSON, TOML, and
validation scripts. Provider sync and governance tests check projection
freshness. A document or adapter change alone does not require Docker
runtime, a remote service, or secret mutation.

## Interfaces

### Contracts

- Bootstrap moves from the root shim to the shared policy and the matching provider adapter, per the Runtime View.
- The Provider Registry carries provider identity and translation facts, and the Stage 99 Registry carries document shape and lifecycle.
- The canonical `SKILL.md` uses `name`, `description` and `metadata`, and native adapters require explicit invocation.

### Failure Boundaries

This description records no failure boundary beyond its Risks: static renderer parity proves tracked configuration only, and a provider runtime change can alter the loading behavior that an authored adapter describes. An adapter cannot relax the shared approval boundary.

## Decisions

### Decision Links

- [ADR-0032 Canonical Agent Governance Home](../decisions/0032-canonical-agent-governance-home.md)
- [ADR-0034 Canonical Knowledge and Prompt Surfaces](../decisions/0034-canonical-knowledge-and-prompt-surfaces.md)

### Quality and Risks

#### Quality Attributes

- **Determinism**: the same source and registry must produce the same
  projection and verdict.
- **Security**: an adapter cannot relax the shared agent governance approval
  boundary.
- **Maintainability**: policy, provider translation, and document schema each
  have exactly one owner.
- **Efficiency**: bootstrap loads request-relevant context, not the whole
  corpus.
- **Recoverability**: use Git diff and history instead of separate snapshots
  or SHA pins.

#### Risks

- Static renderer parity proves tracked configuration only; native invocation, hook
  trust and runtime acceptance need direct evidence.
- A provider runtime change can alter loading behavior that the authored
  adapter describes.

## Traceability

### Requirement Mapping

- [REQ-0024 Agent Governance Standardization](../../01.requirements/0024-agent-governance-standardization.md)

### Currentness and Lineage

- [canonical agent governance bootstrap](../../../.agents/governance/bootstrap.md)
- [Stage 99 Registry](../../99.templates/registry.json)
- SPEC-0264 (retired; version history) delivered folder guides through the provider adapters and the shared hook dispatcher.

#### Evolution

- A new provider enters through a Provider Registry entry and an authored
  adapter, never a second policy copy.
