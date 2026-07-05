---
status: active
---
<!-- Target: docs/02.architecture/requirements/0027-agent-governance-canonical-adapter.md -->

# Agent Governance Canonical Adapter Architecture Reference Document (ARD)

## Overview

이 문서는 `hy-home.docker`의 AI Agent 거버넌스와 provider adapter 표준화를 위한 참조 아키텍처를 정의한다. 핵심 구조는 Stage 00을 canonical policy/catalog layer로 두고, Claude, Codex, Gemini runtime surface는 같은 catalog를 각 provider 형식으로 노출하는 adapter layer로 제한하는 것이다.

## Summary

Agent governance architecture는 repository-local instruction authority, stage-gated documentation lifecycle, provider adapter parity, hook/validator guardrails, advisory memory, and execution evidence를 하나의 추적 가능한 체계로 묶는다.

Stage 00은 active policy와 catalog를 소유한다. Provider directories는 runtime mechanics를 소유하지만 policy를 재정의하지 않는다. Stage 01/02 문서는 왜 이 구조가 필요한지와 어떤 trade-off를 선택했는지를 보존한다.

## Boundaries & Non-goals

- **Owns**:
  - Stage 00 canonical agent and function catalog.
  - Provider adapter parity rules for `.claude/`, `.codex/`, and `.agents/`.
  - Skill and workflow routing boundaries.
  - Hook, validator, memory/progress, and task evidence relationships.
  - Graphify advisory boundary for knowledge navigation.
- **Consumes**:
  - Product requirements from `docs/01.requirements/024-agent-governance-standardization.md`.
  - Existing Stage 00 rules, scopes, provider overlays, and subagent protocol.
  - Runtime adapter files and sync/validation scripts.
  - Phase 1 diagnostic and Phase 2 alignment plan.
- **Does Not Own**:
  - Docker service runtime state, secrets, deployment, or remote GitHub protection settings.
  - User-global Codex settings or credentials.
  - Provider model availability outside the repository policy baseline.
  - Operations procedures unrelated to agent governance.
- **Non-goals**:
  - Do not replace the existing service/tier architecture documents.
  - Do not broaden the HADS mandatory profile beyond `docs/90.references/data/hads/`.
  - Do not recreate retired Codex Markdown prompt files.
  - Do not create a separate active governance layer under provider directories.

## Quality Attributes

- **Performance**: Agent bootstrap should use JIT loading and targeted context retrieval so governance checks do not require reading every repository document.
- **Security**: Agents must not read or expose secrets; provider adapters must not bypass Stage 00 safety and approval rules.
- **Reliability**: Provider surfaces must preserve name-set, role, policy, model, and validation parity with Stage 00.
- **Scalability**: New agents, functions, and skills should be added once in Stage 00 and then exposed through provider adapters.
- **Observability**: Governance work must leave task evidence, progress log entries, and validation outputs sufficient for review.
- **Operability**: Validators and sync scripts must provide deterministic failure signals for template, traceability, adapter, and repository contract drift.

## System Overview & Context

The architecture has four layers.

| Layer | Responsibility | Canonical Paths |
| --- | --- | --- |
| Requirement and decision layer | Defines why agent governance exists and which architecture decision is accepted. | `docs/01.requirements/`, `docs/02.architecture/` |
| Canonical governance layer | Owns active policy, catalog, workflows, scopes, provider-neutral rules, and advisory memory contract. | `docs/00.agent-governance/` |
| Provider adapter layer | Exposes Stage 00 catalog in provider-specific formats and hook/skill mechanics. | `.claude/`, `.codex/`, `.agents/` |
| Evidence and validation layer | Records execution evidence and validates drift. | `docs/04.execution/`, `scripts/validation/`, `scripts/operations/`, `scripts/knowledge/` |

The Stage 00 canonical adapter model is the architecture boundary between policy and runtime mechanics. Policy changes belong in Stage 00 and must be reflected downstream. Adapter files may adapt syntax and execution mechanics, but they must not introduce separate governance.

## Data Architecture

- **Key Entities / Flows**:
  - PRD requirement -> ARD architecture boundary -> ADR decision -> Stage 00 policy -> provider adapter -> validation evidence.
  - Stage 00 catalog -> sync-provider-surfaces -> provider runtime surfaces.
  - Task execution -> progress log -> optional memory note for durable findings.
- **Storage Strategy**:
  - Active policy remains in tracked Markdown under `docs/00.agent-governance/`.
  - Provider adapter definitions remain in tracked runtime directories.
  - Execution evidence remains in Stage 04 task documents and progress log rows.
- **Data Boundaries**:
  - Memory notes are advisory retrieval context, not active policy.
  - Graphify output is generated/advisory and must be corroborated when health is advisory.
  - Secrets and credential values are outside this architecture's documentable data flow.

## Infrastructure & Deployment

- **Runtime / Platform**:
  - Repository-local Markdown, TOML, JSON, shell scripts, and stage documents.
  - Node/npm/rtk may support future automation through `/home/hy/.local/bin`, with explicit PATH handling where needed.
- **Deployment Model**:
  - Documentation and adapter changes are applied through Git and repository validation.
  - No Docker runtime deployment is required for agent governance documentation alignment.
- **Operational Evidence**:
  - `check-repo-contracts.sh` verifies repository documentation and adapter contracts.
  - `check-doc-traceability.sh` verifies selected cross-stage relationships.
  - `sync-provider-surfaces.sh` reports provider surface drift.
  - `generate-llm-wiki-index.sh --check` verifies generated index freshness.
  - `report-graphify-health.sh` records whether graph context is clean or advisory.

## AI Agent Architecture Requirements (If Applicable)

- **Model/Provider Strategy**:
  - Model policy belongs in `subagent-protocol.md` and provider overlays.
  - Provider adapters must not promote new model IDs or reasoning-effort values without Stage 00 alignment.
- **Tooling Boundary**:
  - Agents may run non-destructive validation commands.
  - Runtime, deployment, secret, and remote-protection changes require explicit approval.
- **Memory & Context Strategy**:
  - Agents must read `memory/README.md` and `memory/progress.md` for repository work.
  - Durable findings go to memory notes only when reusable and not active policy.
- **Guardrail Boundary**:
  - Hooks and validators enforce or warn on repository contracts.
  - Provider hooks route guardrails but do not define independent policy.
- **Latency / Cost Budget**:
  - JIT loading and targeted searches are preferred over broad document ingestion.
  - Graphify can accelerate navigation, but advisory graph claims require tracked-source corroboration.

## Related Documents

- **PRD**: [Agent Governance Standardization Product Requirements](../../01.requirements/024-agent-governance-standardization.md)
- **ADR**: [ADR-0027: Stage 00 Canonical Adapter Model](../decisions/0027-stage-00-canonical-adapter-model.md)
- **Current Plan**: [Agent Governance Decision Items and Attachment-Gap Plan](../../04.execution/plans/2026-06-02-agent-governance-decision-items-plan.md)
- **Current Task**: [Agent Governance Missing Items Implementation Task](../../04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md)
- **Stage 00 Governance Hub**: [Agent governance](../../00.agent-governance/README.md)
- **Operations**: [Operations index](../../05.operations/README.md)
