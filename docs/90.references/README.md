---
status: active
---

<!-- Target: docs/90.references/README.md -->

# 90.references

> audits, data, research, learning 4축과 LLM Wiki 생성 인덱스로 관리하는 stable reference stage

## Overview

`docs/90.references`는 active stage 문서를 보조하는 안정적인 참고 지식 공간입니다. 이 stage는 요구사항, 아키텍처, 명세, 실행 계획, 운영 문서가 반복해서 참조하는 배경 지식과 기준 정보를 `audits`, `data`, `research`, `learning` 네 축으로 관리합니다. `llm-wiki/`는 이 네 축의 내용을 찾기 위한 generated navigation surface입니다.

Reference 문서는 결정을 내리거나 절차를 실행하는 문서가 아닙니다. 정책은 `docs/00.agent-governance/` 또는 `docs/05.operations/policies/`, 실행 절차는 `docs/05.operations/runbooks/`, 최신 runtime truth는 `infra/`, `scripts/`, registry 파일이 담당합니다.

## Repository Role

`docs/90.references`의 역할은 다음 세 가지입니다.

1. **Stable Context Registry**: 여러 active stage 문서가 반복해서 참조하는 느리게 변하는 배경 지식과 용어를 보관합니다.
2. **Source-Backed Reference Index**: 외부 표준, 논문, 책, repo-local canonical 파일이 어떤 사실을 뒷받침하는지 짧게 연결합니다.
3. **Routing Guard**: 요구사항, 설계 결정, 실행 계획, 운영 절차, incident 기록으로 가야 할 내용을 reference stage에 섞지 않도록 분리 기준을 제공합니다.

이 stage는 active decision authority가 아닙니다. 최신 정책, 실행 명령, 운영 절차, runtime 설정 원문은 해당 canonical stage 또는 runtime 파일에서만 관리합니다.

## Language Boundary

`docs/90.references`는 독자와 산출물 성격에 따라 언어를 나눕니다.

- 사람이 읽는 reference README와 학습/용어/해석 문서는 한국어를 기본으로 작성합니다.
- LLM 탐색, generated index, HADS profile처럼 machine-readable 성격이 강한 문서는 영어를 사용할 수 있습니다.
- Docker image, Kubernetes, HADS, LLM Wiki, Graphify, `infra/`, `scripts/`, registry JSON 같은 upstream 또는 repo-local technical term은 원문을 보존합니다.
- Reference 문서는 policy, runbook, plan, task evidence처럼 보이는 명령형 문장을 만들지 않고, 필요한 경우 canonical stage 문서로 연결합니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 느리게 변하는 개념, 표준, glossary, FAQ
- 외부 표준이나 논문에 대한 짧은 요약과 source links
- repo-local inventory 또는 version-drift 설명 문서
- 학습 로드맵과 이론 배경
- audit 보고서 또는 audit evidence를 보조하는 안정적 분석 reference
- active stage 문서가 반복해서 참조하는 stable context

### Out of Scope

- 현재 진행 중인 요구사항, 설계 결정, 실행 계획, task evidence
- 운영 정책, runbook, incident timeline, postmortem
- 최신 runtime 설정 원문, Compose 파일의 대체본, secret 값
- 빠르게 변하는 외부 뉴스, 가격, 릴리스 상태의 무검증 복사본

## Structure

```text
docs/90.references/
├── audits/       # Stable audit reports, comparison reports, and audit reference indexes
├── data/         # Stable reference data, glossary, profiles, and inventories
├── learning/     # CS/CE/SE learning roadmap and theory references
├── llm-wiki/     # Repo-local LLM navigation map and generated path index
├── research/     # Source-backed research packs and external-source analysis
└── README.md     # This file
```

## Required Format

Reference 문서는 다음 조건을 만족해야 합니다.

- `docs/99.templates/templates/common/reference.template.md`의 필수 섹션을 따른다.
- `status`, `Overview`, `Purpose`, `Repository Role`, `Scope`, `Definitions / Facts`, `Source Rules`, `Sources`, `Maintenance`, `Related Documents`를 포함한다.
- 제목은 `# Reference: <item name>` 형식을 사용한다.
- source가 외부 문서라면 링크와 함께 어떤 사실을 가져왔는지 요약한다.
- source가 repo-local 파일이라면 상대 경로를 사용한다.
- active policy나 runbook을 대체하는 문장을 쓰지 않는다.
- 민감값, token, credential, private key, shell history, raw secret log를 쓰지 않는다.

