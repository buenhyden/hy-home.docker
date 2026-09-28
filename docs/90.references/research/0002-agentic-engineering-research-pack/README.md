---
title: "Agentic Engineering Research Pack"
version: "2.4.2"
type: "reference/research-pack"
status: "published"
owner: "@buenhyden"
updated: "2026-09-27"
layer: "references"
artifact_id: "RES-0002"
parent_ids:
- "SPEC-0158"
created: "2026-08-28"
observed_at: "2026-09-05"
---

# Agentic Engineering Research Pack

## Question

공식 외부 자료에 근거해 agent engineering, SDLC, 문서화, Compose, CI/CD,
품질과 보안의 선택지를 어떻게 구분하고, 후속 내부 조사에 필요한 질문과
수용 증거를 어떻게 준비할 것인가?

이번 결과는 비규범적 연구다. 상세 주장은 기존 멤버 한 곳이 소유하며 이
README는 범위, 통합 결정, 탐색과 추적성을 제공한다.

## Scope

| 구분 | 이번 기록 |
| --- | --- |
| `repository_baseline` | `f30b168e2fbb0959e4a31749935568fd5b3942f1`; 2026-09-27 fetch한 `origin/main`과 일치 |
| `external_sources_checked_at` | 2026-09-27; 원문별 실제 확인 기록은 멤버의 source/claim 표 |
| `document_updated_at` | 2026-09-27 |
| `historical_workspace_observation` | 기존 관측의 원래 날짜·커밋·범위 유지; frontmatter `observed_at`은 2026-09-05 역사 관측 |
| 내부 적용 상태 | `Not assessed in this run` |

포함 범위는 외부 근거 갱신, 중복된 현재 설명의 통합, 역사 증거 보존, 후속 질문,
문서 검증과 로컬 커밋이다. 구현·운영·계정·보안의 신규 감사, 서비스 집계,
실제 계정·비용, 환경변수·비밀값·원시 로그 조사는 제외했다. 연구를 근거로 한
설정·정책 변경, 배포·재시작·push·PR·merge도 수행 범위가 아니다.

## Method

질문, 증거 모델, 수명주기/관측 시점, 활용 목적이 모두 같을 때 현재 설명을
동일 주장으로 통합한다. 외부 제품 사양과 과거 내부 실행 결과는 합치지 않는다.
공식 상세 문서·원본 저장소·표준·원저자 자료를 직접 확인하고 사실과 해석·권고를
구분한다. 검색 요약만으로 기능을 단정하지 않는다.

| 대상 | 결정 | 이유와 소유자 |
| --- | --- | --- |
| RES-0002 | 유지·갱신·현재 내용 재구성 | 이번 신규 결과의 유일한 상위 팩 |
| m0001–m0019 | 갱신·동일 현재 주장 통합 | 아래 대표 멤버가 본문 소유; 과거 관측은 별도 보존 |
| m0020 | 역사 자료 보존 | baseline 날짜·커밋·판정을 현재 값으로 바꾸지 않음 |
| m0021 | 역사 보존·외부 선택 원칙 보완 | 서비스별 관측·승인 유지; 신규 유지/삭제 평가 없음 |
| RES-0084 | 보존 | 고유 Actions·Hosted/remote 관측 유지; 이번 외부 Actions 갱신은 m0004 |
| RES-0085 | 보존 | 날짜가 있는 baseline·identity-recovery 증거 유지 |
| RES-0096 | 범위 외·참조 유지 | 별도 archive-domain 질문과 증거; 재감사하지 않음 |
| 신규 팩/멤버·이동·삭제 | 수행하지 않음 | 기존 소유자와 평면 경로로 충분함 |

출처 ID는 동일 원문을 추적하는 라벨이고 claim ID는 멤버의 주장 라벨이다.
주요 주장에는 상세 위치, 발행/수정일(없으면 미표시), 실제 확인일, 제품·버전·채널,
사실/해석/권고, 한계·충돌·재확인 조건을 붙인다. 제품 지원과 계정 entitlement,
API 요금과 구독 CLI quota를 구분한다. 찾지 못한 기능은 미지원으로 추론하지 않는다.

### Preservation Declaration

SPEC-0158의 보호 대상과 기존 식별자를 유지한다. 고유 관측·출처·승인 이력은
삭제하지 않으며 역사 구역은 당시 의미로만 읽는다. 기존 보호 집합을 바꾸지 않고
선언을 Method 아래에 배치한다.

- `README.md`
- `m0001-agent-instructions-vibe-coding.md`
- `m0002-agent-model-selection.md`
- `m0003-ai-agent-catalogs.md`
- `m0004-automation-pipeline-workflow.md`
- `m0005-docker-compose-infrastructure.md`
- `m0006-document-metadata-lifecycle.md`
- `m0007-documentation-architecture.md`
- `m0008-harness-engineering.md`
- `m0009-llm-wiki-system.md`
- `m0010-loop-engineering.md`
- `m0011-memory-hierarchy.md`
- `m0012-provider-implementation-comparison.md`
- `m0013-provider-model-landscape.md`
- `m0014-quality-ci-formatting.md`
- `m0015-scope-application-matrix.md`
- `m0016-sdlc-document-roles.md`
- `m0017-security-governance.md`
- `m0018-spec-driven-sdlc.md`
- `m0019-verification-validation.md`
- `m0020-workspace-baseline.md`
- `m0021-local-docker-service-consolidation.md`

## Findings

### Request Coverage and Member Navigation

이번 요청 A–L의 다대일 매핑이다. 모든 현재 내부 적용 상태는
`Not assessed in this run`이다. 상세 분석과 비교는 대표 절이 소유한다.

