---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-06-04-docs-implementation-audit.md -->

# Task: docs/01-05 Content-vs-Implementation Audit

## Overview (KR)

이 문서는 `docs/01.requirements`~`docs/05.operations`(512개 문서)의 **작성된 내용**을
tracked `infra/**` 구현과 의미 단위로 대조한 감사 리포트다. 판정 기준은 링크/거버넌스/체인
검증 통과가 아니라 "문서 내용 vs 현재 구현" 일치 여부다. 본 리포트는 Phase B(아카이브/수정)
실행 및 검증 evidence이며, cross-cutting 거버넌스 작업으로 parent Spec 대신 거버넌스 문서를
참조한다(`documentation-protocol.md` §8.5).

## Inputs

- **Plan**: 승인된 plan-mode 계획 (docs/01-05 content-vs-implementation reconciliation)
- **Implementation SoT**: tracked `infra/**` (compose, configs, scripts, `infra/tech-stack.versions.json`)
- **Existing signals**: `scripts/validation/check-doc-implementation-alignment.sh`, `docs/98.archive/README.md` ledger

## Working Rules

- 기준은 콘텐츠 vs 구현. 자동 체크 통과는 필요조건일 뿐 성공 기준이 아니다.
- 정확히-완료된 문서를 인위적으로 아카이브 후보로 부풀리지 않는다(정직 보고).
- 파괴적 조치(아카이브/삭제)는 현재 구현과 상충하는 whole-document evidence가 확인될 때만 실행한다.

## Methodology & Coverage

- **Structural mapping (100%)**: 512개 문서를 stage/tier/service로 인벤토리하고 40개
  compose-bearing implementation root, tier-level compose 서비스 문서, 거버넌스 표면에 매핑.
- **Deep content read**: 후보군(03 프로세스 스펙, 04 stale active 플랜, 05 draft) + tier 대표 샘플.
- **Signal scans**: frontmatter status 분포, legacy/deprecated 용어, operations↔infra 커버리지.
- **한계**: 모든 512개 문서의 1:1 전수 정독은 수행하지 않음. 아래 "Open decision"에서 심층
  전수 패스 여부를 확인한다.

## Key Finding

2026-06-02 reconciliation이 **구현과 총체적으로 충돌하는 문서를 이미 아카이브**했다(Airbyte
미구현, Codex Markdown/HADS 상충 등 13건 tombstone). 그 결과 이번 심층 감사에서 **신규 ARCHIVE
대상(구현과 상충/orphan)은 발견되지 않았다**. 실질 드리프트는 대부분 **frontmatter status
메타데이터**와 **완료된 일회성 프로세스 문서의 라이프사이클 처리**다.

## Verdict Summary (by stage)

| Stage           | Docs | KEEP (matches impl)                    | FIX (status/content)                       | ARCHIVE candidate   | Notes                                                                         |
| --------------- | ---- | -------------------------------------- | ------------------------------------------ | ------------------- | ----------------------------------------------------------------------------- |
| 01.requirements | 25   | 25 active                              | 23 (status: draft→active)                  | 0                   | tier PRD 23건은 tracked 구현 surface가 있어 active requirements로 유지        |
| 02.architecture | 51   | 51                                     | 0                                          | 0                   | ADR/ARD 전부 현 infra 매핑(traefik/keycloak/vault/kafka/patroni/lgtm 등 실재) |
| 03.specs        | 43   | 15 active / 9 completed / 19 README-like missing status | 7 프로세스 스펙(status active→completed) | 0                   | tier specs 매핑 OK; 프로세스 스펙은 완료된 일회성 작업                        |
| 04.execution    | 125  | 120 completed / 3 active / 2 README-like missing status | stale `active` Open WebUI plan/task → completed; hardening runtime rows deferred | 0 | infra-opt-priority-plan은 ongoing roadmap이라 active 유지                      |
| 05.operations   | 268  | 201 active / 67 README-like missing status | open-notebook draft→active; policy/guide profile 중복 정리; bucket-root leaf 문서를 목적 폴더로 정리 | 0 | orphan 없음(`failures=0`); policy/guide/profile 및 operations purpose 회귀 게이트 반영 |

