---
title: "Infrastructure Optimization Governance Policy"
version: "1.3.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-25"
layer: "operations"
artifact_id: "POL-0006"
parent_ids: []
created: "2026-06-04"
---
# Infrastructure Optimization Governance Policy

## Overview

이 문서는 `infra/01-gateway` 부터 `infra/11-laboratory` 까지 운영 중인 서비스에 대해, 현재 구성 기준의 운영 갭을 점검하고 서비스별 최적화 및 추가 권장사항을 정리한다.
범위는 Docker Compose 기반 운영 표준(가용성, 보안, 관측성, 복구 용이성)이며, 구현 절차는 각 Procedure에서 관리한다.

## Policy Scope

- 대상: `infra/` 하위 게이트웨이/인증/보안/데이터/메시징/관측성/워크플로/AI/툴링/커뮤니케이션/랩 서비스
- 목적: 공통 운영 기준 통일 + 서비스별 개선 백로그 우선순위화
- 비대상: 기능 설계 변경, 애플리케이션 비즈니스 로직 변경

- **Systems**: tracked Compose source의 140 service identity(2026-09-20 inventory: Compose fragment와 root include 각 42개). service directory 수는 identity 수나 activation 범위의 대체 지표가 아니다.
- **Agents**: Infra/DevOps/Operations 역할의 에이전트
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - 모든 장기 실행 서비스에 `healthcheck`, `restart`, `no-new-privileges`, 자원 제한(`cpus`/`memory`)을 기본 적용
  - 민감정보는 환경변수 직접 주입 대신 Docker Secrets 또는 현재 HOME secret authority인 OpenBao 경유 주입을 기본 정책으로 적용
  - 서비스별 운영 문서(`05.operations`)와 실행 절차(`05.operations`)를 상호 링크로 동기화
- **Allowed**:
  - 서비스 성격(상태저장/배치/실험성)에 따른 예외 설정
  - 티어별 확장(예: AI 게이트웨이, 메시징 DLQ, 관측성 장기보관 스토리지)
- **Disallowed**:
  - 운영 서비스에 무검증 무중단 정책 없는 이미지/설정 변경
  - 근거 없는 외부 포트 노출 및 `latest` 태그 관행

### Source and lifecycle boundary

- Compose/Dockerfile declarations own runtime pins. `infra/tech-stack.versions.json`은
  Compose image declaration에서 파생한 projection이며 Dockerfile build pin 전체를
  대체하지 않는다.
- 새 service는 root include, POL-0078 canonical profile membership, public
  environment/secret schema, image projection/update owner, service README와
  Guide/Policy/Runbook을 함께 갱신한다. Guide의 optional
  `implementation_services` mapping이 exact Compose path/service binding을 소유하고,
  existing operations-catalog validator가 global join을 검증한다.
- current HOME selection은 `core mng ai workflow storage obs-core obs-host
  availability logs alerting tracing profiling obs-gpu registry`이며 41 service
  identity다. `tooling`, `testing`,
  `iac`, `dependency-update`는 named operator/development work이고 HOME에 포함하지
  않는다. profile vocabulary 또는 full membership table은 POL-0078에서만 관리한다.
- **Recreate on edit**: 단일 파일 bind mount(`./config/x.yml:/etc/x.yml`)는
  mount 시점의 inode를 고정한다. editor와 branch 전환은 파일을 새 inode로
  교체하므로 container는 이전 내용을 계속 읽고, `restart`도 이를 바꾸지 않는다.
  따라서 단일 파일로 mount된 configuration을 수정한 뒤에는
  `docker compose up -d --force-recreate <service>`로 해당 service를 재생성한다.
  Mount는 directory로 바꾸지 않으며 이 규칙과 hash 점검이 통제 수단이다.
