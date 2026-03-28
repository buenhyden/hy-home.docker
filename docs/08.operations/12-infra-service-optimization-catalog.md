# Infra Service Optimization & Expansion Policy

## Overview (KR)

이 문서는 `infra/01-gateway` 부터 `infra/11-laboratory` 까지 운영 중인 서비스에 대해, 현재 구성 기준의 운영 갭을 점검하고 서비스별 최적화 및 추가 권장사항을 정리한다.  
범위는 Docker Compose 기반 운영 표준(가용성, 보안, 관측성, 복구 용이성)이며, 구현 절차는 각 Runbook에서 관리한다.

## Policy Scope

- 대상: `infra/` 하위 게이트웨이/인증/보안/데이터/메시징/관측성/워크플로/AI/툴링/커뮤니케이션/랩 서비스
- 목적: 공통 운영 기준 통일 + 서비스별 개선 백로그 우선순위화
- 비대상: 기능 설계 변경, 애플리케이션 비즈니스 로직 변경

## Applies To

- **Systems**: Docker Compose 기반 인프라 서비스 39개(서비스 디렉터리 기준)
- **Agents**: Infra/DevOps/Operations 역할의 에이전트
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - 모든 장기 실행 서비스에 `healthcheck`, `restart`, `no-new-privileges`, 자원 제한(`cpus`/`memory`)을 기본 적용
  - 민감정보는 환경변수 직접 주입 대신 `secrets` 또는 Vault 경유 주입을 기본 정책으로 적용
  - 서비스별 운영 문서(`08.operations`)와 실행 절차(`09.runbooks`)를 상호 링크로 동기화
- **Allowed**:
  - 서비스 성격(상태저장/배치/실험성)에 따른 예외 설정
  - 티어별 확장(예: AI 게이트웨이, 메시징 DLQ, 관측성 장기보관 스토리지)
- **Disallowed**:
  - 운영 서비스에 무검증 무중단 정책 없는 이미지/설정 변경
  - 근거 없는 외부 포트 노출 및 `latest` 태그 관행

## Exceptions

- 실험성 서비스(`11-laboratory`)는 제한적 예외 허용 가능  
  단, 외부 노출 시 최소 인증/접근제어(SSO 또는 IP 제한)와 자원 상한은 필수로 승인한다.

## Verification

- Compose 정적 점검: `bash scripts/validate-docker-compose.sh`
- Quick Win 기준선 점검: `bash scripts/check-quickwin-baseline.sh`
- 템플릿/보안 기준선 점검: `bash scripts/check-template-security-baseline.sh`
- 문서 추적성 점검: `bash scripts/check-doc-traceability.sh`
- 운영 갭 점검(예시):
  - `healthcheck`/`restart`/`security_opt`/`secrets`/`limits` 유무를 정기 스캔
- 문서 추적성 점검:
  - 서비스별 `infra/*/README.md` ↔ `docs/08.operations/*` ↔ `docs/09.runbooks/*` 상호 링크 확인

## Review Cadence

- 월 1회 정기 검토
- 신규 서비스 추가/중요 버전업/보안 이슈 발생 시 수시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: AI 관련 변경은 `08-ai` 정책 문서 선반영 후 `09.runbooks/08-ai` 절차로 배포/롤백
- **Eval / Guardrail Threshold**: 서비스 영향 변경은 최소 정상성(헬스체크/핵심 API) 자동 검증 통과 필요
- **Log / Trace Retention**: 운영 로그는 `06-observability` 보존 정책 준수
- **Safety Incident Thresholds**: 인증 실패 급증, 데이터 손상, 장기 장애 징후는 즉시 Incident 프로세스 전환

## Baseline Audit Snapshot (2026-03-27)

- 조사 대상 Compose 서비스: **39**
- 갭 집계(서비스 단위):
  - `healthcheck` 미구성: **6/39**
  - `restart` 미구성: **21/39**
  - `no-new-privileges` 미구성: **37/39**
  - 자원 제한(`cpus`/`memory`) 미구성: **37/39**
  - `secrets` 미구성: **16/39**
- 추가 관찰:
  - `infra/07-workflow/airbyte`는 운영/런북 문서는 있으나 인프라 실체(Compose/README) 정의가 누락되어 온보딩 갭이 존재

