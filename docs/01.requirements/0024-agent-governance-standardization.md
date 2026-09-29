---
title: "Agent Governance Standardization Requirements"
version: "1.3.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "requirements"
artifact_id: "REQ-0024"
parent_ids: []
created: "2026-06-01"
---
# Agent Governance Standardization Requirements

## Problem and Goals

The AI agents in this repository must follow one governance model and one
SDLC even when their execution format differs by provider. The goal is to
separate the owners of policy, provider translation, document format, and
execution evidence, and to keep `.claude/` and `.codex/` from degrading into
independent policy sources.

## Stakeholders and User Needs

- The maintainer must be able to immediately tell which document is
  canonical in case of a conflict.
- An AI agent must load only the minimum policy, role, skill, Spec, and Task
  needed for the request.
- A reviewer must be able to reproduce the difference between provider
  projection and the canonical source, the approval boundary, and the
  verification result.
- An operator needs an explicit approval boundary so agent work does not
  expand into secrets, runtime, deployment, or remote state.

## Functional Requirements

- **REQ-0024-FR-0001**: `.agents/` must be the sole normative owner of AI agent
  policy, workflow, canonical role, canonical skill, and provider boundary.
- **REQ-0024-FR-0002**: The shared agent governance Provider Registry must own
  only provider identity, projection route, model/permission translation, and
  hook binding, and must not intrude on Stage 99's document profile/path/
  template authority.
- **REQ-0024-FR-0003**: `.claude/` and `.codex/` must be adapters that project
  the shared agent governance canonical source into provider or runtime
  format, and must not define separate policy, lifecycle, or completion
  criteria.
  `.agents/` is the actual repository-owned canonical source and holds only
  registered canonical categories. Native provider documents remain the
  authored originals for each of `.claude/` and `.codex/`, and generated
  README files or adapters must not overwrite the canonical source. Codex
  discovers and explicitly reads canonical skills, while Claude uses thin
  generated adapters that link to the canonical source. Skills for both
  providers are invoked explicitly, and discovery, loading, invocation, and
  runtime acceptance must not be claimed as the same evidence. Unknown or
  unsafe content is preserved fail closed and is not deleted automatically.
- **REQ-0024-FR-0004**: Canonical roles and skills must be defined exactly
  once in `.agents/`, and generated/tracked provider surfaces must preserve
  name, role, scope, and source relationships.
- **REQ-0024-FR-0005**: An agent performing repository changes must load the
  relevant Requirement, Architecture, active Spec, and current Task through
  the bootstrap policy and provider adapter.
- **REQ-0024-FR-0006**: The SDLC must use a single flow of
  Requirement -> Architecture/ADR -> Spec -> implementation -> Operations,
  and the current Spec Package's Task must own execution state and evidence.
- **REQ-0024-FR-0007**: General completion judgment must rely on reviewed
  diffs, registered verification results, and current Task evidence, and
  must not require branch SHA pinning, corpus snapshots, or a parallel
  handoff ledger as separate completion conditions.
- **REQ-0024-FR-0008**: Governance gates and fixtures must check only the
  current contract declared by the Stage 99 Registry, script manifest, and
  workflow contract, and must not reproduce retired paths, document bodies,
  or fixed file counts.
- **REQ-0024-FR-0014**: `.agents/`'s canonical categories are limited to
  governance, role, invocable skill, verified navigational knowledge, and
  reusable prompt contract, and selected canonical model-free evaluation input.
  Markdown instruction categories have a registered Stage 99 profile and
  canonical root inventory; evaluator-owned code and data follow the registered
  canonical inventory and script manifest instead. Knowledge and prompt content
  must not duplicate mandatory rules, detailed design, specifications, or runbook
  bodies, and must instead route to the canonical owner. No category owns
  execution progress state, and the current Spec Package Task remains the sole
  progress/handoff authority. Verified knowledge may preserve reusable durable
  domain facts with source, owner, validity, sensitivity, and invalidation; it
  remains navigation, not workflow authority. The selected
  `.agents/evaluations/` target and its migration and verification evidence belong
  to the active Spec Package.

## Non-functional Requirements

- **REQ-0024-NFR-0009**: Rule interpretation and provider projection
  verification must be deterministic and fail closed, with no conflicting
  fallback.
- **REQ-0024-NFR-0010**: `.agents/` must stay English-only except for
  `README.md`, whose language follows the
  [document language rule](../../.agents/governance/documentation-protocol.md#document-language).
  Provider adapters must not lose meaning.
- **REQ-0024-NFR-0011**: Agent permissions must be minimum scope and must not
  expose or change secrets, credentials, private keys, tokens, or
  unapproved external state.
- **REQ-0024-NFR-0012**: A verification failure must be able to identify its
  owner and the target to fix, and a duplicate aggregate gate must not own
  the same predicate more than once.
- **REQ-0024-NFR-0013**: The current document must match the tracked
  implementation, and legacy, deprecated, or conflicting rules must be
  removed from the current surface.

## Constraints

- Shared agent governance policy changes are made only within the approved
  repository scope.
- Provider adapters do not use user-global settings or credentials as
  canonical input.
- Historical body clones, compatibility redirects, and separate progress
  documents are not created.
- Runtime, deployment, secret, and remote GitHub state changes require
  separate explicit approval.

## Acceptance Criteria

- There is no name/source/scope drift between shared agent governance and
  provider surfaces.
- Tracked files under `.claude/` and `.codex/` are classified as authored
  provider adapters, generated projections, or native runtime mechanics that
  the Provider Registry allows.
- The native entry of a canonical skill and its nested governance metadata
  preserve the same ID, owner, and scope, and explicit invocation
  configuration does not expand permissions.
- Every Spec/Plan parent of an active Task is active, and no terminal parent
  has an active child.
- Registered governance and document suites pass without duplicate
  predicates or dependence on historical fixtures.
- The current authority does not use Stage 98 documents or deleted execution
  ledgers as input.

## Traceability

- **Architecture Description**: [AD-0027 Agent Governance Canonical Adapter](../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- **Decision**: [ADR-0032 Canonical Agent Governance Home](../02.architecture/decisions/0032-canonical-agent-governance-home.md)
- **Decision**: [ADR-0034 Canonical Knowledge and Prompt Surfaces](../02.architecture/decisions/0034-canonical-knowledge-and-prompt-surfaces.md)
- **Historical implementation evidence**: [SPEC-0158](../98.archive/completed/03.specs/0158-document-governance-lifecycle-convergence/spec.md)
- **Governance entry**: [canonical agent governance](../../.agents/README.md)