- **Post-apply hash check**: 모든 live apply(`up -d`, recreate, 설정 변경 반영)
  직후 container를 시작한 checkout에서
  `python3 scripts/operations/check-config-mount-hashes.py --root <checkout>`을
  실행한다. `DIFF`(exit 1)는 recreate 누락이므로 해당 service를 재생성하고 다시
  점검한다. `cat`이 없는 image는 `UNREADABLE`로 표시되며,
  `--helper-image <local image with cat>`은 일시적 `--rm` helper container를
  띄우므로 해당 apply 승인 범위에서만 사용한다. `secrets/` 경로와 파일 내용은
  읽거나 출력하지 않는다. `docker cp`는 bind mount를 host 경로로 해석해 오래된
  inode를 보지 못하므로 이 점검에 쓰지 않는다.

### AI Agent Policy

- **Model / Prompt Change Process**: AI 관련 변경은 `08-ai` Policy 선반영 후 AI Runbook(`docs/05.operations/runbooks/README.md`의 08 AI 분류) 절차로 배포/롤백
- **Eval / Guardrail Threshold**: 서비스 영향 변경은 최소 정상성(헬스체크/핵심 API) 자동 검증 통과 필요
- **Log / Trace Retention**: 운영 로그는 `06-observability` 보존 정책 준수
- **Safety Incident Thresholds**: 인증 실패 급증, 데이터 손상, 장기 장애 징후는 즉시 Incident 프로세스 전환

### Roadmap Status and Priority Boundary

이 정책은 기존 infrastructure optimization catalog와 umbrella priority
plan의 고유한 현재 사실을 하나의 canonical owner로 통합합니다. Quick Win
완료는 quarterly roadmap 전체 완료를 의미하지 않습니다.

#### Priority Model

- Priority Score = `Risk Reduction(40) + Availability Impact(25) + Security Impact(25) + Execution Effort Inverse(10)`
- Tier A: `01-gateway`, `02-auth`, `03-security`, `04-data`, `05-messaging`, `06-observability`
- Tier B: `07-workflow`, `08-ai`, `09-tooling`, `10-communication`
- Tier C: `11-laboratory`

#### Roadmap Disposition

| Item | Current evidence | Current disposition |
| :-- | :-- | :-- |
| Quick Wins 001–005 | 2026-03-28 baseline은 승인된 예외 반영 후 `restart`, `healthcheck`, `no-new-privileges`, `cpus`/`mem_limit`, `secrets` 누락 0건을 기록합니다. | Implemented baseline; regression gates를 유지합니다. |
| Workflow definition gap | 미구현 workflow 서비스는 active Operations chain에서 제거되고 archive ledger로만 추적됩니다. | Implemented active-chain cleanup. |
| Traceability | 문서 traceability validator가 standing gate를 소유합니다. | Enforced. |
| 2026 Q2 roadmap | recovery rehearsal calendar, SLO/Alert alignment report, 전체 Tier A closure를 하나의 완료 deliverable로 증명한 후속 evidence가 없습니다. | Unclosed; elapsed time으로 완료를 추론하지 않습니다. |
| 2026 Q3 roadmap | performance backlog report, policy-validation CI, security-hardening checklist의 전체 완료 evidence가 없습니다. | Planned until implemented, superseded, or explicitly retired. |

Quarterly 항목은 후속 Task 또는 replacement roadmap이 위 deliverable을
검증 evidence와 연결할 때만 완료 또는 superseded로 전환할 수 있습니다.
과거 plan-authoring checklist의 완료 표시는 이 정책 roadmap의 완료 근거가
아닙니다.

### Tier-by-Tier Optimization & Expansion Catalog

#### 01-gateway

- [traefik](../../../infra/01-gateway/traefik/README.md): 엔트리포인트별 `rate-limit`/`retry`/`circuit-breaker` 표준화, `restart`/자원 제한 보강
  ([OPER](../guides/0013-traefik.md), [RUN](../runbooks/0013-traefik.md))
