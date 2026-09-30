---
title: "Agent Governance Canonical Adapter Architecture"
version: "1.3.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "AD-0027"
parent_ids:
- "REQ-0024"
created: "2026-06-01"
---
# Agent Governance Canonical Adapter Architecture

## Context and Stakeholders

Even when several AI providers modify the same repository, policy, roles,
skills, SDLC, and approval boundaries must stay single. The maintainer
reviews the norm in `.agents/`, the agent consumes the same norm through the
provider adapter in native runtime form, and the reviewer independently
verifies projection drift.

## System Boundaries

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
- The current Task owns the execution result. After completion, Stage 98
  preserves the frozen body, and Git proves the source and recovery history.
- User-global configuration, credentials, provider availability, and
  deployment state are outside this architecture. The selected canonical
  model-free evaluation target is `.agents/evaluations/`; migration and
  verification evidence belong to the active Spec Package.

## Components

| Component | Responsibility |
| --- | --- |
| canonical agent governance bootstrap and policies | authority resolution, safety, workflow |
| canonical agent governance roles and skills | reusable provider-neutral behavior |
| canonical agent governance knowledge | verified surface-to-authority routing and repository vocabulary |
| canonical evaluation owner | model-free evaluation inputs, distinct from paid or native runtime evidence |
| canonical agent governance prompts | reusable input and output contracts for recurring agent work |
| Provider Registry | provider identity and translation facts |
| Authored native provider documents | provider-specific loading and syntax |
| Generated native adapters | role translation and thin Claude skill pointers |
| Stage 99 Registry | document shape and lifecycle machine contract |
| Validators and suites | focused predicate execution and routing |

## Data Flow

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

## Deployment View

The implementation surface is tracked Markdown, YAML, JSON, TOML, and
validation scripts. Provider sync and governance tests check projection
freshness. A document or adapter change alone does not require Docker
runtime, a remote service, or secret mutation.

## Quality Attributes

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

## Traceability

- [REQ-0024 Agent Governance Standardization](../../01.requirements/0024-agent-governance-standardization.md)
- [ADR-0032 Canonical Agent Governance Home](../decisions/0032-canonical-agent-governance-home.md)
- [ADR-0034 Canonical Knowledge and Prompt Surfaces](../decisions/0034-canonical-knowledge-and-prompt-surfaces.md)
- [canonical agent governance bootstrap](../../../.agents/governance/bootstrap.md)
- [Stage 99 Registry](../../99.templates/registry.json)
