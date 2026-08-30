---
profile_id: research
status: active
artifact_id: RES-0002
artifact_type: research
parent_ids:
  - SPEC-0137
created: 2026-08-28
updated: 2026-08-28
observed_at: 2026-08-28
supersedes:
  - RES-0001
---

# Agentic Engineering Research Pack

> 2026-08-08 기준의 외부 source와 repo-local evidence를 연결하는 비규범적 Stage 90 research map

## Overview

이 pack은 agentic engineering, SDLC, documentation, delivery quality,
verification and validation, infrastructure, security에 관한 20개 leaf를 사람 독자가 탐색하도록 연결합니다.
분석과 adoption boundary를 제공하지만 정책, 승인, 실행 상태, runtime truth를
새로 정의하지 않습니다. 충돌할 때는 이 pack이 아니라 아래 canonical owner를
따릅니다.

- 정책과 agent governance: `docs/00.agent-governance/`
- lifecycle 요구사항: `docs/01.requirements/`; architecture decision과 design:
  `docs/02.architecture/`; implementation contract와 execution evidence:
  `docs/03.specs/`, `docs/04.execution/`; operations: `docs/05.operations/`
- runtime/configuration truth: `infra/`, `scripts/`, provider-native runtime surface
- generated discovery output: `llms.txt`, `docs/90.references/data/0082-llm-wiki-index/`, 그리고 해당
  generator

## Category Role

이 directory는 active lifecycle 문서를 보조하는 source-backed research category이며,
정책이나 실행 evidence의 병렬 authority가 아닙니다.

## Audience

Developers, operators, documentation writers, reviewers, AI agents가 topic과 scope별
canonical evidence owner를 찾을 때 사용합니다.

## Scope

외부 공식 source와 안전한 tracked workspace evidence의 분석, 비교, gap routing은
포함합니다. policy body, secret/private state, runtime 또는 remote 실행 주장,
generated output 수동 편집은 포함하지 않습니다.

## Evidence Classes

| Evidence class      | 이 pack에서의 의미                                                                      | 한계                                                                                  |
| ------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| External fixed      | immutable commit, versioned standard, dated release처럼 다시 식별할 수 있는 자료        | workspace adoption이나 runtime 실행을 증명하지 않음                                   |
| External mutable    | 공식 vendor/product 문서를 retrieval 시점에 확인한 관찰                                 | 날짜 이후 변경될 수 있으므로 재검증 필요                                              |
| Workspace tracked   | pinned commit에서 읽은 tracked source, contract, workflow, test, generated snapshot     | configured 또는 declared 상태이며 실제 실행과 remote enforcement를 자동 증명하지 않음 |
| Runtime or remote   | 실제 provider acceptance, entitlement, deployment, branch protection, live Compose 상태 | 별도 관찰이 없는 항목은 명시적으로 `UNVERIFIED`                                       |
| Historical retained | 이전 pack과 실행 ledger에서 보존한 비교 또는 migration evidence                         | 현재 canonical fact로 승격하지 않음                                                   |

## Structure

이 README가 pack-level human router이며, 아래 20개 topic leaf가 분석 본문을
소유합니다. 별도의 nested policy, plan, runbook, generated artifact는 없습니다.

## Pack Map

### Foundation

| Leaf                                                      | Use it for                                                                                                      |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| [Workspace baseline](./workspace-baseline.md)             | 원래 19개 연구 category와 Task 9a V&V amendment를 포함한 현재 20개 leaf의 tracked baseline, evidence owner, gap |
| [Scope application matrix](./scope-application-matrix.md) | normative 14-scope axis와 각 scope의 adoption disposition                                                       |

### Agentic Engineering

| Leaf                                                                          | Use it for                                                         |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| [Harness engineering](./harness-engineering.md)                               | harness 구성 요소, control plane, enforcement boundary             |
| [Loop engineering](./loop-engineering.md)                                     | feedback loop anatomy, typed loop, stop/retry/evidence boundary    |
| [Provider implementation comparison](./provider-implementation-comparison.md) | Claude/Codex common construction과 provider-native 차이            |
| [Agent instructions and vibe coding](./agent-instructions-vibe-coding.md)     | instruction hierarchy, disciplined prompting, vibe-coding boundary |
| [Provider model landscape](./provider-model-landscape.md)                     | dated provider observations와 fixed local model registry           |
| [Agent model selection](./agent-model-selection.md)                           | task 특성별 model/tier/effort/fallback 선택 규칙                   |
| [AI agent catalogs](./ai-agent-catalogs.md)                                   | local catalog와 immutable external catalog의 import boundary       |
| [Memory hierarchy](./memory-hierarchy.md)                                     | short-term, durable, domain memory와 lifecycle/privacy gaps        |

### SDLC and Documentation

| Leaf                                                            | Use it for                                                             |
| --------------------------------------------------------------- | ---------------------------------------------------------------------- |
| [Spec-driven SDLC](./spec-driven-sdlc.md)                       | lifecycle, gate, traceability, feedback, enforcement layers            |
| [SDLC document roles](./sdlc-document-roles.md)                 | PRD부터 Runbook까지 12개 문서 역할과 금지 대체 관계                    |
| [Document metadata lifecycle](./document-metadata-lifecycle.md) | metadata, state transition, archive, retention ownership               |
| [Documentation architecture](./documentation-architecture.md)   | Diataxis reader modes와 workspace stage architecture의 경계            |
| [LLM Wiki system](./llm-wiki-system.md)                         | authored/generated discovery, safety, freshness, stale-output boundary |

