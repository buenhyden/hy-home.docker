---
profile_id: architecture-description
status: active
artifact_id: AD-0027
artifact_type: architecture-description
parent_ids:
  - REQ-0024
created: 2026-06-01
updated: 2026-08-21
---
# Agent Governance Canonical Adapter Architecture Description

## Context and Stakeholders

이 문서는 `hy-home.docker`의 AI Agent 거버넌스와 provider adapter 표준화를 위한 참조 아키텍처를 정의한다. 핵심 구조는 Stage 00을 canonical policy/catalog layer로 두고, Claude와 Codex runtime surface는 같은 catalog를 각 provider 형식으로 노출하는 adapter layer로 제한하는 것이다.

## Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

Agent governance architecture는 repository-local instruction authority, stage-gated documentation lifecycle, provider adapter parity, hook/validator guardrails, and co-located Task evidence를 하나의 추적 가능한 체계로 묶는다.

Stage 00은 active policy와 catalog를 소유한다. Provider directories는 runtime mechanics를 소유하지만 policy를 재정의하지 않는다. Stage 01/02 문서는 왜 이 구조가 필요한지와 어떤 trade-off를 선택했는지를 보존한다.

## System Boundaries

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

- **Owns**:
  - Stage 00 canonical agent and function catalog.
  - Provider adapter parity rules for `.claude/`, `.codex/`, and `.agents/`.
  - Skill and workflow routing boundaries.
  - Hook, validator, and co-located Task evidence relationships.
  - Graphify advisory boundary for knowledge navigation.
- **Consumes**:
  - Product requirements from `docs/01.requirements/0024-agent-governance-standardization.md`.
  - Existing Stage 00 policies, canonical roles and skills, and provider registry.
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

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Performance**: Agent bootstrap should use JIT loading and targeted context retrieval so governance checks do not require reading every repository document.
- **Security**: Agents must not read or expose secrets; provider adapters must not bypass Stage 00 safety and approval rules.
- **Reliability**: Provider surfaces must preserve name-set, role, policy, model, and validation parity with Stage 00.
- **Scalability**: New agents, functions, and skills should be added once in Stage 00 and then exposed through provider adapters.
- **Observability**: Governance work must leave co-located Task evidence and validation outputs sufficient for review.
- **Operability**: Validators and sync scripts must provide deterministic failure signals for template, traceability, adapter, and repository contract drift.

## Components

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

The architecture has four layers.

| Layer | Responsibility | Canonical Paths |
| --- | --- | --- |
| Requirement and decision layer | Defines why agent governance exists and which architecture decision is accepted. | `docs/01.requirements/`, `docs/02.architecture/` |
| Canonical governance layer | Owns active policies, roles, skills, workflows, and provider registry. | `docs/00.agent-governance/` |
| Provider adapter layer | Exposes Stage 00 catalog in provider-specific formats and hook/skill mechanics. | `.claude/`, `.codex/`, `.agents/` |
| Evidence and validation layer | Records execution evidence and validates drift. | `docs/03.specs/####-<slug>/tasks/`, `scripts/validation/`, `scripts/operations/`, `scripts/knowledge/` |

The Stage 00 canonical adapter model is the architecture boundary between policy and runtime mechanics. Policy changes belong in Stage 00 and must be reflected downstream. Adapter files may adapt syntax and execution mechanics, but they must not introduce separate governance.

## Data Flow

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

- **Key Entities / Flows**:
  - PRD requirement -> Architecture Description architecture boundary -> ADR decision -> Stage 00 policy -> provider adapter -> validation evidence.
  - Stage 00 catalog -> sync-provider-surfaces -> provider runtime surfaces.
  - Task execution -> co-located Task work log -> bounded verification and review evidence.
- **Storage Strategy**:
  - Active policy remains in tracked Markdown under `docs/00.agent-governance/`.
  - Provider adapter definitions remain in tracked runtime directories.
  - Execution evidence remains in the co-located Task for the active Spec package.
- **Data Boundaries**:
  - Temporary session context is not repository authority; reusable findings belong in the owning policy, design, runbook, or Task.
  - Graphify output is generated/advisory and must be corroborated when health is advisory.
  - Secrets and credential values are outside this architecture's documentable data flow.

## Deployment View

- **Runtime / Platform**:
  - Repository-local Markdown, TOML, JSON, shell scripts, and stage documents.
  - Node/npm/rtk may support future automation through `/home/hy/.local/bin`, with explicit PATH handling where needed.
- **Deployment Model**:
  - Documentation and adapter changes are applied through Git and repository validation.
  - No Docker runtime deployment is required for agent governance documentation alignment.
- **Operational Evidence**:
  - `check-repo-contracts.sh` verifies repository documentation and adapter contracts.
  - `check-document-links.py --mode traceability` verifies selected cross-stage relationships.
  - `sync-provider-surfaces.sh` reports provider surface drift.
  - `generate-llm-wiki.py --check` verifies both generated LLM Wiki outputs.
  - `report-graphify-health.sh` records whether graph context is clean or advisory.

## AI Agent Architecture Descriptions (If Applicable)

- **Model/Provider Strategy**:
  - Model policy belongs in `providers/registry.yaml` and the provider adapter descriptions.
  - Provider adapters must not promote new model IDs or reasoning-effort values without Stage 00 alignment.
- **Tooling Boundary**:
  - Agents may run non-destructive validation commands.
  - Runtime, deployment, secret, and remote-protection changes require explicit approval.
- **Context Strategy**:
  - Agents load the bootstrap policy, provider registry, applicable role/skill contract, and current co-located Task.
  - Durable findings are written to the owning tracked policy, design, runbook, or Task rather than a parallel handoff surface.
- **Guardrail Boundary**:
  - Hooks and validators enforce or warn on repository contracts.
  - Provider hooks route guardrails but do not define independent policy.
- **Latency / Cost Budget**:
  - JIT loading and targeted searches are preferred over broad document ingestion.
  - Graphify can accelerate navigation, but advisory graph claims require tracked-source corroboration.

## Traceability

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [Agent Governance Standardization Product Requirements](../../01.requirements/0024-agent-governance-standardization.md)
- **ADR**: [ADR-0027: Stage 00 Canonical Adapter Model](../decisions/0027-stage-00-canonical-adapter-model.md)
- **Current Plan**: Agent Governance Decision Items and Attachment-Gap Plan
- **Current Task**: Agent Governance Missing Items Implementation Task
- **Stage 00 Governance Hub**: [Agent governance](../../00.agent-governance/README.md)
- **Operations**: [Operations index](../../05.operations/README.md)