README 파일은 `docs/99.templates/templates/common/readme.template.md`의 기본 구조를 따르고, 하위 reference 문서를 찾기 위한 index 역할을 합니다.

## Naming and Lifecycle Rules

- Top-level reference category는 `audits/`, `data/`, `research/`, `learning/` 중 하나를 사용한다.
- `llm-wiki/`는 generated navigation surface로만 사용하고, 일반 reference category로 확장하지 않는다.
- Subcategory folder는 `docs/90.references/data/docker/`처럼 lower-kebab-case를 사용한다.
- SDLC-linked audit and research packs use `docs/90.references/{audits,research}/<date>-<sdlc_key>/`.
- Finalized pack report files use descriptive names and must not retain `part-*.md` prefixes.
- Non-README 문서는 `docs/90.references/data/docker/image-version-interpretation.md`처럼 category 폴더 아래에 둔다.
- `status`는 `draft`, `active`, `archived` 중 하나를 사용한다.
- Archived reference는 현재 판단 기준이 아니라 history/context 보존용으로만 둔다.
- 새 subcategory나 reference를 추가하면 이 README와 해당 top-level/category README를 함께 갱신한다.
- Redirect 파일이나 compatibility shim은 만들지 않는다.

## Placement Rules

| Content | Correct Location |
| --- | --- |
| Audit report, comparison report, audit reference index | `docs/90.references/audits/` |
| Stable background, glossary, profile, inventory | `docs/90.references/data/` |
| Source-backed external research and repo-local analysis pack | `docs/90.references/research/` |
| Learning roadmap and theory reference | `docs/90.references/learning/` |
| LLM navigation map and generated path index | `docs/90.references/llm-wiki/` |
| Architecture requirement | `docs/02.architecture/requirements/` |
| Architecture decision | `docs/02.architecture/decisions/` |
| Technical implementation contract | `docs/03.specs/` |
| Implementation plan or evidence | `docs/04.execution/` |
| Operational policy, guide, or runbook | `docs/05.operations/` |
| Incident packet | `docs/05.operations/incidents/YYYY/INC-###-<title>/` |
| Incident record | `docs/05.operations/incidents/YYYY/INC-###-<title>/INC-###-<title>.md` |
| Postmortem | `docs/05.operations/incidents/YYYY/INC-###-<title>/postmortem.md` |

## Reference Contract

Reference 문서는 active stage의 판단을 돕는 안정적 배경 지식입니다.

| Reference Must Include | Reason                                                             |
| ---------------------- | ------------------------------------------------------------------ |
| Repository role        | 어떤 active doc을 보조하고 무엇을 대체하지 않는지 명확히 하기 위함 |
| Definitions / Facts    | 반복 참조되는 사실을 짧게 고정하기 위함                            |
| Sources                | 외부 또는 repo-local 근거를 추적하기 위함                          |
| Maintenance            | review cadence와 update trigger를 명확히 하기 위함                 |

## Category Language Rules

| Category | Purpose / Role | Language Rule |
| --- | --- | --- |
| `audits/` | Stable audit reports and comparison-analysis references | README는 한국어 기본, audit evidence ID, path, command, provider name 원문 보존 |
| `data/docker/` | Docker image/version drift, registry interpretation, and runtime-reference rules | 한국어 설명 기본, image name/tag, JSON key, Compose path 원문 보존 |
| `data/glossary/` | Stable reference terms and stage-boundary vocabulary | 한국어 정의 기본, canonical stage name과 technical term 원문 보존 |
| `data/governance/` | Governance routing, validation-reference data, and advisory classifier context | README는 한국어 기본, non-README reference 문서는 closed-surface contract에 맞춰 영어 사용 |
| `data/hads/` | HADS profile and validator-backed AI-readable reference boundary | English allowed for HADS block/profile terms; 한국어 explanatory note 가능 |
| `data/knowledge/` | Generated LLM Wiki coverage and knowledge-index reference data | README는 한국어 또는 영어 가능, generated coverage snapshot은 machine-readable English 허용 |
| `data/kubernetes/` | Kubernetes and k3s/k3d migration reference context | 한국어 설명 기본, Kubernetes/k3s/k3d resource term 원문 보존 |
| `learning/` | CS/CE/SE learning roadmap and theory references | 한국어 학습 설명 기본, 논문/책/표준명 원문 보존 |
| `llm-wiki/` | Repo-local LLM navigation map and generated tracked path index | README는 한국어 기본, generated `llm-wiki-index.md`와 machine-readable navigation text는 English 허용 |
| `research/` | Source-backed research packs for cross-cutting engineering topics | README는 한국어 설명 기본, non-README reference 문서는 closed-surface contract에 맞춰 영어 사용; 외부 source title, provider name, standard name, repo-local path 원문 보존 |