## Common Template Coverage Snapshot (2026-03-28)

- 기준 템플릿: [infra/common-optimizations.yml](../../infra/common-optimizations.yml)
- 템플릿 기준선:
  - 보안: `no-new-privileges`, `cap_drop: [ALL]` (`x-security-base`)
  - 재시작: `restart: unless-stopped` (`x-restart-default`)
  - 자원 상한: `x-resource-low/med/high/db` (`cpus`, `mem_limit`)
- 적용 커버리지:
  - 서비스 디렉터리 기준: **39/39 (100%)**
  - Compose 파일 기준: **43/43 (100%)**
- 미적용 서비스(서비스 기준): **없음 (0건)**
- 보조 Compose 적용 상태(서비스 수 미산입):
  - [opensearch cluster compose](../../infra/04-data/analytics/opensearch/docker-compose.cluster.yml): **적용 완료**
- 의도된 템플릿 예외:
  - SSoT: [infra/common-optimizations.exceptions.json](../../infra/common-optimizations.exceptions.json)
  - 운영 정책: [13-common-optimizations-template-exceptions.md](./13-common-optimizations-template-exceptions.md)

## Quick Win Enforcement Snapshot (2026-03-28)

- 기준: `PLN-QW-001 ~ PLN-QW-005`
- 검증 명령: `bash scripts/check-quickwin-baseline.sh`
- 통합 Compose 기준 결과(`total services=19`):
  - `restart` 누락: `0`
  - `healthcheck` 누락: `0` (예외 반영 후)
  - `no-new-privileges` 누락: `0`
  - `cpus`/`mem_limit` 누락: `0`
  - `secrets` 누락: `0` (예외 반영 후)
- 승인 예외:
  - `healthcheck`: `pg-cluster-init`, `valkey-cluster-init` (one-shot init job)
  - `secrets`: `etcd-1`, `etcd-2`, `etcd-3` (auth-disabled cluster bootstrap mode)
  - 상세 정의: [infra/common-optimizations.exceptions.json](../../infra/common-optimizations.exceptions.json)

## Tier-by-Tier Optimization & Expansion Catalog

### 01-gateway

- [traefik](../../infra/01-gateway/traefik/README.md): 엔트리포인트별 `rate-limit`/`retry`/`circuit-breaker` 표준화, `restart`/자원 제한 보강  
  ([OPER](./01-gateway/traefik.md), [RUN](../09.runbooks/01-gateway/traefik.md))
- [nginx](../../infra/01-gateway/nginx/README.md): 업스트림 헬스체크/타임아웃 일원화, `read_only`+`tmpfs` 적용, 정적 자산 캐시 정책 강화  
  ([OPER](./01-gateway/nginx.md), [RUN](../09.runbooks/01-gateway/nginx.md))

### 02-auth

- [keycloak](../../infra/02-auth/keycloak/README.md): 세션/캐시 외부화 전략 점검, DB/관리자 비밀 회전 자동화, 노드 확장 대비 세션 정책 정리  
  ([OPER](./02-auth/keycloak.md), [RUN](../09.runbooks/02-auth/keycloak.md))
- [oauth2-proxy](../../infra/02-auth/oauth2-proxy/README.md): 쿠키/세션 만료 정책 표준화, OIDC 장애시 degraded-mode 정책 추가, 보안헤더 강화  
  ([OPER](./02-auth/oauth2-proxy.md), [RUN](../09.runbooks/02-auth/oauth2-proxy.md))

### 03-security

- [vault](../../infra/03-security/vault/README.md): auto-unseal(KMS/HSM) 도입 검토, audit device 원격 적재, `no-new-privileges` 및 자원 상한 일괄 적용  
  ([OPER](./03-security/vault.md), [RUN](../09.runbooks/03-security/vault.md))

### 04-data

