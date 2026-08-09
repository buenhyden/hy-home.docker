---
status: active
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
- generated discovery output: `llms.txt`, `docs/90.references/llm-wiki/`, 그리고 해당
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

| Evidence class | 이 pack에서의 의미 | 한계 |
| --- | --- | --- |
| External fixed | immutable commit, versioned standard, dated release처럼 다시 식별할 수 있는 자료 | workspace adoption이나 runtime 실행을 증명하지 않음 |
| External mutable | 공식 vendor/product 문서를 retrieval 시점에 확인한 관찰 | 날짜 이후 변경될 수 있으므로 재검증 필요 |
| Workspace tracked | pinned commit에서 읽은 tracked source, contract, workflow, test, generated snapshot | configured 또는 declared 상태이며 실제 실행과 remote enforcement를 자동 증명하지 않음 |
| Runtime or remote | 실제 provider acceptance, entitlement, deployment, branch protection, live Compose 상태 | 별도 관찰이 없는 항목은 명시적으로 `UNVERIFIED` |
| Historical retained | 이전 pack과 실행 ledger에서 보존한 비교 또는 migration evidence | 현재 canonical fact로 승격하지 않음 |

## Structure

이 README가 pack-level human router이며, 아래 20개 topic leaf가 분석 본문을
소유합니다. 별도의 nested policy, plan, runbook, generated artifact는 없습니다.

## Pack Map

### Foundation

| Leaf | Use it for |
| --- | --- |
| [Workspace baseline](./workspace-baseline.md) | 원래 19개 연구 category와 Task 9a V&V amendment를 포함한 현재 20개 leaf의 tracked baseline, evidence owner, gap |
| [Scope application matrix](./scope-application-matrix.md) | normative 14-scope axis와 각 scope의 adoption disposition |

### Agentic Engineering

| Leaf | Use it for |
| --- | --- |
| [Harness engineering](./harness-engineering.md) | harness 구성 요소, control plane, enforcement boundary |
| [Loop engineering](./loop-engineering.md) | feedback loop anatomy, typed loop, stop/retry/evidence boundary |
| [Provider implementation comparison](./provider-implementation-comparison.md) | Claude/Codex common construction과 provider-native 차이 |
| [Agent instructions and vibe coding](./agent-instructions-vibe-coding.md) | instruction hierarchy, disciplined prompting, vibe-coding boundary |
| [Provider model landscape](./provider-model-landscape.md) | dated provider observations와 fixed local model registry |
| [Agent model selection](./agent-model-selection.md) | task 특성별 model/tier/effort/fallback 선택 규칙 |
| [AI agent catalogs](./ai-agent-catalogs.md) | local catalog와 immutable external catalog의 import boundary |
| [Memory hierarchy](./memory-hierarchy.md) | short-term, durable, domain memory와 lifecycle/privacy gaps |

### SDLC and Documentation

| Leaf | Use it for |
| --- | --- |
| [Spec-driven SDLC](./spec-driven-sdlc.md) | lifecycle, gate, traceability, feedback, enforcement layers |
| [SDLC document roles](./sdlc-document-roles.md) | PRD부터 Runbook까지 12개 문서 역할과 금지 대체 관계 |
| [Document metadata lifecycle](./document-metadata-lifecycle.md) | metadata, state transition, archive, retention ownership |
| [Documentation architecture](./documentation-architecture.md) | Diataxis reader modes와 workspace stage architecture의 경계 |
| [LLM Wiki system](./llm-wiki-system.md) | authored/generated discovery, safety, freshness, stale-output boundary |

### Delivery and Quality

| Leaf | Use it for |
| --- | --- |
| [Automation pipeline workflow](./automation-pipeline-workflow.md) | local automation topology, GitHub Actions expansion, promotion gaps |
| [Quality, CI, and formatting](./quality-ci-formatting.md) | formatting/lint/type/test/build/coverage gate와 failure propagation |
| [Verification and validation](./verification-validation.md) | conformance와 intended use의 구분, evidence state, acceptance authority, residual risk, monitoring/revalidation |