정책, runbook, plan, task evidence가 reference 문서 안에서 active 지시처럼 보이면 해당 canonical stage로 분리해야 합니다.

## Current References

- [audits/README.md](./audits/README.md) - stable audit report and comparison-report category
- [audits/2026-07-03-workspace-document-contract-audit-pack/README.md](./audits/2026-07-03-workspace-document-contract-audit-pack/README.md) - workspace document contract audit pack
- [audits/2026-07-04-document-restructure-audit-contract-archive/README.md](./audits/2026-07-04-document-restructure-audit-contract-archive/README.md) - document restructure audit, archive, contract, and QA reference pack
- [audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md](./audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md) - agentic engineering implementation-status audit pack
- [audits/2026-07-05-agentic-engineering-implementation-audit-pack/implementation-overview.md](./audits/2026-07-05-agentic-engineering-implementation-audit-pack/implementation-overview.md) - cross-category implementation-status snapshot
- [audits/2026-07-05-agentic-engineering-implementation-audit-pack/harness-engineering-implementation.md](./audits/2026-07-05-agentic-engineering-implementation-audit-pack/harness-engineering-implementation.md) - harness engineering implementation audit
- [audits/2026-07-05-agentic-engineering-implementation-audit-pack/loop-engineering-implementation.md](./audits/2026-07-05-agentic-engineering-implementation-audit-pack/loop-engineering-implementation.md) - loop engineering implementation audit
- [audits/2026-07-05-agentic-engineering-implementation-audit-pack/provider-harness-loop-implementation.md](./audits/2026-07-05-agentic-engineering-implementation-audit-pack/provider-harness-loop-implementation.md) - Claude, Codex, and Gemini harness/loop implementation audit
- [audits/2026-07-05-agentic-engineering-implementation-audit-pack/workspace-rules-environment-implementation.md](./audits/2026-07-05-agentic-engineering-implementation-audit-pack/workspace-rules-environment-implementation.md) - workspace rules, environment, Docker Compose, and infrastructure implementation audit
- [audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](./audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md) - automation, pipeline, and workflow candidate report
- [audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md](./audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md) - SDLC, CI/CD, QA, formatting, linting, and security quality audit
- [audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md](./audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md) - SSDF, SLSA, and OpenSSF Scorecard security maturity coverage audit
- [data/README.md](./data/README.md) - stable reference data category
- [data/docker/README.md](./data/docker/README.md) - Docker image/version drift, registry, and runtime reference rules
- [data/docker/compose-profile-service-coverage.md](./data/docker/compose-profile-service-coverage.md) - generated Docker Compose profile/service coverage snapshot
- [data/docker/image-version-interpretation.md](./data/docker/image-version-interpretation.md) - Docker image/version source interpretation rules
- [data/glossary/README.md](./data/glossary/README.md) - stable reference terminology category
- [data/glossary/stable-reference-terms.md](./data/glossary/stable-reference-terms.md) - shared terms for reference-stage boundaries
- [data/governance/README.md](./data/governance/README.md) - governance routing reference data category
- [data/governance/agent-output-eval-fixtures.md](./data/governance/agent-output-eval-fixtures.md) - agent-output eval fixture catalog for docs, provider, and infra tasks
- [data/governance/gap-to-stage-routing.md](./data/governance/gap-to-stage-routing.md) - Stage 00 gap-to-stage routing advisory reference
- [data/hads/README.md](./data/hads/README.md) - HADS profile category
- [data/hads/profile.md](./data/hads/profile.md) - HADS profile and validation contract
- [data/knowledge/README.md](./data/knowledge/README.md) - generated LLM Wiki coverage and knowledge-index data category
- [data/knowledge/llm-wiki-stage-category-coverage.md](./data/knowledge/llm-wiki-stage-category-coverage.md) - generated LLM Wiki source-bucket/category coverage snapshot
- [data/kubernetes/README.md](./data/kubernetes/README.md) - Kubernetes and k3s/k3d migration reference context
- [data/kubernetes/docker-compose-to-k3s-migration.md](./data/kubernetes/docker-compose-to-k3s-migration.md) - Docker Compose to k3s/k3d migration suitability snapshot
- [learning/README.md](./learning/README.md) - Docker-based infrastructure learning roadmap and theory references
- [llm-wiki/README.md](./llm-wiki/README.md) - repo-local LLM Wiki entrypoint and tracked-source repository map
- [llm-wiki/repository-map.md](./llm-wiki/repository-map.md) - curated tracked-source repository map
- [llm-wiki/llm-wiki-index.md](./llm-wiki/llm-wiki-index.md) - generated tracked repo-local path index
- [research/README.md](./research/README.md) - source-backed research category
- [research/2026-07-05-agentic-research-pack-refresh/README.md](./research/2026-07-05-agentic-research-pack-refresh/README.md) - harness, loop, provider, SDLC, QA research pack index
- [research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md](./research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md) - workspace purpose, roles, gates, contracts, scripts, governance baseline
- [research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md](./research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md) - harness engineering components and workspace application analysis
- [research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md](./research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md) - agent, eval, CI, human approval loop analysis
- [research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md](./research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md) - spec-driven development and SDLC mapping
- [research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md](./research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md) - CI/CD, QA, formatting, and secure quality gate analysis
- [research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md](./research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md) - Claude, Codex, Gemini provider implementation comparison
- [research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md](./research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md) - external AI agent catalog patterns and repo-local curated catalog import boundary
- [research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md](./research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md) - Docker Compose and infrastructure harness analysis
- [research/2026-07-05-agentic-research-pack-refresh/security-governance.md](./research/2026-07-05-agentic-research-pack-refresh/security-governance.md) - security governance and secure SDLC analysis
- [research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md](./research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md) - automation, pipeline, and workflow analysis