- Analytics
  - [influxdb](../../infra/04-data/analytics/influxdb/README.md): retention tiering(핫/웜) 정책과 shard compaction 기준 명문화  
    ([OPER](./04-data/analytics/influxdb.md), [RUN](../09.runbooks/04-data/analytics/influxdb.md))
  - [ksqldb](../../infra/04-data/analytics/ksql/README.md): Kafka 토픽 스키마/호환성 게이트, state store 복구 시간 목표(RTO) 정의  
    ([OPER](./04-data/analytics/ksqldb.md), [RUN](../09.runbooks/04-data/analytics/ksqldb.md))
  - [opensearch](../../infra/04-data/analytics/opensearch/README.md): 인덱스 lifecycle(rollover/ISM) 표준화, 쿼리 가드레일(검색 폭주 제한) 추가  
    ([OPER](./04-data/analytics/opensearch.md), [RUN](../09.runbooks/04-data/analytics/opensearch.md))
  - [warehouses](../../infra/04-data/analytics/warehouses/README.md): 배치 윈도우/리소스 큐 정책, 메타스토어 백업 주기 명시  
    ([OPER](./04-data/analytics/warehouses.md), [RUN](../09.runbooks/04-data/analytics/warehouses.md))
- Cache & KV
  - [valkey-cluster](../../infra/04-data/cache-and-kv/valkey-cluster/README.md): failover 리허설 주기화, eviction 정책 워크로드별 분리, exporter 표준화  
    ([OPER](./04-data/cache-and-kv/valkey-cluster.md), [RUN](../09.runbooks/04-data/cache-and-kv/valkey-cluster.md))
- Lake & Object
  - [minio](../../infra/04-data/lake-and-object/minio/README.md): 버킷 수명주기/버전관리 정책, KMS 연동 암호화, 교차 AZ 복제 검토  
    ([OPER](./04-data/lake-and-object/minio.md), [RUN](../09.runbooks/04-data/lake-and-object/minio.md))
  - [seaweedfs](../../infra/04-data/lake-and-object/seaweedfs/README.md): 볼륨 성장 정책, 마스터 quorum/복구 점검 자동화  
    ([OPER](./04-data/lake-and-object/seaweedfs.md), [RUN](../09.runbooks/04-data/lake-and-object/seaweedfs.md))
- NoSQL
  - [cassandra](../../infra/04-data/nosql/cassandra/README.md): compaction/repair 윈도우 자동화, consistency level 기준(읽기/쓰기) 문서화  
    ([OPER](./04-data/nosql/cassandra.md), [RUN](../09.runbooks/04-data/nosql/cassandra.md))
  - [couchdb](../../infra/04-data/nosql/couchdb/README.md): shard/replica 균형 점검, 디자인문서 배포 절차 표준화  
    ([OPER](./04-data/nosql/couchdb.md), [RUN](../09.runbooks/04-data/nosql/couchdb.md))
  - [mongodb](../../infra/04-data/nosql/mongodb/README.md): replicaset 선출 안정성(heartbeat/timeout) 튜닝, 백업 복구 드릴 정례화  
    ([OPER](./04-data/nosql/mongodb.md), [RUN](../09.runbooks/04-data/nosql/mongodb.md))
- Operational
  - [mng-db](../../infra/04-data/operational/mng-db/README.md): 운영 DB 파라미터 baseline 확정, 슬로우쿼리 게이트와 회귀 점검 추가  
    ([OPER](./04-data/operational/mng-db.md), [RUN](../09.runbooks/04-data/operational/mng-db.md))
  - [supabase](../../infra/04-data/operational/supabase/README.md): 현재 헬스체크 갭 보강, 내부 서비스별 최소 자원 상한 지정, 핵심 컴포넌트 외부노출 재검토  
    ([OPER](./04-data/operational/supabase.md), [RUN](../09.runbooks/04-data/operational/supabase.md))
- Relational
  - [postgresql-cluster](../../infra/04-data/relational/postgresql-cluster/README.md): Patroni failover SLA 수립, VACUUM/Autovacuum 지표 기반 튜닝, PITR 리허설 자동화  
    ([OPER](./04-data/relational/postgresql-cluster.md), [RUN](../09.runbooks/04-data/relational/postgresql-cluster.md))
- Specialized
  - [neo4j](../../infra/04-data/specialized/neo4j/README.md): graph 백업(online/offline) 정책, 대형 질의 timeout/메모리 가드레일 적용  
    ([OPER](./04-data/specialized/neo4j.md), [RUN](../09.runbooks/04-data/specialized/neo4j.md))
  - [qdrant](../../infra/04-data/specialized/qdrant/README.md): 컬렉션별 HNSW/quantization 정책 표준화, 임베딩 재색인 운영 절차 추가  
    ([OPER](./04-data/specialized/qdrant.md), [RUN](../09.runbooks/04-data/specialized/qdrant.md))