## Task Table

### Findings and Disposition

| ID   | Doc(s)                                                                                                                                                                                                                                     | Evidence                                                                                     | Disposition |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- | ----------- |
| F-01 | `docs/05.operations/{guides,policies}/11-laboratory/open-notebook.md`                                                                                                                                                                      | `infra/11-laboratory/open-notebook` 구현 존재, 내용 일치                                     | status `draft`→`active` 적용 |
| F-02 | `docs/04.execution/plans/2026-03-27-08-ai-open-webui-plan.md`, `.../tasks/2026-03-27-08-ai-open-webui-tasks.md`                                                                                                                            | Open WebUI 구현 surface 존재(`infra/08-ai/open-webui`); live RAG indexing은 런타임 evidence 필요 | plan/task status `active`→`completed` 적용; task 내부 live RAG row는 `Deferred`로 보정 |
| F-03 | `docs/03.specs/{workspace-consistency-2026-05b,workspace-doc-consistency-2026-05,docs-taxonomy-agent-first-migration,harness-agent-first-engineering,llm-wiki-agent-first-completion,home-docker-revalidation-deferred-follow-up}/spec.md` | 기술된 작업이 현재 구현에 반영됨(R4/R5 규칙·CI taxonomy·LLM Wiki generator·docs taxonomy 등) | status `active`→`completed` 적용; 현재 구현과 상충하지 않아 archive 미적용 |
| F-04 | `docs/04.execution/plans/2026-03-27-infra-service-optimization-priority-plan.md`                                                                                                                                                           | Quick Wins는 구현됐지만 2026 Q2/Q3 quarterly roadmap과 운영 기준 코드화 항목은 계획으로 남아 있음 | `active` 유지 |
| F-05 | `docs/01.requirements/2026-03-26-*` 및 관련 tier PRD                                                                                                                                                                                       | tracked tier implementation exists under `infra/**`; requirements remain current inputs rather than completed task evidence | status `draft`→`active` 적용 |
| F-06 | 변경 폴더의 README 및 governance 문서                                                                                                                                                                                                      | folder-level content/status changes require README/governance alignment                       | `docs/01.requirements/README.md`, QA/GitHub/script governance, progress log updated |
| F-07 | `docs/05.operations/policies/**/*.md`                                                                                                                                                                                                       | 여러 policy leaf에 현재 `policy.template.md`와 다른 중복 `## Policy Scope` heading이 남아 있었음 | 두 번째 이후 `## Policy Scope` heading 제거, bullets 보존; `check-repo-contracts.sh`에 exactly-one gate 추가; `policies/README.md` 계약 업데이트 |
| F-08 | `docs/05.operations/guides/{05-messaging/kafka,06-observability/{alertmanager,grafana,prometheus},09-tooling/{sonarqube,terraform,terrakube}}.md`, `docs/05.operations/runbooks/09-tooling/terraform.md` | guide leaf 7개에 중복 `### Usage Type` profile block이 남아 있었고 Terraform runbook에 `<your-profile>` placeholder가 있었음 | guide 중복 profile 제거, service content 보존, repo contract에 duplicate Usage Type gate 추가; Terraform runbook은 env-var based credential refresh로 정리 |
| F-09 | `docs/05.operations/{guides,policies}/09-tooling/{sonarqube,syncthing}.md`                                                                                                                                                                  | 문서는 `09-tooling` 경로/구현에 속하지만 ID 주석이 과거 `07-tooling` 또는 `08-tooling` tier를 가리킴 | ID 주석을 `09-tooling:<service>`로 정정; `check-repo-contracts.sh`에 operations ID tier/path 일치 gate 추가; 09-tooling guide/policy README에 규칙 반영 |
| F-10 | `docs/02.architecture/requirements/0013-open-webui-architecture.md`, `docs/03.specs/{01-gateway,02-auth,03-security,05-messaging,08-ai}`, selected `docs/04.execution/tasks`, selected `docs/05.operations/{guides,policies,runbooks}` | compose 및 `infra/tech-stack.versions.json`의 현재 이미지 태그와 문서 본문에 남은 runtime version literal이 어긋남 | Traefik, Keycloak, OAuth2 Proxy, Vault, Kafka, RabbitMQ, Kafbat UI, Open WebUI, Grafana, Airflow, Pushgateway, Pyroscope, Qdrant, Neo4j 문서 버전을 현재 구현에 맞게 정정; `check-repo-contracts.sh`에 stale runtime version gate 추가 |
| F-11 | `docs/03.specs/standardize-infra-net/spec.md`, `docs/05.operations/{guides,runbooks}/12-infra-net/standardize-infra-net.md` | active docs의 wildcard IPv4 예시가 authoritative mapping table과 달리 복사 가능한 placeholder처럼 남아 있었음 | registry의 실제 구현 IP(`172.19.0.7`) 기반 예시로 정정하고 대상 서비스에는 authoritative table 값을 사용하도록 단계 보강; `check-repo-contracts.sh`에 stage docs IP placeholder gate 추가 |
| F-12 | `docs/03.specs/workspace-audit-2026-05/{spec.md,README.md}`, `docs/03.specs/README.md` | 완료된 2026-05 감사 spec의 gap table이 당시 baseline인지 현재 구현 상태인지 불명확하게 읽힐 수 있었음 | section을 historical snapshot으로 명시하고 README/03.specs index에서 completed historical spec으로 설명 보강 |
| F-13 | `docs/05.operations/guides/00-workspace/{env-key-comparison,sensitive-env-vars-comparison}.md` | metadata-only 비교 문서의 숫자가 현재 `.env.example`, `.env`, `secrets/SENSITIVE_ENV_VARS.md*` 상태와 어긋남 | `.env.example`/`.env` 키 수를 325/325로, sensitive registry line count를 184/184로 정정하고 값 비교 금지 문구를 metadata-only로 정리; `check-repo-contracts.sh`에 조건부 metadata comparison guide drift gate 추가 |
| F-14 | `docs/02.architecture/{decisions/0015-analytics-engine-selection.md,requirements/0012-data-analytics-architecture.md}`, `docs/03.specs/04-data-analytics/{spec.md,README.md}` | analytics 엔진 선택/계약 문서가 현재 `infra/04-data/analytics` compose의 version family와 다르게 InfluxDB primary, OpenSearch, StarRocks 계열을 오래된 기준으로 설명함 | InfluxDB 3.x Core primary + InfluxDB 2.x legacy compose, Confluent ksqlDB 8.x, OpenSearch 3.x, StarRocks 4.x로 정정; InfluxDB primary health check를 `8181`로 정정; stale analytics version-family gate 추가 |
| F-15 | `docs/05.operations/{guides/06-observability/prometheus.md,runbooks/11-laboratory/dozzle.md,runbooks/11-laboratory/README.md}`, `infra/11-laboratory/dozzle/README.md` | Prometheus guide와 Dozzle runbook/infra README가 현재 PostgreSQL image family 및 Dozzle compose tag와 맞지 않는 구현값을 담고 있었음 | Prometheus scrape 대상 설명을 PostgreSQL 17/18 family로 정정; Dozzle 기준 tag를 `amir20/dozzle:v10.6.4`로 맞추고 rollback은 직전 검증 tag evidence를 기록하도록 수정; stale Dozzle/PostgreSQL literal gate 추가 |
| F-16 | `docs/05.operations/{guides,policies,runbooks}/README.md` 및 `00-workspace`, `12-infra-net`, `90-knowledge` 목적 폴더 | bucket root에 leaf 문서와 folder index가 섞여 있어 Stage 05 운영 문서 구조가 목적별 탐색 계약과 맞지 않았음 | root에는 bucket `README.md`만 남기고 workspace, infra_net, knowledge 문서를 목적 폴더로 이동; parent/child README와 cross-link를 갱신; `check-repo-contracts.sh`에 operations bucket-root leaf 금지와 target-path 일치 gate 추가 |