### Delivery and Quality

| Leaf                                                              | Use it for                                                                                                      |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| [Automation pipeline workflow](./automation-pipeline-workflow.md) | local automation topology, GitHub Actions expansion, promotion gaps                                             |
| [Quality, CI, and formatting](./quality-ci-formatting.md)         | formatting/lint/type/test/build/coverage gate와 failure propagation                                             |
| [Verification and validation](./verification-validation.md)       | conformance와 intended use의 구분, evidence state, acceptance authority, residual risk, monitoring/revalidation |

### Infrastructure and Security

| Leaf                                                                    | Use it for                                                           |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------- |
| [Docker Compose and infrastructure](./docker-compose-infrastructure.md) | Compose topology, controls, operations evidence ladder, runtime gaps |
| [Security governance](./security-governance.md)                         | secure SDLC, supply chain, secrets, approval, readiness boundaries   |

## Reading Routes

1. 처음 읽을 때는 [Foundation](#foundation)에서 evidence와 scope 축을 확인한 뒤
   필요한 topic group으로 이동합니다.
2. agent 실행 구조를 분석할 때는 [Agentic Engineering](#agentic-engineering)을
   harness, loop, provider, instruction, model, catalog, memory 순으로 읽습니다.
3. 요구사항에서 장기 운영 문서까지의 chain은
   [SDLC and Documentation](#sdlc-and-documentation)을 읽습니다.
4. workflow, gate, formatting, test, release-readiness evidence는
   [Delivery and Quality](#delivery-and-quality)과
   [Verification and validation](./verification-validation.md)을 함께 읽습니다.
5. Compose/runtime 경계와 secure delivery는
   [Infrastructure and Security](#infrastructure-and-security)를 함께 읽습니다.
6. 특정 workspace scope에 적용할 때는 다음 14-scope route와 foundation의
   normative disposition을 먼저 확인합니다.

## Fourteen-scope Routes

이 표는 topic entry를 고르는 human route입니다. 실제 적용 여부와 owner는
scope matrix와 해당 scope의 canonical contract가 결정합니다.
모든 row의 conformance, intended-use, acceptance, residual-risk 판단은
[Verification and validation](./verification-validation.md)을 cross-cutting route로
함께 사용하며, 이것은 열다섯 번째 scope를 만들지 않습니다.

| Scope          | First pack route                                            | Adoption boundary                                                                   |
| -------------- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `agentic`      | [Agentic Engineering](#agentic-engineering)                 | catalog, harness, loop, instruction, model, memory의 primary analysis scope         |
| `architecture` | [SDLC and Documentation](#sdlc-and-documentation)           | enum 안이지만 agent record 없이 function 2개만 보유; 두 owner 모두 타 scope 소속    |
| `backend`      | [Foundation](#foundation)                                   | enum 밖이며 tracked surface도 없음; backend runtime을 추론하지 않음                 |
| `common`       | [Agentic Engineering](#agentic-engineering)                 | shared policies/functions와 provider projection을 구분                              |
| `docs`         | [SDLC and Documentation](#sdlc-and-documentation)           | lifecycle owner와 reader-mode map을 구분                                            |
| `entry`        | [Infrastructure and Security](#infrastructure-and-security) | entry boundary와 runtime evidence를 구분                                            |
| `frontend`     | [Delivery and Quality](#delivery-and-quality)               | enum 밖이지만 tracked Storybook surface 존재; 일반 product frontend는 추론하지 않음 |
| `infra`        | [Infrastructure and Security](#infrastructure-and-security) | Compose/configured state와 live state를 구분                                        |
| `meta`         | [SDLC and Documentation](#sdlc-and-documentation)           | metadata/discovery layer이며 generated freshness를 추론하지 않음                    |
| `mobile`       | [Foundation](#foundation)                                   | enum 밖이며 tracked surface도 없음; mobile adoption을 추론하지 않음                 |
| `ops`          | [Infrastructure and Security](#infrastructure-and-security) | operations contract, config, runtime evidence를 분리                                |
| `product`      | [SDLC and Documentation](#sdlc-and-documentation)           | requirement/decision ownership은 active lifecycle stage에 유지                      |
| `qa`           | [Delivery and Quality](#delivery-and-quality)               | configured, selected, executed, passed, enforced 상태를 분리                        |
| `security`     | [Infrastructure and Security](#infrastructure-and-security) | secret values와 formal conformance를 이 pack에서 주장하지 않음                      |

## Current State and Gaps

- 이 directory는 이 README와 20개 leaf, 합계 21개 파일로 구성됩니다.
  36개 Spec requirement에는 각각 하나의 canonical destination이 있습니다.
  Task 9의 원래 20-file/19-leaf/35-requirement assembly와 review는 historical
  evidence로 유지되고, REQ-36과 21/20/36 current contract는 Task 9a가 별도
  logical unit으로 구현합니다. REQ-34 route/generated cleanup의 원래 20-file
  결과는 Task 10, REQ-35 final review와 handoff는 Task 12가 소유합니다.
- 14개 normative scope는 모두 disposition을 가집니다. 2026-08-14 재도출은
  reachability를 3분류가 아닌 4분류로 정정했습니다. `agentic`, `common`, `docs`,
  `infra`, `ops`, `qa`, `security`는 enum 안에서 agent와 function record를 모두
  가지고, `architecture`는 enum 안이지만 agent 없이 function 2개만 가지며,
  `entry`, `frontend`, `meta`, `product`는 enum 밖이되 tracked subject surface가
  존재하고, `backend`와 `mobile`만 enum 밖이면서 tracked surface가 없습니다.
  정확한 근거와 per-scope 수치는 [scope matrix](./scope-application-matrix.md)가
  소유합니다.
- provider runtime acceptance와 entitlement, remote GitHub enforcement,
  deployment/live Compose 상태는 검증되지 않았습니다. delivery promotion,
  typed memory lifecycle, catalog reachability, backup/SLO/port ownership에도
  후속 gap이 남습니다.
- Task 10b의 LLM Wiki predecessor는 1,338 index row와 1,337 coverage path에서
  fresh했고, Task 9a는 staged 21번째 leaf를 canonical generator로 반영해
  1,339/1,338 target을 검증합니다. security readiness는 11 implemented, 1 partial,
  1 gap으로 fresh하며 broad dependency SCA가 유일한 gap입니다. 더 오래된 stale/
  fail-closed 결과는 Task의 historical predecessor로 유지됩니다.
- repository contract, metadata, traceability, alignment, generator freshness,
  workflow/security/Compose/provenance 결과는 각 Task command와 candidate에만
  적용됩니다. local PASS를 runtime, remote enforcement, release acceptance로
  확장하지 않습니다.

## Requirement-by-Scope Matrix

This aggregate is a closed relevance index, not an adoption, entitlement,
runtime, or claim-verification assertion. Each `applies` cell means the named
owner's Scope Application table supplies the detailed
condition, verification, and limit for that scope. No additional source or
claim is created by this aggregation.

| Subject / category | Owner leaf | agentic | architecture | common | docs | infra | ops | qa | security |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Workspace measurement | [workspace baseline](./workspace-baseline.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Scope application | [scope application matrix](./scope-application-matrix.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Harness elements | [harness engineering](./harness-engineering.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Workspace harness and loop systems, environment, and rules | [harness engineering](./harness-engineering.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Loop feedback, stopping, and escalation | [loop engineering](./loop-engineering.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Claude implementation | [provider implementation comparison](./provider-implementation-comparison.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Codex implementation | [provider implementation comparison](./provider-implementation-comparison.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Common Claude/Codex environment, rules, and system | [provider implementation comparison](./provider-implementation-comparison.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Instruction context | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Model landscape | [provider model landscape](./provider-model-landscape.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Work-aware model and configuration selection | [agent model selection](./agent-model-selection.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| AI agent catalogs / agency-agents | [AI agent catalogs](./ai-agent-catalogs.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Short-term memory | [memory hierarchy](./memory-hierarchy.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Long-term memory | [memory hierarchy](./memory-hierarchy.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Domain memory | [memory hierarchy](./memory-hierarchy.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Memory management | [memory hierarchy](./memory-hierarchy.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Spec-driven development | [spec-driven SDLC](./spec-driven-sdlc.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| SDLC | [spec-driven SDLC](./spec-driven-sdlc.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| PRD | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Architecture Description | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Local historical ARD | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| ADR role and decision scope | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| ADR lifecycle, status, and supersession | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| ADR relationships | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| SPEC | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| PLAN | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| TASK | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Guide | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Incident | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Postmortem | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Policy | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Release evidence practice | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Runbook | [SDLC document roles](./sdlc-document-roles.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Document metadata and lifecycle | [document metadata lifecycle](./document-metadata-lifecycle.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Diataxis | [documentation architecture](./documentation-architecture.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| C4 Model | [documentation architecture](./documentation-architecture.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| arc42 | [documentation architecture](./documentation-architecture.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Architecture-practice composition | [documentation architecture](./documentation-architecture.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| LLM Wiki | [LLM Wiki system](./llm-wiki-system.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| CI/CD | [automation pipeline workflow](./automation-pipeline-workflow.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| GitHub Actions | [automation pipeline workflow](./automation-pipeline-workflow.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| QA formatting | [quality CI and formatting](./quality-ci-formatting.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| QA linting | [quality CI and formatting](./quality-ci-formatting.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| QA testing | [quality CI and formatting](./quality-ci-formatting.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| QA syntax errors | [quality CI and formatting](./quality-ci-formatting.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Verification | [verification and validation](./verification-validation.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Validation | [verification and validation](./verification-validation.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Docker Compose | [Docker Compose infrastructure](./docker-compose-infrastructure.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Infrastructure | [Docker Compose infrastructure](./docker-compose-infrastructure.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |
| Security | [security governance](./security-governance.md#scope-application) | applies | applies | applies | applies | applies | applies | applies | applies |

The matrix has 50 subject/category rows, eight closed dispositions per row,
and exactly one owner leaf per row. It does not change any leaf's claim state:
the two ADR gaps remain literally `UNVERIFIED`, and DCI feature/OCI/source/
entitlement gaps are not promoted.

## Architecture Practice Delta Claim Index

| Claim ID | Owner leaf | Evidence mode | Source family |
| --- | --- | --- | --- |
| `DOCARCH-C4-001` | `documentation-architecture.md` | source-backed | `https://c4model.com/` |
| `DOCARCH-ARC42-001` | `documentation-architecture.md` | source-backed | `https://arc42.org/` |
| `DOCARCH-COMP-001` | `documentation-architecture.md` | synthesis-only | `—` |
| `SDLCDOC-ADR-001` | `sdlc-document-roles.md` | source-backed | `https://adr.github.io/` |
| `SDLCDOC-ADR-002` | `sdlc-document-roles.md` | source-backed | `https://adr.github.io/` |
| `SDLCDOC-ADR-003` | `sdlc-document-roles.md` | source-backed | `https://adr.github.io/` |
| `SCOPE-COMP-001` | `scope-application-matrix.md` | synthesis-only | `—` |

## Architecture Practice Direct-Page Index

| Page key | Source ID | Claim ID | Family root | Direct URL | Accessed at | State |
| --- | --- | --- | --- | --- | --- | --- |
| `C4-INTRODUCTION` | `DA-SRC-001` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/introduction` | 2026-08-28 | VERIFIED |
| `C4-ABSTRACTIONS` | `DA-SRC-002` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/abstractions` | 2026-08-28 | VERIFIED |
| `C4-DIAGRAMS` | `DA-SRC-003` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/diagrams` | 2026-08-28 | VERIFIED |
| `C4-NOTATION` | `DA-SRC-004` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/diagrams/notation` | 2026-08-28 | VERIFIED |
| `ARC42-OVERVIEW` | `DA-SRC-005` | `DOCARCH-ARC42-001` | `https://arc42.org/` | `https://arc42.org/overview/` | 2026-08-28 | VERIFIED |
| `ADR-ROLE` | `SDR-SRC-001` | `SDLCDOC-ADR-001` | `https://adr.github.io/` | `https://adr.github.io/madr/decisions/0000-use-markdown-architectural-decision-records.html` | 2026-08-28 | VERIFIED |
| `ADR-LIFECYCLE` | `SDR-SRC-002` | `SDLCDOC-ADR-002` | `https://adr.github.io/` | `https://adr.github.io/madr/decisions/0008-add-status-field.html` | 2026-08-28 | UNVERIFIED |
| `ADR-RELATIONSHIPS` | `SDR-SRC-003` | `SDLCDOC-ADR-003` | `https://adr.github.io/` | `https://adr.github.io/madr/` | 2026-08-28 | UNVERIFIED |

## Maintenance and Canonical-owner Boundaries

- 새 사실은 먼저 evidence class, observation date 또는 pinned identity, 그리고
  canonical workspace owner를 기록합니다. mutable external 사실은 다음 변경에서
  다시 확인합니다.
- policy나 procedure가 바뀌면 이 reference에 본문을 복사하지 말고 Stage 00 또는
  active lifecycle owner를 바꾼 뒤 링크와 분석만 조정합니다.
- tracked configuration과 runtime/remote evidence를 합치지 않습니다. 실행하지 않은
  validation은 PASS로 기록하지 않습니다.
- `llms.txt`와 `docs/90.references/data/0082-llm-wiki-index/`는 generator가 소유합니다. 이 pack 또는
  human router 변경만으로 generated artifact를 손으로 고치지 않습니다.
- requirement, source, scope, old-claim migration evidence의 canonical execution
  owner는 [Task ledger](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)입니다.
- V&V source, workspace count, acceptance-authority, monitoring 또는 generated
  path set이 바뀌면 official source를 다시 열고 owner command와 두 LLM Wiki
  freshness gate를 재실행합니다.

## How to Work in This Area

1. 먼저 evidence class와 14-scope disposition을 확인합니다.
2. 변경할 사실의 canonical owner를 다시 읽고 mutable source는 재검증합니다.
3. policy나 procedure 본문을 복사하지 말고 topical leaf의 분석과 링크만 갱신합니다.
4. generated artifact는 해당 generator와 승인된 Task에서만 갱신합니다.
5. metadata, traceability, repository contract, deterministic coverage check를 실행하고
   실패와 `UNVERIFIED` 상태를 그대로 기록합니다.

## Migration State

- 이 2026-08-08 pack은 Task 9부터 agentic-engineering research의 canonical human
  route입니다.
- `2026-07-05-agentic-research-pack-refresh/`는 삭제하거나 수정하지 않았으며
  superseded historical input으로 남아 있습니다. claim-level disposition과
  destination은 Task ledger에 보존됩니다.
- `verification-validation.md`는 old-pack claim predecessor가 없는 REQ-36 신규
  leaf입니다. 이 추가는 retiring pack의 exact 20 files를 바꾸거나 Task 11의
  deletion authority를 넓히지 않습니다.
- parent research README의 human route와 superseded mapping만 이 Task에서
  전환합니다. repository-wide cross-link와 generated machine route는 Task 10,
  old-pack 삭제 gate는 Task 11이 소유합니다.
- 2026-08-11에 별도 source-refresh Task가 20개 leaf를 in-place로 재검증했습니다.
  pack의 21-file/20-leaf 구성, 14-scope 축, 36개 requirement destination은 바뀌지
  않았습니다. refresh evidence는 [Source refresh Task](../../../04.execution/tasks/2026-08-11-agentic-research-pack-source-refresh.md)가
  소유합니다.
- 2026-08-14에 별도 deepening Task가 20개 leaf 전체를 in-place로 심화했습니다.
  외부 source를 다시 조사하고 각 scope의 tracked evidence를 leaf 산문에서
  상속하지 않고 직접 재도출했습니다. pack의 21-file/20-leaf 구성, 14-scope 축,
  36개 requirement destination, leaf `status: draft`는 모두 그대로입니다.
  20개 leaf 전부가 `reviewed_at: 2026-08-14`를 받았으며, deepening evidence와
  재도출 과정에서 확인된 correction은
  [Deepening Task](../../../04.execution/tasks/2026-08-14-agentic-research-pack-deepening.md)가
  소유합니다.
- 2026-08-17에 coverage 감사가 REQ-03의 loop 측 결손 하나를 확인했습니다.
  `harness-engineering.md`는 `### Environment and rules for workspace application`
  섹션을 가지고 있었으나 `loop-engineering.md`에는 대응 섹션이 없어, 해당
  leaf에만 동일 구조의 섹션을 추가했습니다. 추가된 8개 규칙은 모두 그 leaf가
  이미 확립하고 인용한 사실의 재진술이며 새로운 주장이나 canonical owner의
  정책 본문 복사를 포함하지 않습니다. 이 변경으로 `loop-engineering.md`만
  `reviewed_at: 2026-08-17`을 가지고 나머지 19개 leaf는 `2026-08-14`에
  머무릅니다. pack의 21-file/20-leaf 구성, 14-scope 축, 36개 requirement
  destination, leaf `status: draft`는 바뀌지 않았습니다. 증거는
  [Deepening Task](../../../04.execution/tasks/2026-08-14-agentic-research-pack-deepening.md)가
  계속 소유합니다.

## Related Documents

- [Research references](../README.md)
- [Spec 137](../../../03.specs/137-agentic-research-pack-rebuild/spec.md)
- [Implementation Plan](../../../04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
- [Source refresh Task](../../../04.execution/tasks/2026-08-11-agentic-research-pack-source-refresh.md)
- [Deepening Task](../../../04.execution/tasks/2026-08-14-agentic-research-pack-deepening.md)
- [Stage authoring matrix](../../../00.agent-governance/policies/stage-authoring-matrix.md)
- [Documentation protocol](../../../00.agent-governance/policies/documentation-protocol.md)

## Question

This package preserves its existing research evidence under the Stage 99 `research` contract.

## Method

This package preserves its existing research evidence under the Stage 99 `research` contract.

## Findings

This package preserves its existing research evidence under the Stage 99 `research` contract.

### Claim Index

| Claim ID | Owner leaf | State |
| --- | --- | --- |
| `WB-001` | [workspace-baseline](./workspace-baseline.md) | VERIFIED (tracked baseline) |
| `WB-002` | [workspace-baseline](./workspace-baseline.md) | VERIFIED (tracked configuration) |
| `SAM-001` | [scope-application-matrix](./scope-application-matrix.md) | VERIFIED (tracked specification) |
| `SAM-002` | [scope-application-matrix](./scope-application-matrix.md) | VERIFIED (tracked governance routing) |
| `HE-001` | [harness engineering](./harness-engineering.md) | VERIFIED (tracked configuration) |
| `HE-002` | [harness engineering](./harness-engineering.md) | VERIFIED (tracked configuration) |
| `HE-003` | [harness engineering](./harness-engineering.md) | HISTORICAL VERIFIED (retained official observation) |
| `HE-004` | [harness engineering](./harness-engineering.md) | VERIFIED (tracked configuration) |
| `HE-005` | [harness engineering](./harness-engineering.md) | HISTORICAL VERIFIED (retained official observation) |
| `LE-001` | [loop engineering](./loop-engineering.md) | VERIFIED (tracked configuration) |
| `LE-002` | [loop engineering](./loop-engineering.md) | VERIFIED (tracked configuration) |
| `LE-003` | [loop engineering](./loop-engineering.md) | VERIFIED (tracked configuration) |
| `LE-004` | [loop engineering](./loop-engineering.md) | HISTORICAL VERIFIED (retained official observation) |
| `LE-005` | [loop engineering](./loop-engineering.md) | HISTORICAL VERIFIED (retained external study) |
| `PIC-001` | [provider implementation comparison](./provider-implementation-comparison.md) | VERIFIED (tracked configuration) |
| `PIC-002` | [provider implementation comparison](./provider-implementation-comparison.md) | VERIFIED (tracked configuration) |
| `PIC-003` | [provider implementation comparison](./provider-implementation-comparison.md) | VERIFIED (tracked configuration) |
| `PIC-004` | [provider implementation comparison](./provider-implementation-comparison.md) | HISTORICAL VERIFIED (retained official observation) |
| `PIC-005` | [provider implementation comparison](./provider-implementation-comparison.md) | HISTORICAL VERIFIED (retained official observation) |
| `PIC-006` | [provider implementation comparison](./provider-implementation-comparison.md) | HISTORICAL VERIFIED (retained official observation) |
| `PIC-007` | [provider implementation comparison](./provider-implementation-comparison.md) | HISTORICAL VERIFIED (retained official observation) |
| `AIV-001` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) | VERIFIED (tracked configuration) |
| `AIV-002` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) | VERIFIED (tracked configuration) |
| `AIV-003` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) | HISTORICAL VERIFIED (retained official observation) |
| `AIV-004` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) | ADVISORY |
| `AIV-005` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) | HISTORICAL VERIFIED (retained official observation) |
| `PML-001` | [provider model landscape](./provider-model-landscape.md) | VERIFIED (tracked configuration) |
| `PML-002` | [provider model landscape](./provider-model-landscape.md) | HISTORICAL VERIFIED (retained official observation) |
| `PML-003` | [provider model landscape](./provider-model-landscape.md) | UNVERIFIED |
| `PML-004` | [provider model landscape](./provider-model-landscape.md) | ADVISORY |
| `AMS-001` | [agent model selection](./agent-model-selection.md) | VERIFIED (tracked configuration) |
| `AMS-002` | [agent model selection](./agent-model-selection.md) | ADVISORY |
| `AMS-003` | [agent model selection](./agent-model-selection.md) | HISTORICAL VERIFIED (retained official observation) |
| `AMS-004` | [agent model selection](./agent-model-selection.md) | VERIFIED (tracked configuration) |
| `AAC-001` | [AI agent catalogs](./ai-agent-catalogs.md) | HISTORICAL VERIFIED (retained fixed source) |
| `AAC-002` | [AI agent catalogs](./ai-agent-catalogs.md) | HISTORICAL VERIFIED (retained fixed source) |
| `AAC-003` | [AI agent catalogs](./ai-agent-catalogs.md) | HISTORICAL VERIFIED (retained fixed source) |
| `AAC-004` | [AI agent catalogs](./ai-agent-catalogs.md) | VERIFIED (tracked governance) |
| `MH-001` | [memory hierarchy](./memory-hierarchy.md) | HISTORICAL VERIFIED (retained official observation) |
| `MH-002` | [memory hierarchy](./memory-hierarchy.md) | HISTORICAL VERIFIED (retained official observation) |
| `MH-003` | [memory hierarchy](./memory-hierarchy.md) | UNVERIFIED |
| `MH-004` | [memory hierarchy](./memory-hierarchy.md) | ADVISORY |
| `SSD-001` | [spec-driven SDLC](./spec-driven-sdlc.md) | HISTORICAL VERIFIED |
| `SSD-002` | [spec-driven SDLC](./spec-driven-sdlc.md) | HISTORICAL VERIFIED |
| `SSD-003` | [spec-driven SDLC](./spec-driven-sdlc.md) | VERIFIED (tracked configuration) |
| `DML-001` | [document metadata lifecycle](./document-metadata-lifecycle.md) | VERIFIED (tracked configuration) |
| `DML-004` | [document metadata lifecycle](./document-metadata-lifecycle.md) | VERIFIED (tracked configuration) |
| `LWS-001` | [LLM Wiki system](./llm-wiki-system.md) | VERIFIED (tracked configuration) |
| `LWS-003` | [LLM Wiki system](./llm-wiki-system.md) | VERIFIED (tracked configuration) |
| `SSD-004` | [spec-driven SDLC](./spec-driven-sdlc.md) | HISTORICAL VERIFIED |
| `DML-002` | [document metadata lifecycle](./document-metadata-lifecycle.md) | VERIFIED (tracked configuration) |
| `DML-003` | [document metadata lifecycle](./document-metadata-lifecycle.md) | VERIFIED (tracked configuration) |
| `DML-005` | [document metadata lifecycle](./document-metadata-lifecycle.md) | VERIFIED (tracked configuration) |
| `LWS-002` | [LLM Wiki system](./llm-wiki-system.md) | VERIFIED (tracked configuration) |
| `LWS-004` | [LLM Wiki system](./llm-wiki-system.md) | HISTORICAL VERIFIED |
| `SDR-001` | [SDLC document roles](./sdlc-document-roles.md) | VERIFIED (tracked configuration) |
| `SDR-002` | [SDLC document roles](./sdlc-document-roles.md) | VERIFIED (tracked configuration) |
| `SDR-003` | [SDLC document roles](./sdlc-document-roles.md) | VERIFIED (tracked + historical retained source) |
| `SDR-004` | [SDLC document roles](./sdlc-document-roles.md) | HISTORICAL VERIFIED |
| `SDR-005` | [SDLC document roles](./sdlc-document-roles.md) | VERIFIED (tracked configuration) |
| `SDR-006` | [SDLC document roles](./sdlc-document-roles.md) | HISTORICAL VERIFIED |
| `DOCARCH-DIATAXIS-BASE-001` | [documentation architecture](./documentation-architecture.md) | HISTORICAL VERIFIED |
| `SCOPE-COMP-001` | [scope application matrix](./scope-application-matrix.md) | ADVISORY |
| `DOCARCH-C4-001` | [documentation architecture](./documentation-architecture.md) | VERIFIED |
| `DOCARCH-ARC42-001` | [documentation architecture](./documentation-architecture.md) | VERIFIED |
| `DOCARCH-COMP-001` | [documentation architecture](./documentation-architecture.md) | ADVISORY |
| `SDLCDOC-ADR-001` | [SDLC document roles](./sdlc-document-roles.md) | VERIFIED |
| `SDLCDOC-ADR-002` | [SDLC document roles](./sdlc-document-roles.md) | UNVERIFIED |
| `SDLCDOC-ADR-003` | [SDLC document roles](./sdlc-document-roles.md) | UNVERIFIED |
| `APW-001` | [automation pipeline workflow](./automation-pipeline-workflow.md) | VERIFIED (tracked configuration) |
| `APW-002` | [automation pipeline workflow](./automation-pipeline-workflow.md) | VERIFIED (tracked configuration) |
| `APW-003` | [automation pipeline workflow](./automation-pipeline-workflow.md) | HISTORICAL VERIFIED (retained official observation) |
| `QCF-001` | [quality CI and formatting](./quality-ci-formatting.md) | VERIFIED (tracked configuration) |
| `QCF-002` | [quality CI and formatting](./quality-ci-formatting.md) | VERIFIED (tracked configuration) |
| `QCF-003` | [quality CI and formatting](./quality-ci-formatting.md) | HISTORICAL VERIFIED (retained official observation) |
| `VV-001` | [verification and validation](./verification-validation.md) | VERIFIED (tracked configuration) |
| `VV-002` | [verification and validation](./verification-validation.md) | HISTORICAL VERIFIED (retained official observation) |
| `VV-003` | [verification and validation](./verification-validation.md) | VERIFIED (tracked governance) |
| `DCI-001` | [Docker Compose infrastructure](./docker-compose-infrastructure.md) | VERIFIED (tracked configuration) |
| `DCI-002` | [Docker Compose infrastructure](./docker-compose-infrastructure.md) | HISTORICAL VERIFIED (retained official observation) |
| `DCI-003` | [Docker Compose infrastructure](./docker-compose-infrastructure.md) | UNVERIFIED |
| `SG-001` | [security governance](./security-governance.md) | HISTORICAL VERIFIED (retained official observation) |
| `SG-002` | [security governance](./security-governance.md) | HISTORICAL VERIFIED (retained official observation) |
| `SG-003` | [security governance](./security-governance.md) | HISTORICAL VERIFIED (retained official observation) |
| `SG-004` | [security governance](./security-governance.md) | VERIFIED (tracked configuration) |

## Sources

This package preserves its existing research evidence under the Stage 99 `research` contract.

### Source Index

| Source ID | Owner leaf |
| --- | --- |
| `WB-SRC-001` | [workspace-baseline](./workspace-baseline.md) |
| `WB-SRC-002` | [workspace-baseline](./workspace-baseline.md) |
| `WB-SRC-003` | [workspace-baseline](./workspace-baseline.md) |
| `SAM-SRC-001` | [scope-application-matrix](./scope-application-matrix.md) |
| `SAM-SRC-002` | [scope-application-matrix](./scope-application-matrix.md) |
| `HE-SRC-001` | [harness engineering](./harness-engineering.md) |
| `HE-SRC-002` | [harness engineering](./harness-engineering.md) |
| `HE-SRC-003` | [harness engineering](./harness-engineering.md) |
| `HE-SRC-004` | [harness engineering](./harness-engineering.md) |
| `HE-SRC-005` | [harness engineering](./harness-engineering.md) |
| `HE-SRC-006` | [harness engineering](./harness-engineering.md) |
| `HE-SRC-007` | [harness engineering](./harness-engineering.md) |
| `LE-SRC-001` | [loop engineering](./loop-engineering.md) |
| `LE-SRC-002` | [loop engineering](./loop-engineering.md) |
| `LE-SRC-003` | [loop engineering](./loop-engineering.md) |
| `LE-SRC-004` | [loop engineering](./loop-engineering.md) |
| `PIC-SRC-001` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `PIC-SRC-002` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `PIC-SRC-003` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `PIC-SRC-004` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `PIC-SRC-005` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `PIC-SRC-006` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `PIC-SRC-007` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `PIC-SRC-008` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `PIC-SRC-009` | [provider implementation comparison](./provider-implementation-comparison.md) |
| `AIV-SRC-001` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) |
| `AIV-SRC-002` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) |
| `AIV-SRC-003` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) |
| `AIV-SRC-004` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) |
| `AIV-SRC-005` | [agent instructions and bounded generated work](./agent-instructions-vibe-coding.md) |
| `PML-SRC-001` | [provider model landscape](./provider-model-landscape.md) |
| `PML-SRC-002` | [provider model landscape](./provider-model-landscape.md) |
| `PML-SRC-003` | [provider model landscape](./provider-model-landscape.md) |
| `PML-SRC-004` | [provider model landscape](./provider-model-landscape.md) |
| `PML-SRC-005` | [provider model landscape](./provider-model-landscape.md) |
| `AMS-SRC-001` | [agent model selection](./agent-model-selection.md) |
| `AMS-SRC-002` | [agent model selection](./agent-model-selection.md) |
| `AMS-SRC-003` | [agent model selection](./agent-model-selection.md) |
| `AAC-SRC-001` | [AI agent catalogs](./ai-agent-catalogs.md) |
| `AAC-SRC-002` | [AI agent catalogs](./ai-agent-catalogs.md) |
| `AAC-SRC-003` | [AI agent catalogs](./ai-agent-catalogs.md) |
| `AAC-SRC-004` | [AI agent catalogs](./ai-agent-catalogs.md) |
| `MH-SRC-001` | [memory hierarchy](./memory-hierarchy.md) |
| `MH-SRC-002` | [memory hierarchy](./memory-hierarchy.md) |
| `MH-SRC-003` | [memory hierarchy](./memory-hierarchy.md) |
| `SSD-SRC-001` | [spec-driven SDLC](./spec-driven-sdlc.md) |
| `SSD-SRC-002` | [spec-driven SDLC](./spec-driven-sdlc.md) |
| `SSD-SRC-003` | [spec-driven SDLC](./spec-driven-sdlc.md) |
| `SSD-SRC-004` | [spec-driven SDLC](./spec-driven-sdlc.md) |
| `DML-SRC-001` | [document metadata lifecycle](./document-metadata-lifecycle.md) |
| `DML-SRC-002` | [document metadata lifecycle](./document-metadata-lifecycle.md) |
| `LWS-SRC-001` | [LLM Wiki system](./llm-wiki-system.md) |
| `LWS-SRC-002` | [LLM Wiki system](./llm-wiki-system.md) |
| `LWS-SRC-003` | [LLM Wiki system](./llm-wiki-system.md) |
| `DA-SRC-001` | [documentation architecture](./documentation-architecture.md) |
| `DA-SRC-002` | [documentation architecture](./documentation-architecture.md) |
| `DA-SRC-003` | [documentation architecture](./documentation-architecture.md) |
| `DA-SRC-004` | [documentation architecture](./documentation-architecture.md) |
| `DA-SRC-005` | [documentation architecture](./documentation-architecture.md) |
| `DA-SRC-006` | [documentation architecture](./documentation-architecture.md) |
| `SDR-SRC-001` | [SDLC document roles](./sdlc-document-roles.md) |
| `SDR-SRC-002` | [SDLC document roles](./sdlc-document-roles.md) |
| `SDR-SRC-003` | [SDLC document roles](./sdlc-document-roles.md) |
| `SDR-SRC-004` | [SDLC document roles](./sdlc-document-roles.md) |
| `SDR-SRC-005` | [SDLC document roles](./sdlc-document-roles.md) |
| `SDR-SRC-006` | [SDLC document roles](./sdlc-document-roles.md) |
| `SDR-SRC-007` | [SDLC document roles](./sdlc-document-roles.md) |
| `SDR-SRC-008` | [SDLC document roles](./sdlc-document-roles.md) |
| `APW-SRC-001` | [automation pipeline workflow](./automation-pipeline-workflow.md) |
| `APW-SRC-002` | [automation pipeline workflow](./automation-pipeline-workflow.md) |
| `APW-SRC-003` | [automation pipeline workflow](./automation-pipeline-workflow.md) |
| `APW-SRC-004` | [automation pipeline workflow](./automation-pipeline-workflow.md) |
| `APW-SRC-005` | [automation pipeline workflow](./automation-pipeline-workflow.md) |
| `QCF-SRC-001` | [quality CI and formatting](./quality-ci-formatting.md) |
| `QCF-SRC-002` | [quality CI and formatting](./quality-ci-formatting.md) |
| `QCF-SRC-003` | [quality CI and formatting](./quality-ci-formatting.md) |
| `QCF-SRC-004` | [quality CI and formatting](./quality-ci-formatting.md) |
| `QCF-SRC-005` | [quality CI and formatting](./quality-ci-formatting.md) |
| `VV-SRC-001` | [verification and validation](./verification-validation.md) |
| `VV-SRC-002` | [verification and validation](./verification-validation.md) |
| `VV-SRC-003` | [verification and validation](./verification-validation.md) |
| `DCI-SRC-001` | [Docker Compose infrastructure](./docker-compose-infrastructure.md) |
| `DCI-SRC-002` | [Docker Compose infrastructure](./docker-compose-infrastructure.md) |
| `DCI-SRC-003` | [Docker Compose infrastructure](./docker-compose-infrastructure.md) |
| `DCI-SRC-004` | [Docker Compose infrastructure](./docker-compose-infrastructure.md) |
| `SG-SRC-001` | [security governance](./security-governance.md) |
| `SG-SRC-002` | [security governance](./security-governance.md) |
| `SG-SRC-003` | [security governance](./security-governance.md) |
| `SG-SRC-004` | [security governance](./security-governance.md) |
| `SG-SRC-005` | [security governance](./security-governance.md) |
| `SG-SRC-006` | [security governance](./security-governance.md) |
| `SG-SRC-007` | [security governance](./security-governance.md) |
| `SG-SRC-008` | [security governance](./security-governance.md) |
| `SG-SRC-009` | [security governance](./security-governance.md) |

## Implications

This package preserves its existing research evidence under the Stage 99 `research` contract.

## Traceability

This package preserves its existing research evidence under the Stage 99 `research` contract.