### Infrastructure and Security

| Leaf | Use it for |
| --- | --- |
| [Docker Compose and infrastructure](./docker-compose-infrastructure.md) | Compose topology, controls, operations evidence ladder, runtime gaps |
| [Security governance](./security-governance.md) | secure SDLC, supply chain, secrets, approval, readiness boundaries |

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

| Scope | First pack route | Adoption boundary |
| --- | --- | --- |
| `agentic` | [Agentic Engineering](#agentic-engineering) | catalog, harness, loop, instruction, model, memory의 primary analysis scope |
| `architecture` | [SDLC and Documentation](#sdlc-and-documentation) | enum-only scope이며 현재 concrete catalog adoption을 추론하지 않음 |
| `backend` | [Foundation](#foundation) | explicit no-current-profile disposition; backend runtime을 추론하지 않음 |
| `common` | [Agentic Engineering](#agentic-engineering) | shared policies/functions와 provider projection을 구분 |
| `docs` | [SDLC and Documentation](#sdlc-and-documentation) | lifecycle owner와 reader-mode map을 구분 |
| `entry` | [Infrastructure and Security](#infrastructure-and-security) | entry boundary와 runtime evidence를 구분 |
| `frontend` | [Delivery and Quality](#delivery-and-quality) | explicit no-current-profile disposition; UI implementation을 추론하지 않음 |
| `infra` | [Infrastructure and Security](#infrastructure-and-security) | Compose/configured state와 live state를 구분 |
| `meta` | [SDLC and Documentation](#sdlc-and-documentation) | metadata/discovery layer이며 generated freshness를 추론하지 않음 |
| `mobile` | [Foundation](#foundation) | explicit no-current-profile disposition; mobile adoption을 추론하지 않음 |
| `ops` | [Infrastructure and Security](#infrastructure-and-security) | operations contract, config, runtime evidence를 분리 |
| `product` | [SDLC and Documentation](#sdlc-and-documentation) | requirement/decision ownership은 active lifecycle stage에 유지 |
| `qa` | [Delivery and Quality](#delivery-and-quality) | configured, selected, executed, passed, enforced 상태를 분리 |
| `security` | [Infrastructure and Security](#infrastructure-and-security) | secret values와 formal conformance를 이 pack에서 주장하지 않음 |

## Current State and Gaps

- 이 directory는 이 README와 20개 leaf, 합계 21개 파일로 구성됩니다.
  36개 Spec requirement에는 각각 하나의 canonical destination이 있습니다.
  Task 9의 원래 20-file/19-leaf/35-requirement assembly와 review는 historical
  evidence로 유지되고, REQ-36과 21/20/36 current contract는 Task 9a가 별도
  logical unit으로 구현합니다. REQ-34 route/generated cleanup의 원래 20-file
  결과는 Task 10, REQ-35 final review와 handoff는 Task 12가 소유합니다.
- 14개 normative scope는 모두 disposition을 가집니다. `architecture`는
  enum-only이고 `backend`, `docs`, `entry`, `frontend`, `meta`, `mobile`은
  catalog enum 밖의 명시적 scope입니다.
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

## Maintenance and Canonical-owner Boundaries

- 새 사실은 먼저 evidence class, observation date 또는 pinned identity, 그리고
  canonical workspace owner를 기록합니다. mutable external 사실은 다음 변경에서
  다시 확인합니다.
- policy나 procedure가 바뀌면 이 reference에 본문을 복사하지 말고 Stage 00 또는
  active lifecycle owner를 바꾼 뒤 링크와 분석만 조정합니다.
- tracked configuration과 runtime/remote evidence를 합치지 않습니다. 실행하지 않은
  validation은 PASS로 기록하지 않습니다.
- `llms.txt`와 `docs/90.references/llm-wiki/`는 generator가 소유합니다. 이 pack 또는
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

## Related Documents

- [Research references](../README.md)
- [Spec 137](../../../03.specs/137-agentic-research-pack-rebuild/spec.md)
- [Implementation Plan](../../../04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