## Archive Decision

완료된 일회성 **프로세스 스펙/플랜**(F-03/F-04: workspace-audit, docs-taxonomy-migration,
harness-agent-first, llm-wiki-completion 등)은 현재 구현과 **상충하지 않고 정확히 일치**한다.
따라서 archive 기준은 "historical" 여부가 아니라 **현재 구현과 상충하는지**로 적용한다.
이번 pass에서 신규 archive 대상은 발견되지 않았고, 이미 Airbyte 및 구 Codex/HADS 상충 chain은
`docs/98.archive/README.md` ledger로 tombstone 처리되어 있다.
Stage 05 bucket-root 구조 drift(F-16)는 문서 내용 자체가 현재 구현과 상충하지 않고 위치/탐색
계약만 낡은 경우라 archive가 아니라 in-place 이동 및 reference 갱신으로 처리했다.

## Verification Summary

- Stage 01-05 inventory: `docs/01.requirements=25`, `docs/02.architecture=51`, `docs/03.specs=43`, `docs/04.execution=125`, `docs/05.operations=268`, total `512`.
- operations 서비스 커버리지: `check-doc-implementation-alignment.sh` → `operations_service_docs_checked=143`, `failures=0`.
- operations bucket-root scan: `docs/05.operations/{guides,policies,runbooks}` root에는 각 bucket `README.md`만 남음.
- stale operations root-path scan: 이전 bucket-root leaf 형태(`guides/<leaf>.md`, `runbooks/<leaf>.md`, `policies/<leaf>.md`) 0건.
- legacy/orphan 스캔: 신규 미구현-service 문서 없음; Patroni/Spilo/HADS는 현행 구현 또는 historical evidence로 분류.
- policy profile scan: `docs/05.operations/policies/**/*.md` leaf에서 `## Policy Scope` 중복 0건; repo contract가 policy leaf당 exactly one heading을 강제.
- guide profile scan: 중복 `### Usage Type` 0건; 남은 TODO/TBD/placeholder-like hits는 historical evidence 또는 scan command literal로 분류.
- operations ID tier scan: `docs/05.operations/{guides,policies,runbooks}` ID 주석과 path tier 불일치 0건; repo contract가 불일치를 차단.
- runtime version drift scan: stale runtime version literal 0건; repo contract가 현재 compose/tech-stack registry와 어긋나는 문서 버전 재유입을 차단.
- IP placeholder scan: wildcard infra/k3d IPv4 placeholder 0건; repo contract가 concrete-network placeholder 재유입을 차단.
- metadata comparison scan: `.env.example`/`.env` key count 325/325, sensitive registry line count 184/184, secret ID count 107; repo contract가 로컬 파일 존재 시 metadata-only 숫자 drift를 차단.
- analytics/laboratory version-family scan: analytics primary/decision stale phrases, Dozzle old tag, and PostgreSQL old scrape family phrase 0건; repo contract가 exact stale literal 재유입을 차단.
- reference.template.md archive 언급: 0건(제약 이미 충족).
- Local QA gate: `bash scripts/validation/run-local-qa-gates.sh` → PASS, repo contracts `failures=0`.

## Related Documents

- **Archive index/ledger**: [98.archive README](../../98.archive/README.md)
- **Alignment check**: [check-doc-implementation-alignment.sh](../../../scripts/validation/check-doc-implementation-alignment.sh)
- **Documentation protocol**: [documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Progress Log**: [progress.md](../../00.agent-governance/memory/progress.md)