### 05-messaging

- [kafka](../../infra/05-messaging/kafka/README.md): 토픽 거버넌스(파티션/보존/compaction) 표준화, DLQ/재처리 파이프라인 공식화  
  ([OPER](./05-messaging/kafka.md), [RUN](../09.runbooks/05-messaging/kafka.md))
- [rabbitmq](../../infra/05-messaging/rabbitmq/README.md): quorum queue 채택 범위 정의, dead-letter 정책과 소비자 재시도 표준화  
  ([OPER](./05-messaging/rabbitmq.md), [RUN](../09.runbooks/05-messaging/rabbitmq.md))

### 06-observability

- [prometheus](../../infra/06-observability/prometheus/README.md): scrape budget 관리, rule/group 지연 예산 도입, 장기저장(remote_write) 계층화  
  ([OPER](./06-observability/prometheus.md), [RUN](../09.runbooks/06-observability/prometheus.md))
- [alertmanager](../../infra/06-observability/alertmanager/README.md): 알림 라우팅 소유권 분리, 중복 억제/소거 윈도우 표준화  
  ([OPER](./06-observability/alertmanager.md), [RUN](../09.runbooks/06-observability/alertmanager.md))
- [grafana](../../infra/06-observability/grafana/README.md): 폴더별 권한/RBAC 정리, 대시보드 lint/JSON 검증 파이프라인 추가  
  ([OPER](./06-observability/grafana.md), [RUN](../09.runbooks/06-observability/grafana.md))
- [loki](../../infra/06-observability/loki/README.md): 로그 라벨 카디널리티 예산, retention/compaction 분리 운영  
  ([OPER](./06-observability/loki.md), [RUN](../09.runbooks/06-observability/loki.md))
- [tempo](../../infra/06-observability/tempo/README.md): trace 샘플링 정책(서비스/엔드포인트별) 명문화, 스팬 폭주 보호장치 추가  
  ([OPER](./06-observability/tempo.md), [RUN](../09.runbooks/06-observability/tempo.md))
- [alloy](../../infra/06-observability/alloy/README.md): 수집 파이프라인 표준 모듈화, 신규 서비스 온보딩 템플릿화  
  ([OPER](./06-observability/alloy.md), [RUN](../09.runbooks/06-observability/alloy.md))
- [pushgateway](../../infra/06-observability/pushgateway/README.md): short-lived job 전용 정책 강제, stale metrics 정리 자동화  
  ([OPER](./06-observability/pushgateway.md), [RUN](../09.runbooks/06-observability/pushgateway.md))
- [pyroscope](../../infra/06-observability/pyroscope/README.md): 프로파일 수집 대상 우선순위화, CPU/heap 프로파일 보존정책 확정  
  ([OPER](./06-observability/pyroscope.md), [RUN](../09.runbooks/06-observability/pyroscope.md))

### 07-workflow

- [airflow](../../infra/07-workflow/airflow/README.md): DAG 품질 게이트(파싱/스케줄/지연) CI 추가, 워커 오토스케일 기준 정의  
  ([OPER](./07-workflow/airflow.md), [RUN](../09.runbooks/07-workflow/airflow.md))
- [n8n](../../infra/07-workflow/n8n/README.md): 워크플로 버전관리/Git 백업 표준화, 자격증명 스토어 Vault 연계 강화  
  ([OPER](./07-workflow/n8n.md), [RUN](../09.runbooks/07-workflow/n8n.md))
- [airbyte](./07-workflow/airbyte.md): 현재 인프라 실체 정의(Compose/README) 우선 보강, 커넥터 승격 기준(실험→운영) 추가  
  ([RUN](../09.runbooks/07-workflow/airbyte.md))

### 08-ai

- [ollama](../../infra/08-ai/ollama/README.md): 모델 캐시/스토리지 정책, GPU 스케줄링 및 동시성 상한, 모델 승격 절차(실험→운영) 명문화  
  ([OPER](./08-ai/ollama.md), [RUN](../09.runbooks/08-ai/ollama.md))