| 요청 | 주제 | 대표 멤버 | 세부 범위 |
| --- | --- | --- | --- |
| A | Harness와 bounded loop | [m0008](m0008-harness-engineering.md#current-external-research), [m0010](m0010-loop-engineering.md#current-external-research) | instruction/tools/environment/sandbox/context/memory/skill/orchestration/관측/평가/복구; goal/state/plan/act/observe/verify/review/stop/handoff, budget/retry/checkpoint/멱등성/병렬 충돌 |
| B | 공통 거버넌스와 instruction | [m0001](m0001-agent-instructions-vibe-coding.md#current-external-research), [m0012](m0012-provider-implementation-comparison.md#current-external-research) | 정책/역할/절차/도구/스타일, 계층/충돌/명시적 로딩/신뢰, 스택/coding standard, 공통 원본/native adapter |
| C | Agent catalog·모델·비용 | [m0003](m0003-ai-agent-catalogs.md#current-external-research), [m0002](m0002-agent-model-selection.md#current-external-research), [m0013](m0013-provider-model-landscape.md#current-external-research) | 형식/배포/변환/license/pinning/권한/평가; 작업별 effort/fallback/지연/token/context/compaction/cache/rate/동시성/예산 |
| D | 기억·LLM Wiki·handoff | [m0011](m0011-memory-hierarchy.md#current-external-research), [m0009](m0009-llm-wiki-system.md#current-external-research), [m0012](m0012-provider-implementation-comparison.md#current-external-research) | 단기/장기/영역별 기억과 승인 증거; 승격/검색/요약/만료/삭제/오염; ingest/query/lint/RAG/llms.txt 차이; 최소 handoff |
| E | SDD·SDLC·개발 문서 | [m0018](m0018-spec-driven-sdlc.md#current-external-research), [m0016](m0016-sdlc-document-roles.md#current-external-research), [m0006](m0006-document-metadata-lifecycle.md#current-external-research) | PRD/Requirement/SPEC/PLAN/TASK/ADR 책임/입출력/소유/검토/수명주기/내용/관계/변경/분할/보존; 요구→수용과 작업→운영 |
| F | 운영 문서 | [m0016](m0016-sdlc-document-roles.md#current-external-research) | Guide/Incident/Postmortem/Policy/Release/Runbook 독자/목적/트리거/소유/필수항목/상태/검토/개정/보존/관계; 안전 중단/복구/action 추적 |
| G | 문서화·탐색 | [m0007](m0007-documentation-architecture.md#current-external-research), [m0006](m0006-document-metadata-lifecycle.md#current-external-research) | Diátaxis 독자 필요, C4 수준/동적/배포, arc42 품질/위험, ADR 결정/supersession, README 역할과 중복 방지 |
| H | Compose·Infrastructure | [m0005](m0005-docker-compose-infrastructure.md#current-external-research), [m0021](m0021-local-docker-service-consolidation.md#current-external-research) | 사양/CLI/include/merge/extends/profile/interpolation/project/dependency/health/network/ports/volume/config/secret/resources/stop/restart/provenance; TLS/DNS/관측/복구/업데이트/license/중복/부담 |
| I | CI/CD·Actions | [m0004](m0004-automation-pipeline-workflow.md#current-external-research) | test/build/package/publish/deploy/promotion/rollback; workflow/job/step/event/filter/reuse/matrix/concurrency/cache/artifact/required checks/environment/OIDC/pinning/untrusted PR/runner |
| J | QA·Verification/Validation | [m0014](m0014-quality-ci-formatting.md#current-external-research), [m0019](m0019-verification-validation.md#current-external-research) | format/lint/syntax/schema/static/unit/integration/contract/E2E/문서/보안/flaky/fixture/mutation/coverage; 적합성과 의도한 사용/수용/독립 검토 |
| K | Security | [m0017](m0017-security-governance.md#current-external-research) | SSDF/공급망/SBOM/provenance/signature/취약점/least privilege/sandbox/secret/pinning/예외/위험/감사; agent/MCP/plugin/hook/injection/유출/기억 오염/socket/mount/privileged/network/runner |
| L | Editor·hooks·project tracking | [m0004](m0004-automation-pipeline-workflow.md#current-external-research), [m0014](m0014-quality-ci-formatting.md#current-external-research), [m0018](m0018-spec-driven-sdlc.md#current-external-research) | provider/Git/editor/CI 주체; commit message/inline edit/documentation/test hook/재검토/우회/network; GitHub/Linear/Jira/Markdown hierarchy/deps/roadmap/workflow/automation/권한/Git/API/MCP/export/부담 |

적용 수준과 관심 영역의 교차 매핑, 후보 표면의 확인 여부, 후속 질문의 증거·검사
방법·합격/실패·권한·소유 역할은 [m0015](m0015-scope-application-matrix.md#future-internal-checks)가
통합 안내한다. [m0020](m0020-workspace-baseline.md)은 과거 내부 baseline의 보존 위치다.

### Synthesis

instruction과 역할 설명은 권한이나 sandbox enforcement의 증거가 아니다.
외부 제품 지원, 계정 이용 권한, 로컬 채택과 실행 결과도 별개의 주장이다.
문서 형식 검사, 정적 Compose 검증, Hosted CI, 실제 사용자 목적과 복구 성공은
서로 대체할 수 없는 증거다. 이는 연결된 멤버들의 출처를 종합한 연구자의
해석이며 새 정책이나 내부 평가 결과가 아니다.

### Historical workspace observations — not reassessed in this refresh

아래 기록은 이전 관찰의 한국어 보존본입니다. 현재 주장이나 새 승인으로 읽지 않으며, 현재 외부 연구는 위의 갱신된 member 탐색을 따릅니다.

현재 routing(2026-09-06): [공통 Agent 거버넌스](../../../../.agents/README.md)와
[ADR-0032](../../../02.architecture/decisions/0032-canonical-agent-governance-home.md)가
활성 source 위치를 소유합니다. 아래의 이전 Stage 00 경로, inventory,
provider 투영, check 결과는 날짜가 있는 관찰로 남으며 현재 지시나 새
runtime 수용 증거가 아닙니다. Source 링크는 이제 현재 owner로
연결되며 원래의 `observed_at`, `reviewed_at`, status, 측정된 사실은
그대로 보존됩니다.

#### Historical question

모든 claim에 canonical owner 하나와 명시적인 증거 깊이가 있도록,
이 저장소는 agentic workspace, spec-driven SDLC, operations corpus,
documentation architecture, Compose platform, quality 체계, 보안 통제를
어떻게 구조화해야 하는가?

세부 질문은 다음과 같습니다:

1. 어떤 provider-neutral 행동이 공통 Agent 거버넌스에 속하고, 어떤 Claude
   또는 Codex 행동이 native adapter의 관심사로 남아야 하는가?
2. instruction, model routing, catalog, loop, memory, handoff, hook,
   context, cost, editor 통합은 어떻게 관리되고 검증되어야 하는가?
3. Requirement, Architecture/ADR, Spec, Plan, Task, Operations, Stage 90
   증거는 소유권, lifecycle, 대체 규칙에서 어떻게 다른가?
4. 어떤 Diátaxis, C4, arc42, ADR, README, 생성된 navigation 관행이
   병렬 권위를 만들지 않으면서 발견 가능성을 높이는가?
5. 추적되는 Compose, CI/CD, QA, 검증, 보안 surface는 무엇을 증명하며
   무엇이 여전히 runtime, provider, remote 관찰을 필요로 하는가?

이 package는 gap을 찾고 권고를 route할 수 있습니다. 현재 owner를
대신해 정책, 구현, provider entitlement, deployment, release, 잔여
위험을 승인할 수 없습니다.

이 package는 현재 주제 연구와 cross-package routing의 canonical hub입니다.
관련된 Stage 90 package는 의도적으로 별도 증거 owner로 유지됩니다:

- [RES-0084](../0084-github-actions-platform/README.md)는 세부 GitHub
   Actions platform mechanics와 날짜가 있는 Hosted/remote 증거를
   소유합니다.
- [RES-0085](../0085-workspace-engineering-main-baseline-assessment/README.md)는
   날짜가 있는 baseline 범위와 identity-recovery carrier를 보존합니다;
   현재 baseline 해석은 [m0020](m0020-workspace-baseline.md)이
   소유합니다.
- [RES-0096](../0096-archive-disposition-consistency/README.md)은
   archive-domain consistency 평가와 그 SPEC-0177/SPEC-0178 증거를
   소유합니다.

통합은 소유권과 routing으로 이루어지며 날짜가 있는 증거를 복사하거나
평탄화하거나 삭제하지 않습니다. 새 현재 finding은 이 package 아래 소유
구성원을 갱신해야 하며 전문적이고 역사적이며 archive-domain인 finding은
기존 package에 남습니다.

#### Historical scope

> Historical evidence (not current authority; source: Git history): 문서 관찰 baseline 시점에 기록된 source 경로.
>
> - Repository: `buenhyden/hy-home.docker`.
> - 비교 branch와 commit: `main`의
>   `71da6654e2fa3def174b238ad309c92fe46e9dae`. 이전에 평가한 baseline인
>   `4c6d211129615eab372d720ebd209b6c27618c86`는 날짜가 있는 구성원
>   재검증과 RES-0085에 그대로 보존되며 현재 상태로 다시 쓰지 않습니다.
> - Repository 관찰 날짜와 외부 source 확인 날짜:
>   2026-09-05.
> - 관찰 checkout 범위: `main`만 있는 격리된 clone과, merge되지 않은
>   local branch를 담은 개발자 clone. 둘은 같은 commit의 등록된 check
>   하나에서 결과가 다르므로, 둘 중 하나를 저장소의 최종 판정으로
>   내세우지 않고 두 결과를 모두 기록합니다.
> - 포함: `docs/00.agent-governance/`, Stage 01, 02, 03, 05, 90, 98, 99;
>   root entrypoint; `.agents/`, `.claude/`, `.codex/`, workflow, Compose
>   선언, script, test, 생성된 navigation 소유권.
> - 포함된 외부 계열: 공식 Claude Code, OpenAI Codex, GitHub,
>   Docker, MCP, Diátaxis, C4, arc42, GitHub Spec Kit, ISO 공개 정의,
>   NIST SSDF, SLSA, upstream agency-agents 자료.
> - 제외: secret이나 credential 값, user-global provider 설정,
>   shell history, raw log, 승인되지 않은 provider/runtime 변경, 새 실서비스
>   배포, tag, release.
> - 증거 경계: 설정은 실행이 아님; local 실행은 Hosted CI가 아님; Hosted
>   CI는 배포가 아님; 특정 시점의 entitlement는 미래를 보장하지 않음;
>   추적되는 protection 의도는 remote 강제가 아님.
> - [m0020](m0020-workspace-baseline.md)이 현재 저장소-local baseline을
>   소유합니다. [RES-0085](../0085-workspace-engineering-main-baseline-assessment/README.md)는
>   날짜가 있는 2026-09-05 평가 범위와 identity 복구 증거를 보존합니다.
>   [RES-0084](../0084-github-actions-platform/README.md)는 GitHub Actions
>   platform 메커니즘의 세부 사항을 소유합니다. 이 package는 주제별 연구와
>   그 cross-category navigation을 소유합니다.

#### Historical method

1. 무언가를 발급하거나 재구성하기 전에, 모든 활성 research package와
   구성원을 경로, 제목, `artifact_id`, `parent_ids`, lifecycle metadata,
   heading, 링크, 관찰 날짜로 열거합니다.
2. 요청된 용어, 동의어, 약어, 오래된 Stage 04 route, 구식 개수, 중복된
   claim, 상충하는 증거, `UNVERIFIED` 경계를 파일명과 본문에서 검색합니다.
3. Stage 90 산문에서 저장소 사실을 상속받는 대신, 현재 canonical
   Requirement, Architecture/ADR, Spec/Task, Operations, audit, data,
   Registry, template, validator, workflow, 생성된 산출물 owner를
   읽습니다.
4. 가변적인 외부 claim은 2026-09-05에 공식 primary source에서 다시
   엽니다. 이전의 고정 commit이나 날짜가 있는 관찰은 역사적 증거로
   유지하고 새로고침되지 않은 claim은 그렇게 표시합니다.
5. 채택을 Defined, Configured, Local-executed, Repository-enforced,
   Runtime-verified, Remote-verified, Unverified로 분류합니다.
6. 중복을 같은 question, 증거 모델, lifecycle, decision route로
   취급합니다. 그 owner를 제자리에서 갱신하고 넷 모두 실질적으로 다를
   때만 package를 만듭니다.
7. 집중된 document/reference check, 생성된 index 신선도, 링크와 lifecycle
   check를 실행한 뒤 canonical full gate를 실행합니다. local, Hosted,
   provider, runtime, remote 결과는 별도 증거 행으로 남깁니다.

##### Historical existing artifact decision record

| Existing artifact | Related requested categories | Current problem | Decision | Target artifact |
| --- | --- | --- | --- | --- |
| RES-0002 README | A–G navigation과 cross-category 요약 | 세부 claim, source, 역사적 routing이 구성원 내용과 중복됨 | question/scope/method/router/traceability owner로 다시 씀 | RES-0002 README, 같은 identity |
| RES-0002-m0001–m0020 | 모든 주제 범주 | 역사적 분석은 강하지만 관찰 metadata와 여러 현재 route가 오래됨 | ID와 내용은 보존하고 현재 재검증 증거를 추가 | 같은 구성원 20개 |
| RES-0084 | GitHub Actions, CI, remote enforcement | platform 분석이 aggregate-check 도입 이전 것 | 채택과 증거 경계를 제자리에서 갱신 | RES-0084 |
| RES-0085 | 현재 `main` baseline | 그 question이 m0020이 이미 소유한 current-baseline 목적과 중복됨 | 현재 소유권을 m0020으로 통합하고 RES-0085는 `review` 상태의 날짜가 있는 복구 증거로 보존 | RES-0002-m0020과 RES-0085 증거 |
| New RES-0096 candidate | 같은 question 집합 | 기존 owner와 관찰 주기를 중복함 | 만들지 않음 | 없음 |

##### Historical 2026-09-05 baseline decision record

이 pass는 `main@71da6654e2fa3def174b238ad309c92fe46e9dae`에서 같은 question
집합을 다시 관찰했고 구조적 변화는 없었습니다. 요청된 모든 범주가 이미
정확히 하나의 소유 구성원으로 해결되었으므로, package identity, 구성원
identity, `created` 값, 아래 구성원 배정은 바뀌지 않습니다.

| Existing artifact | Related requested categories | Current problem | Decision | Target artifact |
| --- | --- | --- | --- | --- |
| RES-0002 README | A–G navigation | Scope가 `main`보다 세 commit 뒤처진 baseline을 인용 | 현재 baseline pointer를 진전시키고 날짜가 있는 것은 보존 | RES-0002 README, 같은 identity |
| RES-0002-m0006 | B12, D10, D11 | `SPEC-0173`의 identity-space 증거가 기록되지 않음 | SPEC-0172 작업이 진행 중인 동안 구성원은 건드리지 않고 검증 owner와 함께 관찰을 기록 | RES-0002-m0019 |
| RES-0002-m0014 | F1–F13 | 인용된 gate 판정이 checkout identity를 담지 않음 | 날짜가 있는 재현 조건을 추가하고 분석을 m0019로 route | RES-0002-m0014 |
| RES-0002-m0019 | F14–F18 | checkout 간 검증 결정성이 분석되지 않음 | 세 환경 비교를 canonical 분석으로 추가 | RES-0002-m0019 |
| RES-0002-m0020 | A3, A20 | 현재 baseline pointer가 delta보다 뒤처짐 | pointer를 진전시키고 delta 효과를 기록 | RES-0002-m0020 |
| RES-0002-m0001–m0005, m0007–m0013, m0015–m0018 | 나머지 범주 | delta에서 owner가 바뀌지 않음 | 그대로 보존; 재관찰 없이 날짜를 다시 매기지 않음 | 같은 구성원 |
| RES-0084 | E7, E9 | 그 날짜가 있는 관찰은 이 delta 밖에 있음 | 바꾸지 않음 | RES-0084 |
| RES-0085 | 날짜가 있는 request 범위 | `4c6d2111` 인용이 그 존재 목적 | 갱신하지 않음; 날짜가 있는 baseline을 보존하는 것이 존재 이유 | RES-0085 |
| New research package candidate | 같은 question 집합 | 이미 존재하는 owner를 중복함 | 만들지 않음 | 없음 |

실질적인 추가 사항은 한 가지입니다. local gate 판정이 checkout에 따라
달라집니다: 이 단일 commit에서 격리된 `main` 전용 clone은 전체
profile을 통과하고 merge되지 않은 branch에 닿을 수 있는 개발자
clone은 실패합니다. 두 결과 모두 기록됩니다. 이 관찰이 건드리는 저장소
계약은 Stage 00과 Stage 99에 속하므로, 후속 작업은 이 package가 아니라
일반적인 Requirement-to-Task chain으로 진행됩니다.

#### Historical findings

##### Historical member navigation

<!-- Historical evidence table (not current authority; source: Git history). -->
| Category | Member | Core question | Repository state | Evidence depth | Priority |
| --- | --- | --- | --- | --- | --- |
| Instructions and prompt hierarchy | [m0001](m0001-agent-instructions-vibe-coding.md) | How are durable instructions separated from ad-hoc prompts? | Root adapters load Stage 00; hooks enforce selected boundaries | Defined, Configured, Repository-enforced | High |
| Model routing | [m0002](m0002-agent-model-selection.md) | How should task class select provider/model/effort? | Work profiles are registered; quality/cost effectiveness is unmeasured | Configured, Repository-enforced, Unverified effectiveness | High |
| Agent catalogs | [m0003](m0003-ai-agent-catalogs.md) | How are external roles admitted without copying authority? | 14 roles and 23 skills are canonical; external catalogs are research inputs | Repository-enforced | Medium |
| Automation and delivery | [m0004](m0004-automation-pipeline-workflow.md) | Where do hooks, CI, CD, promotion, and rollback differ? | CI aggregate gates exist; live deployment remains unverified | Configured, Repository-enforced, Hosted-executed | High |
| Compose infrastructure | [m0005](m0005-docker-compose-infrastructure.md) | What do profiles and service controls prove? | 28 selections render; four domain defects remain owner-routed | Configured, Local-executed, Repository-enforced | High |
| Metadata and lifecycle | [m0006](m0006-document-metadata-lifecycle.md) | How are identity, status, retention, and retirement enforced? | Common-six and profile lifecycle contracts are active | Repository-enforced | High |
| Documentation architecture | [m0007](m0007-documentation-architecture.md) | How should Diátaxis, C4, arc42, ADR, and README compose? | Selective composition exists; no parallel taxonomy is required | Defined, Configured | Medium |
| Harness engineering | [m0008](m0008-harness-engineering.md) | Which controls make agents effective and bounded? | Canonical roles/skills/adapters/hooks are enforced; outcomes are partly observed | Repository-enforced, Runtime-verified in bounded probes | High |
| LLM Wiki | [m0009](m0009-llm-wiki-system.md) | How can generated navigation remain non-authoritative and fresh? | Generator ownership and freshness checks are active | Repository-enforced | Medium |
| Loop engineering | [m0010](m0010-loop-engineering.md) | How are discovery, retry, stop, review, and handoff bounded? | Stage 00 defines the loop; live provider equivalence is unverified | Defined, Repository-enforced | High |
| Memory | [m0011](m0011-memory-hierarchy.md) | What is durable, what expires, and who may delete it? | Task evidence exists; durable semantic memory lifecycle remains partial | Defined, Configured, Unverified | High |
| Provider comparison | [m0012](m0012-provider-implementation-comparison.md) | What is shared and what must stay Claude/Codex-native? | Shared control plane projects into native surfaces | Repository-enforced, point-in-time Runtime-verified | High |
| Provider/model landscape | [m0013](m0013-provider-model-landscape.md) | Which model, effort, fallback, entitlement, and cost claims are supportable? | Registry is configured; entitlement is dated and cost is unmeasured | Configured, point-in-time Runtime-verified | High |
| Quality and CI | [m0014](m0014-quality-ci-formatting.md) | Which quality layers block drift? | Registered local/full and Hosted aggregate gates exist | Local-executed, Repository-enforced, Hosted-executed | High |
| Scope application | [m0015](m0015-scope-application-matrix.md) | Where does every requested concern apply and who owns it? | All requested categories route to existing owners | Defined | Medium |
| SDLC document roles | [m0016](m0016-sdlc-document-roles.md) | What does each artifact own and never replace? | Registered roles and operations composition are enforced | Repository-enforced | High |
| Security | [m0017](m0017-security-governance.md) | Which controls are local, remote, runtime, or missing? | Static and supply-chain controls are strong; production posture is unverified | Repository-enforced, point-in-time Remote-verified | High |
| Spec-driven SDLC | [m0018](m0018-spec-driven-sdlc.md) | How does intent flow into verified work? | Current package form is enforced; intended-use acceptance remains owner-bound | Repository-enforced | High |
| Verification and validation | [m0019](m0019-verification-validation.md) | Does evidence prove conformance and intended use? | Conformance gates exist; deployment acceptance is absent | Local-executed, Repository-enforced | High |
| Workspace baseline | [m0020](m0020-workspace-baseline.md) | What is actually present at the repository boundary? | Current baseline and dated measurements are consolidated here; RES-0085 preserves recovery evidence | Configured, Local-executed | High |
| Local Docker service consolidation | [m0021](m0021-local-docker-service-consolidation.md) | Which local services are open source, overlapping, or safe removal candidates? | Current Compose/runtime inventory and official project sources compared; removal decisions remain user- and data-dependent | Local-executed, External-source-reviewed | High |

##### Historical requested category routing

`Current status`와 `Principal gap`은 이 관찰 시점의 평가입니다. `Evidence
depth`는 Method에서 정의한 통제 어휘(Defined, Configured, Local-executed,
Repository-enforced, Runtime-verified, Remote-verified, Unverified)를
그대로 사용합니다.

| Requested category | Owning member | Current status | Evidence depth | Principal gap |
| --- | --- | --- | --- | --- |
| A1 Harness engineering | [m0008](m0008-harness-engineering.md) | 부분적 | Repository-enforced | 결과 지표 없음 |
| A2 Loop engineering | [m0010](m0010-loop-engineering.md) | 부분적 | Repository-enforced | provider 간 결과 동등성 미검증 |
| A3 Workspace harness, loop, rules, environment | [m0020](m0020-workspace-baseline.md) | 부분적 | Configured, Local-executed | editor/runtime 수용 불완전 |
| A4 Claude Code implementation | [m0012](m0012-provider-implementation-comparison.md) | 채택됨 | Configured, point-in-time Runtime-verified | 전체 native event coverage 부분적 |
| A5 Codex implementation | [m0012](m0012-provider-implementation-comparison.md) | 채택됨 | Configured, point-in-time Runtime-verified | native hook surface가 더 작음 |
| A6 Shared Claude/Codex governance | [m0012](m0012-provider-implementation-comparison.md) | 구현됨 | Repository-enforced | 행동 동등성 미검증 |
| A7 Provider-native differences | [m0012](m0012-provider-implementation-comparison.md) | 문서화됨 | Defined, Configured | upstream capability가 가변적 |
| A8 System prompt and command hierarchy | [m0001](m0001-agent-instructions-vibe-coding.md) | 구현됨 | Repository-enforced | provider system prompt는 여전히 외부에 있음 |
| A9 Context loading and priority | [m0001](m0001-agent-instructions-vibe-coding.md) | 구현됨 | Defined, Configured | runtime 준수는 확률적임 |
| A10 Task-aware model selection | [m0002](m0002-agent-model-selection.md) | 정책으로 구현됨 | Repository-enforced | 결과 검증 없음 |
| A11 Model, effort, fallback, entitlement | [m0013](m0013-provider-model-landscape.md) | 부분적 | Configured, point-in-time Runtime-verified | 현재 entitlement/fallback 보장되지 않음 |
| A12 Agent catalog and agency-agents | [m0003](m0003-ai-agent-catalogs.md) | 부분적 | Repository-enforced | 자동 외부 intake 없음 |
| A13 Roles, capabilities, tools, permissions | [m0003](m0003-ai-agent-catalogs.md) | 구조적으로 구현됨 | Repository-enforced | runtime least-privilege 증명 부분적 |
| A14 Agent memory hierarchy | [m0011](m0011-memory-hierarchy.md) | 부분적 | Defined, Configured | 단일 내구성 semantic-memory 권위 없음 |
| A15 Short-, long-, domain-memory | [m0011](m0011-memory-hierarchy.md) | 부분적 | Defined | long/domain lifecycle 불완전 |
| A16 Memory promotion, retention, expiry, privacy, deletion | [m0011](m0011-memory-hierarchy.md) | 격차 | Defined | 강제되는 lifecycle 없음 |
| A17 Claude/Codex context sharing | [m0012](m0012-provider-implementation-comparison.md) | 구조적으로만 | Configured | 의미적 전달 수용 미검증 |
| A18 Session handoff and evidence sharing | [m0012](m0012-provider-implementation-comparison.md) | 부분적 | Defined, Repository-enforced | live handoff 품질 미측정 |
| A19 Test and CI agent hooks | [m0004](m0004-automation-pipeline-workflow.md) | 부분적 | Configured, Repository-enforced | native parity가 다름 |
| A20 Editor shortcuts, tasks, code actions | [m0020](m0020-workspace-baseline.md) | 격차 | Unverified | 저장소 전체 계약 없음 |
| A21 Rate limit, cost, token, context management | [m0013](m0013-provider-model-landscape.md) | 부분적 | Configured | 직접적인 cost/rate 증거 없음 |
| B1 Spec-driven development | [m0018](m0018-spec-driven-sdlc.md) | 구현됨 | Repository-enforced | intended-use 수용은 owner-bound |
| B2 SDLC purpose and necessity | [m0018](m0018-spec-driven-sdlc.md) | 정의됨 | Defined | 효과성 지표 없음 |
| B3 SDLC governance | [m0018](m0018-spec-driven-sdlc.md) | 구현됨 | Repository-enforced | 등록된 범위에는 없음 |
| B4 Full SDLC lifecycle | [m0018](m0018-spec-driven-sdlc.md) | 구조적으로 구현됨 | Repository-enforced | deployment/release 완료는 조건부 |
| B5 Requirement-to-operations traceability | [m0016](m0016-sdlc-document-roles.md) | 구조적으로 구현됨 | Repository-enforced | runtime 증거는 별도로 남음 |
| B6 PRD | [m0016](m0016-sdlc-document-roles.md) | 등록된 관점 | Repository-enforced | 독립 package type 아님 |
| B7 SPEC | [m0016](m0016-sdlc-document-roles.md) | 등록됨 | Repository-enforced | 현재 형태에는 없음 |
| B8 PLAN | [m0016](m0016-sdlc-document-roles.md) | 등록됨 | Repository-enforced | 반드시 prospective로 남아야 함 |
| B9 TASK | [m0016](m0016-sdlc-document-roles.md) | 등록됨 | Repository-enforced | 반드시 증거 중심으로 남아야 함 |
| B10 ADR | [m0016](m0016-sdlc-document-roles.md) | 등록됨 | Repository-enforced | decision 품질은 reviewer-bound |
| B11 Ownership and non-substitution | [m0016](m0016-sdlc-document-roles.md) | 구현됨 | Repository-enforced | 등록된 role에는 없음 |
| B12 State transition, completion, supersession, retention, retirement | [m0006](m0006-document-metadata-lifecycle.md) | 구현됨 | Repository-enforced | 역사적 기록은 별도로 남음 |
| B13 Approval, review, independent-review boundary | [m0018](m0018-spec-driven-sdlc.md) | 구현됨 | Defined, Repository-enforced | 사람의 수용은 owner-bound로 남음 |
| C1 Guide | [m0016](m0016-sdlc-document-roles.md) | 등록됨 | Repository-enforced | subject coverage가 다름 |
| C2 Incident | [m0016](m0016-sdlc-document-roles.md) | 등록됨 | Repository-enforced | 사건 발생 시에만 생성 |
| C3 Postmortem | [m0016](m0016-sdlc-document-roles.md) | 등록됨 | Repository-enforced | 해결된 incident 증거 필요 |
| C4 Policy | [m0016](m0016-sdlc-document-roles.md) | 등록됨 | Repository-enforced | subject coverage가 다름 |
| C5 Release | [m0016](m0016-sdlc-document-roles.md) | 구성된 증거 | Defined | 독립 profile 없음 |
| C6 Runbook | [m0016](m0016-sdlc-document-roles.md) | 등록됨 | Repository-enforced | runtime 리허설이 다름 |
| C7 Operations-document relationships | [m0016](m0016-sdlc-document-roles.md) | 구현됨 | Repository-enforced | 등록된 topology에는 없음 |
| C8 Release evidence vs deployment evidence | [m0016](m0016-sdlc-document-roles.md) | 정의됨 | Defined | 현재 release target 없음 |
| C9 Incident, recovery, postmortem, improvement traceability | [m0016](m0016-sdlc-document-roles.md) | 구조적으로 구현됨 | Repository-enforced | live incident는 사건 의존적 |
| D1 Diátaxis | [m0007](m0007-documentation-architecture.md) | 선택적으로 적용됨 | Defined, Configured | 전체 corpus 분류 불필요 |
| D2 C4 Model | [m0007](m0007-documentation-architecture.md) | 부분적 | Defined | view coverage는 수요 기반 |
| D3 arc42 | [m0007](m0007-documentation-architecture.md) | 부분적 | Defined | 병렬 폴더 분류 아님 |
| D4 ADR operating model | [m0016](m0016-sdlc-document-roles.md) | 구현됨 | Repository-enforced | 검토 품질은 여전히 사람에게 있음 |
| D5 LLM Wiki | [m0009](m0009-llm-wiki-system.md) | 구현됨 | Repository-enforced | Graphify snapshot은 advisory/오래됨으로 남음 |
| D6 Generated index vs authored-document boundary | [m0009](m0009-llm-wiki-system.md) | 구현됨 | Repository-enforced | 생성 파일은 owner command 필요 |
| D7 README purpose and role | [m0007](m0007-documentation-architecture.md) | 구현됨 | Repository-enforced | legacy 산문은 여전히 낡을 수 있음 |
| D8 Repository/stage/package/service README differences | [m0007](m0007-documentation-architecture.md) | 구현됨 | Repository-enforced | service coverage가 다름 |
| D9 Documentation navigation | [m0007](m0007-documentation-architecture.md) | 구현됨 | Configured, Repository-enforced | graph noise는 advisory로 남음 |
| D10 Duplication prevention and canonical ownership | [m0006](m0006-document-metadata-lifecycle.md) | 구조적으로 구현됨 | Repository-enforced | 의미적 중복은 여전히 검토 필요 |
| D11 Metadata and document lifecycle | [m0006](m0006-document-metadata-lifecycle.md) | 구현됨 | Repository-enforced | 활성 등록 corpus에는 없음 |
| E1 Docker Compose | [m0005](m0005-docker-compose-infrastructure.md) | statically 구현됨 | Configured, Local-executed | live service 수용 없음 |
| E2 Service boundaries and profiles | [m0005](m0005-docker-compose-infrastructure.md) | 알려진 결함과 함께 구현됨 | Repository-enforced | AUD-0097이 아직 열려 있음 |
| E3 Network, volume, secret, healthcheck | [m0005](m0005-docker-compose-infrastructure.md) | 부분적 | Configured, Repository-enforced | runtime 행동 미검증 |
| E4 Configuration vs runtime state | [m0005](m0005-docker-compose-infrastructure.md) | 명시적으로 분리됨 | Defined | 새 runtime 관찰 없음 |
| E5 Continuous Integration | [m0004](m0004-automation-pipeline-workflow.md) | 구현됨 | Repository-enforced, Hosted-executed | point-in-time Hosted 증거 |
| E6 Continuous Delivery/Deployment | [m0004](m0004-automation-pipeline-workflow.md) | 부분적/격차 | Defined | live target이나 promotion 수용 없음 |
| E7 GitHub Actions | [m0004](m0004-automation-pipeline-workflow.md) | CI에는 구현됨 | Configured, Hosted-executed | 세부는 RES-0084 참고 |
| E8 Promotion, release, deployment, rollback | [m0004](m0004-automation-pipeline-workflow.md) | 부분적 | Defined, Configured rehearsal | 현재 production target/version 없음 |
| E9 Remote control plane and branch protection | [m0004](m0004-automation-pipeline-workflow.md) | cutoff 시점 검증됨 | Remote-verified | 이후 drift는 새 read-back 필요 |
| E10 Operational readiness and recoverability | [m0005](m0005-docker-compose-infrastructure.md) | 부분적 | Repository-enforced | owner-routed 결함 넷, live 리허설 없음 |
| F1 Quality Assurance | [m0014](m0014-quality-ci-formatting.md) | 구조적으로 구현됨 | Repository-enforced | intended-use 수용은 별도 |
| F2 Formatting | [m0014](m0014-quality-ci-formatting.md) | 구현됨 | Repository-enforced | 도구 버전 drift는 모니터링됨 |
| F3 Linting | [m0014](m0014-quality-ci-formatting.md) | 구현됨 | Repository-enforced | surface별 coverage |
| F4 Syntax validation | [m0014](m0014-quality-ci-formatting.md) | 구현됨 | Repository-enforced | runtime semantics는 별도 |
| F5 Static analysis | [m0014](m0014-quality-ci-formatting.md) | 구현됨 | Repository-enforced, Hosted-executed | remote configuration은 drift 가능 |
| F6 Unit test | [m0014](m0014-quality-ci-formatting.md) | 구현됨 | Repository-enforced | domain별 coverage가 다름 |
| F7 Integration test | [m0014](m0014-quality-ci-formatting.md) | 부분적 | Repository-enforced | live 외부 통합 제한적 |
| F8 Contract test | [m0014](m0014-quality-ci-formatting.md) | 강하게 구현됨 | Repository-enforced | runtime 계약은 별도로 남음 |
| F9 Regression test | [m0014](m0014-quality-ci-formatting.md) | 구현됨 | Repository-enforced | 역사적 gap별 coverage |
| F10 Coverage | [m0014](m0014-quality-ci-formatting.md) | 부분적 | Storybook에는 Hosted-executed | 저장소 전체 threshold 없음 |
| F11 Pre-commit hook | [m0014](m0014-quality-ci-formatting.md) | 구현됨 | Configured, CI에는 Repository-enforced | local 설치는 사용자 의존적 |
| F12 Local validation | [m0014](m0014-quality-ci-formatting.md) | 구현됨 | Local-executed | point-in-time 결과 |
| F13 CI quality gate | [m0014](m0014-quality-ci-formatting.md) | 구현됨 | Repository-enforced, Hosted-executed | Hosted 미래 실행은 달라질 수 있음 |
| F14 Verification | [m0019](m0019-verification-validation.md) | 구현됨 | Repository-enforced | 증거는 artifact별로 남음 |
| F15 Validation | [m0019](m0019-verification-validation.md) | 부분적 | Defined | intended-use owner 증거가 다름 |
| F16 Intended-use acceptance | [m0019](m0019-verification-validation.md) | 부분적 | deployment에는 Unverified | 정확한 target 없음 |
| F17 Residual risk | [m0019](m0019-verification-validation.md) | owner-bound | Defined | 보편적 수용 권위 없음 |
| F18 Revalidation and monitoring | [m0019](m0019-verification-validation.md) | 부분적 | Configured | 가변적 외부/runtime 상태 |
| G1 Security governance | [m0017](m0017-security-governance.md) | 구조적으로 구현됨 | Repository-enforced | production 수용 없음 |
| G2 Secret and credential handling | [m0017](m0017-security-governance.md) | 경계로 구현됨 | Defined, Repository-enforced | secret store는 조사되지 않음 |
| G3 Least privilege | [m0017](m0017-security-governance.md) | 부분적 | Configured, Repository-enforced | runtime identity 증명이 다름 |
| G4 Supply-chain security | [m0017](m0017-security-governance.md) | 등록된 sample에는 구현됨 | Repository-enforced | 전체 service fleet provenance 없음 |
| G5 Dependency analysis | [m0017](m0017-security-governance.md) | 부분적 | Repository-enforced | ecosystem 범위가 다름 |
| G6 Code/infrastructure static analysis | [m0017](m0017-security-governance.md) | 구현됨 | Repository-enforced, Hosted-executed | runtime finding은 별도 |
| G7 Approval boundaries | [m0017](m0017-security-governance.md) | 구현됨 | Defined, Repository-enforced | provider enforcement가 다름 |
| G8 Audit evidence | [m0017](m0017-security-governance.md) | 구조적으로 구현됨 | Repository-enforced | live platform audit log는 조사되지 않음 |
| G9 Local security validation vs remote enforcement | [m0017](m0017-security-governance.md) | 명시적으로 분리됨 | Local-executed, cutoff 시점 Remote-verified | 이후 drift 가능 |
| G10 Runtime security state | [m0017](m0017-security-governance.md) | Unverified | Unverified | live deployment 관찰 없음 |
| G11 Security readiness and gaps | [m0017](m0017-security-governance.md) | 부분적 | Defined, Repository-enforced | AUD-0097과 production posture가 남음 |

빠진 요청 범주는 없습니다. 이전 연구 대비 바뀐 주요 결론은 통합된
문서 계약 lifecycle/common-six corpus, m0020으로의 현재 baseline
소유권 통합(RES-0085는 날짜가 있는 복구 증거를 보존), 두 aggregate CI
route 모두의 Hosted 수용, 2026-09-05 remote protection read-back입니다.
이 변화로 저장소 증거는 강화되지만 live deployment, 영구 memory,
editor 통합, 비용, provider 결과 gap은 닫히지 않습니다.

#### Historical sources

2026-09-05에 다시 연 공통 공식 source:

- [Claude Code feature model](https://code.claude.com/docs/en/features-overview),
  [hooks](https://code.claude.com/docs/en/hooks),
  [subagents](https://code.claude.com/docs/en/sub-agents),
  [memory](https://code.claude.com/docs/en/memory).
- [OpenAI Codex app architecture](https://openai.com/index/introducing-the-codex-app/),
  [Codex safety controls](https://openai.com/index/running-codex-safely/),
  [harness engineering](https://openai.com/index/harness-engineering/).
- [Model Context Protocol architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture).
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use),
  [OIDC](https://docs.github.com/en/actions/reference/security/oidc),
  [ruleset status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
- [Docker Compose specification](https://docs.docker.com/compose/compose-file/),
  [services and healthchecks](https://docs.docker.com/reference/compose-file/services/),
  [profiles](https://docs.docker.com/compose/how-tos/profiles/),
  [secrets](https://docs.docker.com/reference/compose-file/secrets/).
- [Diátaxis](https://diataxis.fr/), [C4 Model](https://c4model.com/),
  [arc42 documentation](https://arc42.org/documentation/).
- [GitHub Spec Kit](https://github.github.com/spec-kit/),
  [ISO 29148 public terminology](https://www.iso.org/obp/ui/#iso:std:iso-iec-ieee:29148:ed-2:v1:en),
  [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final),
  [SLSA 1.2](https://slsa.dev/spec/v1.2/).
- [agency-agents division authority](https://github.com/msitarzewski/agency-agents/blob/main/divisions.json).

저장소 source:

- Baseline commit `71da6654e2fa3def174b238ad309c92fe46e9dae`, 이전에
  평가된 baseline `4c6d211129615eab372d720ebd209b6c27618c86`는 날짜가
  있는 증거로 보존됨.
- [공통 거버넌스](../../../../.agents/README.md),
  [Stage 99 Registry](../../../99.templates/registry.json),
  [Stage 03](../../../03.specs/README.md),
  [Stage 05](../../../05.operations/README.md).
- [Workflow contract](../../../../.github/workflow-contract.yml),
  [CI workflow](../../../../.github/workflows/ci-quality.yml),
  [main protection record](../../../../.github/rulesets/main-protection.md).
- [Implementation audits](../../audits/README.md), Compose profile data,
  LLM Wiki index, repository map.

각 구성원이 세부 claim과 source inventory를 소유합니다. 이
package 수준 목록은 범주 전반에 공유되는 source만 담습니다.

#### Historical implications

1. 공통 Agent 거버넌스를 provider-neutral 정책으로, Stage 99를 문서 계약
   권위로 보존합니다; Stage 90 finding을 어느 쪽으로도 승격하지
   않습니다.
2. 20개 구성원의 주제별 분할을 유지합니다. 경쟁 package를 추가하거나
   README가 세부 분석을 반복하게 만들지 않으면서 전체 요청을
   매핑합니다.
3. 현재 read-back이 일치하는 동안 두 aggregate CI check와 그 app
   binding을 보존합니다. 불일치 시 기록된 12-check rollback을
   사용합니다.
4. 내구성 있는 memory lifecycle, editor task/action, cost/rate 증거,
   넓은 supply-chain provenance, Compose 결함 종료, production
   deployment/release 수용은 별도의 승인된 SDLC 작업을 통해 route
   합니다.
5. Diátaxis, C4, arc42를 기존 owner 안의 독자/viewpoint 도구로
   적용합니다; 두 번째 문서 tree를 도입하지 않습니다.
6. 모든 권고를 다음 route에 유지합니다:
   Research → Requirement → Architecture/ADR → Spec → Plan → Task →
   Verification → Independent Review.

#### Historical traceability

- 구성원: [m0001](m0001-agent-instructions-vibe-coding.md),
  [m0002](m0002-agent-model-selection.md),
  [m0003](m0003-ai-agent-catalogs.md),
  [m0004](m0004-automation-pipeline-workflow.md),
  [m0005](m0005-docker-compose-infrastructure.md),
  [m0006](m0006-document-metadata-lifecycle.md),
  [m0007](m0007-documentation-architecture.md),
  [m0008](m0008-harness-engineering.md),
  [m0009](m0009-llm-wiki-system.md),
  [m0010](m0010-loop-engineering.md),
  [m0011](m0011-memory-hierarchy.md),
  [m0012](m0012-provider-implementation-comparison.md),
  [m0013](m0013-provider-model-landscape.md),
  [m0014](m0014-quality-ci-formatting.md),
  [m0015](m0015-scope-application-matrix.md),
  [m0016](m0016-sdlc-document-roles.md),
  [m0017](m0017-security-governance.md),
  [m0018](m0018-spec-driven-sdlc.md),
  [m0019](m0019-verification-validation.md),
  [m0020](m0020-workspace-baseline.md).
- 관련 연구: [RES-0084](../0084-github-actions-platform/README.md)와
  [RES-0085](../0085-workspace-engineering-main-baseline-assessment/README.md)의
  날짜가 있는 baseline/recovery 증거.
- 정책: [공통 Agent 거버넌스](../../../../.agents/README.md)와
  [documentation protocol](../../../../.agents/governance/documentation-protocol.md).
- Requirements: [REQ-0024](../../../01.requirements/0024-agent-governance-standardization.md),
  [REQ-0025](../../../01.requirements/0025-operational-readiness-closure.md),
  [REQ-0026](../../../01.requirements/0026-document-retention-and-retirement.md).
- Architecture/ADR: [AD-0027](../../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md),
  [AD-0028](../../../02.architecture/descriptions/0028-operational-readiness-closure.md),
  [AD-0030](../../../02.architecture/descriptions/0030-document-lifecycle-governance.md),
  [ADR-0028](../../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md),
  [ADR-0032 Canonical Agent Governance Home](../../../02.architecture/decisions/0032-canonical-agent-governance-home.md),
  ADR-0031.
- Implementation 증거: [완료된 SPEC-0172 결과](../../../98.archive/completed/03.specs/0172-document-contract-convergence/spec.md)와
  [현재 lifecycle reconciliation](../../../98.archive/completed/03.specs/0173-governance-qa-surface-convergence/tasks/tsk-0001-lifecycle-and-red-contracts.md).
- Operations: [Stage 05](../../../05.operations/README.md).
- Audit/data: AUD-0026,
  [k6 guide](../../../05.operations/guides/0061-k6.md), DATA-0082, DATA-0083.
- Package/index/template authority: [research index](../README.md),
  [research-pack template](../../../99.templates/templates/references/research-pack.template.md),
  [research-member template](../../../99.templates/templates/references/research.template.md),
  [Registry](../../../99.templates/registry.json).

#### Historical preservation declaration

SPEC-0158은 아래 나열된 모든 파일을 consumer가 없더라도 보호합니다. 이
선언은 내구성 있는 경로 oracle이며 고정된 개수, hash, commit을 담지
않습니다. 파일은 고쳐지고 확장될 수 있지만 삭제, archive, tombstone,
실질적 축소는 되지 않습니다. 구성원 집합 변경은 이 선언을 원자적으로
갱신해야 합니다.

- `README.md`
- `m0001-agent-instructions-vibe-coding.md`
- `m0002-agent-model-selection.md`
- `m0003-ai-agent-catalogs.md`
- `m0004-automation-pipeline-workflow.md`
- `m0005-docker-compose-infrastructure.md`
- `m0006-document-metadata-lifecycle.md`
- `m0007-documentation-architecture.md`
- `m0008-harness-engineering.md`
- `m0009-llm-wiki-system.md`
- `m0010-loop-engineering.md`
- `m0011-memory-hierarchy.md`
- `m0012-provider-implementation-comparison.md`
- `m0013-provider-model-landscape.md`
- `m0014-quality-ci-formatting.md`
- `m0015-scope-application-matrix.md`
- `m0016-sdlc-document-roles.md`
- `m0017-security-governance.md`
- `m0018-spec-driven-sdlc.md`
- `m0019-verification-validation.md`
- `m0020-workspace-baseline.md`
- `m0021-local-docker-service-consolidation.md`

역사적 연속성은 유지됩니다: canonical pack은 2026년 8월 SPEC-0158
아래에서 재구성되었고 모든 구성원이 source 새로고침과 심화를 거쳤으며
loop coverage gap은 2026-08-17에 수리되었고 2026-09-05 갱신은 모든
identity와 정확한 구성원 집합을 보존합니다. 이후의 baseline 통합은
보호된 어떤 경로도 바꾸지 않으며 m0020을 단일 현재 workspace-baseline
owner로 만듭니다.

#### Historical limitations

- 사용자 전역 Claude/Codex 설정, secret, credential, 개인 key,
  environment 값, shell history, raw log는 이 갱신에서 읽지
  않았습니다.
- 이 갱신에서는 새 provider call, Compose service 시작, deployment,
  rollback, tag, release 동작은 수행하지 않았습니다.
- Provider entitlement와 remote protection은 SPEC-0172가 기록한
  point-in-time 관찰이며 미래 상태를 추론하지 않습니다.
- 깨끗한 full gate는 baseline commit에서의 local conformance만
  증명하며 production 적합성, service 건강성, 내구성, 성능, 복구를
  증명하지 않습니다.
- 모든 profile이 정적으로 render되더라도 네 가지 Compose domain 결함이
  AUD-0097에 남아 있습니다.
- 외부 source는 2026-09-05 이후 가변적입니다. 유료 ISO 텍스트는
  조회하지 않았고 public catalog와 용어 자료만 사용했습니다.
- Graphify report는 baseline보다 이전이며 noise가 있어 advisory로
  취급합니다; 현재 생성된 LLM Wiki 신선도는 오직 등록된 generator와
  check만이 결정합니다.

## Sources

원문별 상세 절·확인일·제품 범위는 멤버의 `Claims and Sources`에서 직접 확인한다.
공급자·모델은 [m0012](m0012-provider-implementation-comparison.md#claims-and-sources)와
[m0013](m0013-provider-model-landscape.md#claims-and-sources), 문서·SDLC는
[m0007](m0007-documentation-architecture.md#claims-and-sources)과
[m0018](m0018-spec-driven-sdlc.md#claims-and-sources), Compose·knowledge는
[m0005](m0005-docker-compose-infrastructure.md#claims-and-sources)와
[m0009](m0009-llm-wiki-system.md#claims-and-sources), CI·보안은
[m0004](m0004-automation-pipeline-workflow.md#claims-and-sources)와
[m0017](m0017-security-governance.md#claims-and-sources)를 시작점으로 삼는다.

역사 인용을 이번 확인 날짜로 다시 지정하지 않았다. 접근 불가, 발행일 미표시,
draft/preview와 문서 간 차이는 해당 주장 옆에 한계로 남긴다.

## Implications

작은 local-first 작업 공간에서는 기존 문서·작업 기록·native 기능으로 필요를
충족하는지 먼저 평가한다. 새로운 wrapper, tracker, 기억 시스템, agent catalog는
수용 시나리오·권한 경계·유지비용이 분명할 때 후보가 된다. 비용 절감률이나
안전성 향상은 측정 없이 주장하지 않는다.

후속 내부 조사는 m0015의 질문을 출발점으로 별도 승인된 범위에서 수행한다.
복구 시험, 실제 provider 호출, 계정·권한 read-back, 서비스 변경은 권한과 격리
조건을 먼저 정해야 한다. 이번 연구는 그 실행을 승인하지 않는다.

## Traceability

연구는 비규범적 근거다. 실제 채택과 변경은 [거버넌스](../../../../.agents/README.md),
[SDLC](../../../../.agents/governance/sdlc.md) 및 해당 Requirement·Architecture·Spec·운영
소유자가 결정한다. 이번 문서 갱신 증거는
[SPEC-0185 Task](../../../98.archive/completed/03.specs/0185-agentic-research-refresh/tasks/tsk-0001-external-research-refresh.md)에만 기록한다.
기존 `parent_ids`는 구조적 관계를 유지하며 새 인용을 부모로 추가하지 않았다.

보존 자료: [RES-0084](../0084-github-actions-platform/README.md),
[RES-0085](../0085-workspace-engineering-main-baseline-assessment/README.md),
[RES-0096](../0096-archive-disposition-consistency/README.md).
문서 계약: [Registry](../../../99.templates/registry.json),
[pack template](../../../99.templates/templates/references/research-pack.template.md),
[member template](../../../99.templates/templates/references/research.template.md).
탐색: [연구 인덱스](../README.md).

## Limitations

- 워크스페이스 구현·운영·계정·보안 상태는 새로 평가하지 않았다. 내부 적용
  상태는 모두 `Not assessed in this run`이다.
- 공식 문서도 변한다. 버전·채널·과금·지원 범위는 채택 전에 재확인한다.
  과거 자료와 이번 가변 문서를 동일한 관측으로 취급하지 않는다.
- 역사 자료의 생성·검증 명령과 count는 실행 지시가 아니다. 폐기된 로컬
  LLM Wiki를 복원하거나 생성기를 실행하지 않는다.
- 문서 검증은 서비스 health, 복구, 성능, 공급자 이용 권한 또는 remote
  enforcement를 증명하지 않는다. 실제 결과와 미실행 사유는 Task에서 구분한다.