## Stage Handoff

| Direction     | Stage                   | What Is Exchanged                                                              |
| ------------- | ----------------------- | ------------------------------------------------------------------------------ |
| Receives from | `docs/01.requirements/` | Terminology and domain concepts that stabilize into glossary entries           |
| Receives from | `docs/02.architecture/` | Background rationale for decisions that becomes stable reference context       |
| Receives from | `docs/03.specs/`        | Implementation facts that graduate into stable version/standard references     |
| Receives from | `docs/04.execution/`    | Lessons and patterns that stabilize into learning roadmap content              |
| Receives from | `docs/05.operations/`   | Stable operational knowledge that moves from procedure to background reference |
| Provides to   | All active stages       | Stable background context, shared glossary terms, and source-backed facts      |

Reference docs do not gate or block any other stage. They are supplementary, not prerequisite.

## How to Work in This Area

1. Confirm the content is stable reference material, not active policy or procedure.
2. Start new non-README reference docs from [reference.template.md](../99.templates/templates/common/reference.template.md).
3. Choose `audits/`, `data/`, `research/`, or `learning/` before creating a subcategory.
4. Link to authoritative sources and related active-stage documents.
5. Update this README and the affected top-level/category README when adding, moving, or deleting reference docs.
6. Run `bash scripts/validation/check-repo-contracts.sh` after changing reference docs or templates.

## Related Documents

- [docs index](../README.md)
- [audit references](./audits/README.md)
- [reference data](./data/README.md)
- [learning references](./learning/README.md)
- [LLM Wiki references](./llm-wiki/README.md)
- [research references](./research/README.md)
- [glossary references](./data/glossary/README.md)
- [reference template](../99.templates/templates/common/reference.template.md)
- [README template](../99.templates/templates/common/readme.template.md)
- [documentation protocol](../00.agent-governance/rules/documentation-protocol.md)
- [stage authoring matrix](../00.agent-governance/rules/stage-authoring-matrix.md)