- [nginx](../../../infra/01-gateway/nginx/README.md): 업스트림 헬스체크/타임아웃 일원화, `read_only`+`tmpfs` 적용, 정적 자산 캐시 정책 강화
  ([OPER](../guides/0011-nginx.md), [RUN](../runbooks/0011-nginx.md))

#### 02-auth

- [keycloak](../../../infra/02-auth/keycloak/README.md): 세션/캐시 외부화 전략 점검, DB/관리자 비밀 회전 자동화, 노드 확장 대비 세션 정책 정리
  ([OPER](../guides/0014-keycloak.md), [RUN](../runbooks/0014-keycloak.md))
- [oauth2-proxy](../../../infra/02-auth/oauth2-proxy/README.md): 쿠키/세션 만료 정책 표준화, OIDC 장애시 degraded-mode 정책 추가, 보안헤더 강화
  ([OPER](../guides/0015-oauth2-proxy.md), [RUN](../runbooks/0015-oauth2-proxy.md))

#### 03-security

- [openbao](../../../infra/03-security/openbao/README.md): 현재 HOME secret authority의 single-node Raft 복구, auto-unseal(KMS/HSM), remote audit와 최소 권한 운영을 단계적으로 검토
  ([OPER](../guides/0085-openbao.md), [RUN](../runbooks/0085-openbao.md))

#### 04-data

- Analytics
  - [influxdb](../../../infra/04-data/analytics/influxdb/README.md): retention tiering(핫/웜) 정책과 shard compaction 기준 명문화
    ([OPER](../guides/0017-influxdb.md), [RUN](../runbooks/0017-influxdb.md))
  - [opensearch](../../../infra/04-data/analytics/opensearch/README.md): 인덱스 lifecycle(rollover/ISM) 표준화, 쿼리 가드레일(검색 폭주 제한) 추가
    ([OPER](../guides/0019-opensearch.md), [RUN](../runbooks/0019-opensearch.md))
- Cache & KV
  - [valkey-cluster](../../../infra/04-data/cache-and-kv/valkey-cluster/README.md): failover 리허설 주기화, eviction 정책 워크로드별 분리, exporter 표준화
    ([OPER](../guides/0022-valkey-cluster.md), [RUN](../runbooks/0022-valkey-cluster.md))
- Lake & Object
  - [seaweedfs](../../../infra/04-data/lake-and-object/seaweedfs/README.md): 볼륨 성장 정책, 마스터 quorum/복구 점검 자동화
    ([OPER](../guides/0024-seaweedfs.md), [RUN](../runbooks/0024-seaweedfs.md))
- NoSQL
  - [cassandra](../../../infra/04-data/nosql/cassandra/README.md): compaction/repair 윈도우 자동화, consistency level 기준(읽기/쓰기) 문서화
    ([OPER](../guides/0025-cassandra.md), [RUN](../runbooks/0025-cassandra.md))
  - [couchdb](../../../infra/04-data/nosql/couchdb/README.md): shard/replica 균형 점검, 디자인문서 배포 절차 표준화
    ([OPER](../guides/0026-couchdb.md), [RUN](../runbooks/0026-couchdb.md))
  - [mongodb](../../../infra/04-data/nosql/mongodb/README.md): replicaset 선출 안정성(heartbeat/timeout) 튜닝, 백업 복구 드릴 정례화
    ([OPER](../guides/0027-mongodb.md), [RUN](../runbooks/0027-mongodb.md))
- Operational
  - [mng-db](../../../infra/04-data/operational/mng-db/README.md): 운영 DB 파라미터 baseline 확정, 슬로우쿼리 게이트와 회귀 점검 추가
    ([OPER](../guides/0028-management-database.md), [RUN](../runbooks/0028-management-database.md))
  - [supabase](../../../infra/04-data/operational/supabase/README.md): 현재 헬스체크 갭 보강, 내부 서비스별 최소 자원 상한 지정, 핵심 컴포넌트 외부노출 재검토
    ([OPER](../guides/0029-supabase.md), [RUN](../runbooks/0029-supabase.md))