- [open-webui](../../infra/08-ai/open-webui/README.md): SSO 강제, 모델 접근 권한 분리, 대화 로그 보존/마스킹 정책 강화  
  ([OPER](./08-ai/open-webui.md), [RUN](../09.runbooks/08-ai/open-webui.md))

### 09-tooling

- [terraform](../../infra/09-tooling/terraform/README.md): plan/apply 승인 게이트, state 잠금/백업 정책 강화, drift 자동 탐지 추가  
  ([OPER](./09-tooling/terraform.md), [RUN](../09.runbooks/09-tooling/terraform.md))
- [terrakube](../../infra/09-tooling/terrakube/README.md): 워크스페이스 분리 전략, 실행 권한과 감사로그 연동 강화  
  ([OPER](./09-tooling/terrakube.md), [RUN](../09.runbooks/09-tooling/terrakube.md))
- [registry](../../infra/09-tooling/registry/README.md): 이미지 서명/검증(cosign) 도입, 취약점 스캔 실패 차단 정책 적용  
  ([OPER](./09-tooling/registry.md), [RUN](../09.runbooks/09-tooling/registry.md))
- [sonarqube](../../infra/09-tooling/sonarqube/README.md): 품질게이트 임계값 재정의, 브랜치 정책과 보안 룰셋 분리 관리  
  ([OPER](./09-tooling/sonarqube.md), [RUN](../09.runbooks/09-tooling/sonarqube.md))
- [k6](../../infra/09-tooling/k6/README.md): 성능 회귀 기준선 저장/비교 자동화, 시나리오 태그 표준화  
  ([OPER](./09-tooling/k6.md), [RUN](../09.runbooks/09-tooling/k6.md))
- [locust](../../infra/09-tooling/locust/README.md): 분산 실행 토폴로지 표준화, 테스트 데이터 초기화/정리 루틴 추가  
  ([OPER](./09-tooling/locust.md), [RUN](../09.runbooks/09-tooling/locust.md))
- [syncthing](../../infra/09-tooling/syncthing/README.md): 동기화 폴더 ACL/암호화 기준 강화, 충돌 파일 처리 정책 명문화  
  ([OPER](./09-tooling/syncthing.md), [RUN](../09.runbooks/09-tooling/syncthing.md))

### 10-communication

- [mail](../../infra/10-communication/mail/README.md): SPF/DKIM/DMARC 운영 기준 강화, 큐 적체 경보 및 재전송 정책 표준화  
  ([OPER](./10-communication/mail.md), [RUN](../09.runbooks/10-communication/mail.md))

### 11-laboratory

- [dashboard](../../infra/11-laboratory/dashboard/README.md): 실험성 대시보드 접근정책(SSO/IP allowlist) 적용, 만료 정책(자동 종료) 추가  
  ([OPER](./11-laboratory/dashboard.md), [RUN](../09.runbooks/11-laboratory/dashboard.md))
- [dozzle](../../infra/11-laboratory/dozzle/README.md): 로그 열람 권한 제한, 프로덕션 로그 접근 차단 규칙 강화  
  ([OPER](./11-laboratory/dozzle.md), [RUN](../09.runbooks/11-laboratory/dozzle.md))
- [portainer](../../infra/11-laboratory/portainer/README.md): 관리자 계정/세션 정책 강화, 엔드포인트 등록 승인 절차 명문화  
  ([OPER](./11-laboratory/portainer.md), [RUN](../09.runbooks/11-laboratory/portainer.md))
- [redisinsight](../../infra/11-laboratory/redisinsight/README.md): 접근권한 최소화, 운영 캐시 직접 수정 금지 정책 및 감사로그 적용  
  ([OPER](./11-laboratory/redisinsight.md), [RUN](../09.runbooks/11-laboratory/redisinsight.md))

## Related Documents

- **PRD**: [AI Open WebUI PRD](../01.prd/2026-03-27-08-ai-open-webui.md)
- **ARD**: [Architecture References](../02.ard/README.md)
- **Operations Index**: [08.operations README](./README.md)
- **Runbook Index**: [09.runbooks README](../09.runbooks/README.md)
- **Infra Source of Truth**: [infra README](../../infra/README.md)