- Relational
  - [postgresql-cluster](../../../infra/04-data/relational/postgresql-cluster/README.md): Patroni failover SLA 수립, VACUUM/Autovacuum 지표 기반 튜닝, PITR 리허설 자동화
    ([OPER](../guides/0031-postgresql-cluster.md), [RUN](../runbooks/0031-postgresql-cluster.md))
- Specialized
  - [neo4j](../../../infra/04-data/specialized/neo4j/README.md): graph 백업(online/offline) 정책, 대형 질의 timeout/메모리 가드레일 적용
    ([OPER](../guides/0033-neo4j.md), [RUN](../runbooks/0033-neo4j.md))
  - [qdrant](../../../infra/04-data/specialized/qdrant/README.md): 컬렉션별 HNSW/quantization 정책 표준화, 임베딩 재색인 운영 절차 추가
    ([OPER](../guides/0034-qdrant.md), [RUN](../runbooks/0034-qdrant.md))

#### 05-messaging

- [kafka](../../../infra/05-messaging/kafka/README.md): 토픽 거버넌스(파티션/보존/compaction) 표준화, DLQ/재처리 파이프라인 공식화
  ([OPER](../guides/0036-kafka.md), [RUN](../runbooks/0036-kafka.md))

#### 06-observability

- [prometheus](../../../infra/06-observability/prometheus/README.md): scrape budget 관리, rule/group 지연 예산 도입, 장기저장(remote_write) 계층화
  ([OPER](../guides/0045-prometheus.md), [RUN](../runbooks/0045-prometheus.md))
- [alertmanager](../../../infra/06-observability/alertmanager/README.md): 알림 라우팅 소유권 분리, 중복 억제/소거 윈도우 표준화
  ([OPER](../guides/0039-alertmanager.md), [RUN](../runbooks/0039-alertmanager.md))
- [grafana](../../../infra/06-observability/grafana/README.md): 폴더별 권한/RBAC 정리, 대시보드 lint/JSON 검증 파이프라인 추가
  ([OPER](../guides/0041-grafana.md), [RUN](../runbooks/0041-grafana.md))
- [loki](../../../infra/06-observability/loki/README.md): 로그 라벨 카디널리티 예산, retention/compaction 분리 운영
  ([OPER](../guides/0043-loki.md), [RUN](../runbooks/0043-loki.md))
- [tempo](../../../infra/06-observability/tempo/README.md): trace 샘플링 정책(서비스/엔드포인트별) 명문화, 스팬 폭주 보호장치 추가
  ([OPER](../guides/0049-tempo.md), [RUN](../runbooks/0049-tempo.md))
- [alloy](../../../infra/06-observability/alloy/README.md): 수집 파이프라인 표준 모듈화, 신규 서비스 온보딩 템플릿화
  ([OPER](../guides/0040-alloy.md), [RUN](../runbooks/0040-alloy.md))
- [pushgateway](../../../infra/06-observability/pushgateway/README.md): short-lived job 전용 정책 강제, stale metrics 정리 자동화
  ([OPER](../guides/0046-pushgateway.md), [RUN](../runbooks/0046-pushgateway.md))
- [pyroscope](../../../infra/06-observability/pyroscope/README.md): 프로파일 수집 대상 우선순위화, CPU/heap 프로파일 보존정책 확정
  ([OPER](../guides/0047-pyroscope.md), [RUN](../runbooks/0047-pyroscope.md))

#### 07-workflow

- [airflow](../../../infra/07-workflow/airflow/README.md): DAG 품질 게이트(파싱/스케줄/지연) CI 추가, 워커 오토스케일 기준 정의
  ([OPER](../guides/0050-airflow.md), [RUN](../runbooks/0050-airflow.md))
- [n8n](../../../infra/07-workflow/n8n/README.md): 워크플로 버전관리/Git 백업 표준화. 자격증명 저장소의 OpenBao 연계는 별도 설계·승인·마이그레이션 후에만 도입하며 현재 통합으로 간주하지 않음
  ([OPER](../guides/0053-n8n.md), [RUN](../runbooks/0053-n8n.md))

#### 08-ai

- [ollama](../../../infra/08-ai/ollama/README.md): 모델 캐시/스토리지 정책, GPU 스케줄링 및 동시성 상한, 모델 승격 절차(실험→운영) 명문화
  ([OPER](../guides/0056-ollama.md), [RUN](../runbooks/0056-ollama.md))
- [open-webui](../../../infra/08-ai/open-webui/README.md): SSO 강제, 모델 접근 권한 분리, 대화 로그 보존/마스킹 정책 강화
  ([OPER](../guides/0057-open-webui.md), [RUN](../runbooks/0057-open-webui.md))

#### 09-tooling

- [opentofu](../../../infra/09-tooling/opentofu/README.md): plan/apply 승인 게이트, state 잠금/백업 정책 강화, drift 자동 탐지 추가
  ([OPER](../guides/0082-opentofu.md), [RUN](../runbooks/0082-opentofu.md)); 기존 Terraform workspace는 [migration handoff](../guides/0068-terraform.md)를 따른다.
- [terrakube](../../../infra/09-tooling/terrakube/README.md): 워크스페이스 분리 전략, 실행 권한과 감사로그 연동 강화
  ([OPER](../guides/0069-terrakube.md), [RUN](../runbooks/0069-terrakube.md))
- [registry](../../../infra/09-tooling/registry/README.md): 이미지 서명/검증(cosign) 도입, 취약점 스캔 실패 차단 정책 적용
  ([OPER](../guides/0065-registry.md), [RUN](../runbooks/0065-registry.md))
- [sonarqube](../../../infra/09-tooling/sonarqube/README.md): 품질게이트 임계값 재정의, 브랜치 정책과 보안 룰셋 분리 관리
  ([OPER](../guides/0066-sonarqube.md), [RUN](../runbooks/0066-sonarqube.md))
- [k6](../../../infra/09-tooling/k6/README.md): 성능 회귀 기준선 저장/비교 자동화, 시나리오 태그 표준화
  ([OPER](../guides/0061-k6.md), [RUN](../runbooks/0061-k6.md))
- [locust](../../../infra/09-tooling/locust/README.md): 분산 실행 토폴로지 표준화, 테스트 데이터 초기화/정리 루틴 추가
  ([OPER](../guides/0062-locust.md), [RUN](../runbooks/0062-locust.md))
- Syncthing runtime은 저장소에서 제거되었으며 현재 서비스 확장/하드닝 대상이 아니다. 기존 파일과 외부 동기화 상태는 제거된 Compose 서비스를 재기동하지 않고 소유자와 확인한다.

#### 10-communication

- [mail](../../../infra/10-communication/stalwart/README.md): SPF/DKIM/DMARC 운영 기준 강화, 큐 적체 경보 및 재전송 정책 표준화
  ([OPER](../guides/0070-mail.md), [RUN](../runbooks/0070-mail.md))

#### 11-laboratory

- [dozzle](../../../infra/11-laboratory/dozzle/README.md): 로그 열람 권한 제한, 프로덕션 로그 접근 차단 규칙 강화
  ([OPER](../guides/0072-dozzle.md), [RUN](../runbooks/0072-dozzle.md))
- [redisinsight](../../../infra/11-laboratory/redisinsight/README.md): 접근권한 최소화, 운영 캐시 직접 수정 금지 정책 및 감사로그 적용
  ([OPER](../guides/0076-redisinsight.md), [RUN](../runbooks/0076-redisinsight.md))

## Exceptions

- 실험성 서비스(`11-laboratory`)는 제한적 예외 허용 가능
  단, 외부 노출 시 최소 인증/접근제어(SSO 또는 IP 제한)와 자원 상한은 필수로 승인한다.

## Verification

- Compose 정적 점검: `bash scripts/validation/validate-docker-compose.sh`
- Quick Win 기준선 점검: `bash scripts/validation/check-quickwin-baseline.sh`
- 템플릿/보안 기준선 점검: `bash scripts/validation/check-template-security-baseline.sh`
- 문서 추적성 점검: `python3 scripts/validation/check-document-links.py --mode traceability`
- 단일 파일 config mount 점검(live apply 직후, read-only): `python3 scripts/operations/check-config-mount-hashes.py --root <checkout>`
- 운영 갭 점검(예시):
  - `healthcheck`/`restart`/`security_opt`/`secrets`/`limits` 유무를 정기 스캔
- 문서 추적성 점검:
  - 서비스별 `infra/*/README.md` ↔ `docs/05.operations/*` ↔ `docs/05.operations/*` 상호 링크 확인

### Baseline Audit Snapshot (2026-03-27)

- 조사 대상 Compose 서비스: **39**
- 갭 집계(서비스 단위):
  - `healthcheck` 미구성: **6/39**
  - `restart` 미구성: **21/39**
  - `no-new-privileges` 미구성: **37/39**
  - 자원 제한(`cpus`/`memory`) 미구성: **37/39**
  - `secrets` 미구성: **16/39**
- 추가 관찰:
  - workflow tier의 미구현 서비스 문서는 active operations chain에서 제거하고 archive ledger로만 추적한다.

### Common Template Coverage Snapshot (2026-03-28)

- 기준 템플릿: [infra/common-optimizations.yml](../../../infra/common-optimizations.yml)
- 템플릿 기준선:
  - 보안: `no-new-privileges`, `cap_drop: [ALL]` (`x-security-base`)
  - 재시작: `restart: unless-stopped` (`x-restart-default`)
  - 자원 상한: `x-resource-low/med/high/db` (`cpus`, `mem_limit`)
- 적용 커버리지:
  - 서비스 디렉터리 기준: **39/39 (100%)**
  - Compose 파일 기준: **43/43 (100%)**
- 미적용 서비스(서비스 기준): **없음 (0건)**
- 보조 Compose 적용 상태(서비스 수 미산입):
  - opensearch cluster 노드는 [opensearch compose](../../../infra/04-data/analytics/opensearch/docker-compose.yml)의 `opensearch-cluster` profile로 통합됨: **적용 완료**
- 의도된 템플릿 예외:
  - SSoT: [infra/common-optimizations.exceptions.json](../../../infra/common-optimizations.exceptions.json)
  - 운영 정책: [common-optimizations-template-exceptions.md](0001-common-optimizations-template-exceptions.md)

### Quick Win Enforcement Snapshot (2026-03-28)

- 기준: `PLN-QW-001 ~ PLN-QW-005`
- 검증 명령: `bash scripts/validation/check-quickwin-baseline.sh`
- 통합 Compose 기준 결과(`total services=19`):
  - `restart` 누락: `0`
  - `healthcheck` 누락: `0` (예외 반영 후)
  - `no-new-privileges` 누락: `0`
  - `cpus`/`mem_limit` 누락: `0`
  - `secrets` 누락: `0` (예외 반영 후)
- 승인 예외:
  - `healthcheck`: `pg-cluster-init`, `valkey-cluster-init` (one-shot init job)
  - `secrets`: `etcd-1`, `etcd-2`, `etcd-3` (auth-disabled cluster bootstrap mode)
  - 상세 정의: [infra/common-optimizations.exceptions.json](../../../infra/common-optimizations.exceptions.json)

## Review Cadence

- 월 1회 정기 검토
- 신규 서비스 추가/중요 버전업/보안 이슈 발생 시 수시 검토

## Traceability

- Subject peers: none — `00-workspace/0006-infrastructure-optimization-governance` holds this document alone.

## Related Documents

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../infra/tech-stack.versions.json) provides Compose-image drift verification.

- [Operations index](../README.md)
