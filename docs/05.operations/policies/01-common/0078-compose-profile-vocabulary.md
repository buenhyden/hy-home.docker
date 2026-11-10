---
title: "Compose Profile Vocabulary Policy"
version: "1.16.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-10"
layer: "operations"
artifact_id: "POL-0078"
created: "2026-09-04"
---

# Compose Profile Vocabulary Policy

## Overview

추적된 Compose profile의 이름·분류·목적을 소유한다. `include`는 파일을 병합하고
profile은 서비스를 선택한다. 여러 profile 선택은 합집합이며 보안 격리를 제공하지
않는다. 서비스 수는 구현에서 계산하며 본문에 고정하지 않는다.

## Scope

- **Systems**: 정상 root가 include하는 `infra/**/{compose,docker-compose}*.{yml,yaml}`와 독립 `labs/*/docker-compose.yml` entrypoint.
- **Optional overlays**: 아래 typed 계약으로 분류한 추적된 root 서비스 확장 소스. 독립 entrypoint나 새 서비스 inventory가 아니다.
- **Environments**: HOME, DEV, OPTIONAL, LAB 및 명시적 migration/maintenance 작업. LAB은 root의 profile 선택 대상이 아니다.

### Definitions

각 이름은 정확히 한 행, 한 category와 비어 있지 않은 purpose를 가진다.
`baseline`은 공통 출발점, `domain`은 기능 영역, `capability`는 선택 기능,
`role`은 사용 역할, `topology`는 배치 대안, `lifecycle`은 전환 단계,
`automation`은 부수 효과를 검토해야 하는 작업 선택이다. 서비스 명단은 현재
선언을 설명하며 실제 선택은 Compose에서 재확인한다.

| Profile | Category | Purpose | Selected services | Default? | Additional side effect | Lifecycle |
| --- | --- | --- | --- | --- | --- | --- |
| `admin` | domain | 데이터·로그·노트북 관리 UI | `dozzle`, `redisinsight` | No | normal service startup | current |
| `admin-data` | role | Valkey 데이터 탐색 UI | `redisinsight` | No | normal service startup | current |
| `admin-logs` | role | 컨테이너 로그 UI | `dozzle` | No | normal service startup | current |
| `ai` | domain | HOME 언어 AI와 vector 저장소; Open WebUI는 LAB `lab-open-webui`(ADR-0062 개정) | `qdrant`, `ollama`, `ollama-exporter` | No | normal service startup | current |
| `ai-image` | capability | GPU 이미지 생성 | `comfyui` | No | normal service startup | current |
| `ai-llm` | capability | 언어 모델 추론·검색 저장소 | `qdrant`, `ollama`, `ollama-exporter` | No | normal service startup | current |
| `alerting` | capability | 메트릭 경보 전달 | `prometheus`, `grafana`, `alertmanager` | No | normal service startup | current |
| `analytics-engineering` | capability | dbt 업무 원천 dev-pg 기반; dbt 작업은 LAB `lab-dbt`(SPEC-0262) | `dev-pg`, `dev-platform-provision`, `dev-pg-monitor-provision`, `dev-pg-exporter` | No | monitoring initialization: dev-pg-monitor-provision | current |
| `api-mock` | capability | 개발·기능 테스트용 HTTP stub 서버; bounded journal과 tracked mapping 제공 | `wiremock` | No | normal service startup; host 게시만 loopback 전용이며 project default network peer는 인증 없는 admin API에 접근 가능 | current |
| `auth` | domain | 접근 인증과 SSO | `keycloak`, `oauth2-proxy` | No | normal service startup | current |
| `availability` | capability | HTTP 가용성 점검 | `gatus` | No | normal service startup | current |
| `backup` | automation | Restic 백업·SQLite export·R2 offsite copy 작업; host timer와 명시적 명령만 실행 | `restic`, `restic-offsite`, `backup-sqlite-export` | No | backup repository and export staging writes when run; `restic-offsite`는 R2 원격 저장소에 추가만 함 | current |
| `bi` | capability | Superset metadata용 mng-pg 기반; Superset은 LAB `lab-superset`(SPEC-0262) | `mng-pg`, `mng-pg-init`, `mng-pg-monitor-provision`, `mng-pg-exporter` | No | initialization: mng-pg-init; monitoring initialization: mng-pg-monitor-provision | current |
| `blog-ingestion` | capability | 서버 A의 Blog-data 수집 Gateway; n8n-worker(수집)와 Traefik(Export·Attestation 정확한 경로)만 각자의 내부 격리망으로 접근 | `blog-ingestion` | No | 검토된 Blog-data `dev` 커밋으로 로컬 빌드한 이미지가 없으면 시작 실패 | current |
| `batch-metrics` | capability | 배치 작업 메트릭 수집 | `prometheus`, `grafana`, `pushgateway` | No | normal service startup | current |
| `cassandra` | topology | 독립 LAB 단일 Cassandra 노드; 내부망 무인증 | `cassandra-node1` | No | normal service startup; 실제 기동은 별도 승인 | current |
| `cdc` | capability | Debezium 원천은 dev-pg; 다른 관리 도구 metadata는 mng-pg에 유지 | `dev-pg`, `dev-platform-provision`, `dev-pg-monitor-provision`, `dev-pg-exporter`, `kafka-1`, `schema-registry`, `kafka-connect`, `debezium-db-provision`, `kafka-exporter` | No | initialization: debezium-db-provision (복제 role·grant·publication); connector 등록·snapshot은 별도 승인; monitoring initialization: dev-pg-monitor-provision | current |
| `contract-testing` | capability | Pact Broker 계약 저장·검증 결과와 feature 소유 DB 준비 | `mng-pg`, `mng-pg-init`, `mng-pg-monitor-provision`, `mng-pg-exporter`, `pact-broker-db-provision`, `pact-broker` | No | initialization: pact-broker-db-provision (role·database); pact 게시·검증 결과 쓰기; monitoring initialization: mng-pg-monitor-provision | current |
| `core` | baseline | 접근·인증·secret 기반과 관리 DB; HOME 앱 전체는 아님 | `traefik`, `keycloak`, `oauth2-proxy`, `openbao`, `openbao-agent`, `mng-valkey`, `mng-valkey-exporter`, `mng-pg`, `mng-pg-init`, `mng-pg-monitor-provision`, `mng-pg-exporter` | No | initialization: mng-pg-init; monitoring initialization: mng-pg-monitor-provision | current |
| `couchdb` | topology | 독립 LAB CouchDB 복제 구성과 초기화 | `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init` | No | initialization: couchdb-cluster-init | current |
| `crawl4ai` | capability | 격리 network의 token 보호 웹 crawler, `crawl4ai-egress` 출구 gateway와 `crawl4ai-loopback` host 전달기; 소비자 POL-0091 | `crawl4ai`, `crawl4ai-egress`, `crawl4ai-loopback` | No | normal service startup | current |
| `data-science` | capability | MLflow 추적과 그 provisioner; JupyterLab은 LAB `jupyterlab` profile(SPEC-0262) | `mng-pg`, `mng-pg-init`, `mng-pg-monitor-provision`, `mng-pg-exporter`, `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets`, `mlflow-db-provision`, `mlflow` | No | initialization: mlflow-db-provision, seaweedfs-buckets; monitoring initialization: mng-pg-monitor-provision | current |
| `dependency-update` | automation | Renovate 갱신 제안 작업; 명시적 실행만 허용 | `renovate` | No | remote dependency proposals when configured | current |
| `dev` | baseline | 개발 접근·관측·메일 캡처; HOME 최소 선택과 다름 | `traefik`, `keycloak`, `oauth2-proxy`, `openbao`, `openbao-agent`, `mng-valkey`, `mng-valkey-exporter`, `mng-pg`, `mng-pg-init`, `mng-pg-monitor-provision`, `mng-pg-exporter`, `prometheus`, `grafana`, `grafana-db-provision`, `node-exporter`, `cadvisor`, `gatus`, `mailpit` | No | initialization: mng-pg-init, mng-pg-monitor-provision, grafana-db-provision | current |
| `dev-data` | capability | 단일 개발 PG·Valkey와 그 지표 exporter를 명시적으로 선택 | `dev-pg`, `dev-pg-monitor-provision`, `dev-pg-exporter`, `dev-valkey`, `dev-valkey-exporter` | No | 새 개발 저장소 기동; 관리 DB·Valkey와 상태 분리; initialization: dev-pg-monitor-provision | current |
| `experience` | capability | 관리자 전용 공유 Storybook 정적 UI 검토와 원격 문서 MCP | `storybook`, `storybook-mcp` | No | 정적 origin startup; `unless-stopped` 재시작 정책은 명시적 중지 전 reboot에도 유지 | current |
| `graph` | role | 그래프 데이터 저장 | `neo4j` | No | normal service startup | current |
| `iac` | automation | OpenTofu와 Terrakube IaC 작업; apply는 별도 승인; Terrakube state는 `storage`와 함께 선택 | `opentofu`, `terrakube-api`, `terrakube-ui`, `terrakube-executor` | No | operator IaC execution | current |
| `jupyterlab` | topology | 독립 LAB `labs/jupyterlab/docker-compose.yml`의 token 보호 단일 사용자 notebook(SPEC-0262) | `jupyterlab` | No | `${LAB_DATA_DIR}/jupyterlab/work` bind; host port는 `LAB_HOST_BIND_IP`에만; MLflow endpoint는 선택 입력 | current |
| `lab-dbt` | topology | 독립 LAB `labs/dbt/docker-compose.yml`의 dbt 변환 작업(SPEC-0262) | `dbt-db-provision`, `dbt` | No | initialization: dbt-db-provision (role·grant·target schema); `dbt run`/`build`는 target schema 쓰기; `LAB_DBT_DB_HOST` 승인 전 렌더링 전용 | current |
| `lab-kafka` | topology | 독립 LAB Kafka 3-broker KRaft 구성·exporter·초기화 | `lab-kafka-1`, `lab-kafka-2`, `lab-kafka-3`, `lab-kafka-exporter`, `lab-kafka-init` | No | initialization: lab-kafka-init | current |
| `lab-lakehouse` | topology | 독립 LAB `labs/lakehouse/docker-compose.yml`의 Iceberg batch·유지보수, SQL 조회, streaming 적재, 데이터 품질 검사(SPEC-0262) | `seaweedfs-table-bucket`, `spark`, `trino`, `flink-jobmanager`, `flink-taskmanager`, `great-expectations` | No | initialization: seaweedfs-table-bucket (table bucket·policy·namespace); 기본 `spark` 명령은 namespace 조회만; S3·catalog endpoint 승인 전 렌더링 전용 | current |
| `lab-locust` | topology | root에서 분리된 Locust master/worker headless 부하 LAB | `lab-locust-master`, `lab-locust-worker` | No | `labs/locust/docker-compose.yml`의 별도 project/network/volume; target 승인 후에만 트래픽 생성 | current |
| `lab-open-webui` | topology | 독립 LAB `labs/open-webui/docker-compose.yml`의 채팅·RAG 웹; Keycloak native OIDC(ADR-0062 개정 2026-11-10) | `open-webui` | No | `${LAB_DATA_DIR}/open-webui/data` bind; host port는 `LAB_HOST_BIND_IP`에만; `LAB_OPEN_WEBUI_OLLAMA_BASE_URL` 승인 전 렌더링 전용 | current |
| `lab-superset` | topology | 독립 LAB `labs/superset/docker-compose.yml`의 Superset BI 웹; Keycloak native OIDC(SPEC-0262) | `superset-db-provision`, `superset-init`, `superset` | No | initialization: superset-db-provision (role·database), superset-init (migration·role 동기화·`lakehouse` DB 등록); `LAB_SUPERSET_DB_HOST` 승인 전 렌더링 전용 | current |
| `lakehouse` | capability | SeaweedFS S3·Iceberg REST catalog 저장소; 엔진은 LAB `lab-lakehouse`(SPEC-0262) | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets` | No | initialization: seaweedfs-buckets | current |
| `local` | baseline | 로컬 접근·인증·관리 DB와 메일 캡처 | `traefik`, `keycloak`, `oauth2-proxy`, `openbao`, `openbao-agent`, `mng-valkey`, `mng-valkey-exporter`, `mng-pg`, `mng-pg-init`, `mng-pg-monitor-provision`, `mng-pg-exporter`, `mailpit` | No | initialization: mng-pg-init; monitoring initialization: mng-pg-monitor-provision | current |
| `logs` | capability | 로그 수집·조회와 object 저장소 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets`, `loki`, `alloy`, `grafana` | No | initialization: seaweedfs-buckets | current |
| `mail-dev` | capability | 개발 SMTP 캡처 | `mailpit` | No | normal service startup | current |
| `mail-server` | topology | 독립 LAB `labs/stalwart/docker-compose.yml`의 자체 완결 메일 서버; relay 없음, SMTP는 LAB network에만, 관리 UI는 `LAB_HOST_BIND_IP` loopback 게시(SPEC-0262) | `stalwart`, `stalwart-config` | No | initialization: stalwart-config (도메인·listener·relay 금지 plan 적용; listener 변경은 재시작 후) | current |
| `messaging` | domain | Kafka broker·schema·connect·관리 UI | `kafka-1`, `schema-registry`, `kafka-connect`, `kafbat-ui`, `kafka-exporter`, `kafka-init` | No | initialization: kafka-init | current |
| `messaging-admin` | role | Kafka 관리 UI와 직접 종속 서비스 | `kafka-1`, `schema-registry`, `kafka-connect`, `kafbat-ui`, `kafka-exporter` | No | normal service startup | current |
| `messaging-broker` | role | Kafka 단일 broker·초기화·exporter | `kafka-1`, `kafka-exporter`, `kafka-init` | No | initialization: kafka-init | current |
| `messaging-connect` | role | Kafka Connect와 broker·schema 종속성 | `kafka-1`, `schema-registry`, `kafka-connect`, `kafka-exporter` | No | normal service startup | current |
| `messaging-schema` | role | Kafka schema registry | `kafka-1`, `schema-registry`, `kafka-exporter` | No | normal service startup | current |
| `mlops` | capability | MLflow 추적 서버와 feature 소유 DB·bucket 준비 | `mng-pg`, `mng-pg-init`, `mng-pg-monitor-provision`, `mng-pg-exporter`, `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets`, `mlflow-db-provision`, `mlflow` | No | initialization: mlflow-db-provision, seaweedfs-buckets; monitoring initialization: mng-pg-monitor-provision | current |
| `mng` | role | HOME 관리 DB·공유 broker·exporter | `mng-valkey`, `mng-valkey-exporter`, `mng-pg`, `mng-pg-init`, `mng-pg-monitor-provision`, `mng-pg-exporter` | No | initialization: mng-pg-init, mng-pg-monitor-provision | current |
| `mongodb` | topology | 독립 LAB MongoDB replica set과 초기화·관리 UI | `mongo-key-generator`, `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`, `mongo-init`, `mongo-express` | No | initialization: mongo-key-generator, mongo-init | current |
| `n8n-sandbox` | capability | n8n Assistant 코드 sandbox: 인증서 생성 job, sandbox API, privileged Docker-in-Docker runner(owner 결정 2026-11-09); 기본 선택에서 제외 | `n8n-sandbox-certs`, `n8n-sandbox-api`, `n8n-sandbox-runner-1` | No | initialization: n8n-sandbox-certs (mTLS 자료 생성) | current |
| `nginx` | topology | Traefik 대체 gateway; 기본 ingress port 중복 금지 | `nginx`, `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets` | No | initialization: seaweedfs-buckets | current |
| `notebook` | capability | Open Notebook과 SurrealDB 저장소 | `surrealdb`, `open_notebook` | No | normal service startup | current |
| `obs` | domain | 전체 관측 기능; HOME에 필요한 하위 선택만 권장 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets`, `prometheus`, `loki`, `tempo`, `alloy`, `grafana`, `grafana-db-provision`, `node-exporter`, `cadvisor`, `gatus`, `pyroscope`, `alertmanager`, `pushgateway` | No | initialization: seaweedfs-buckets, grafana-db-provision | current |
| `obs-core` | capability | 메트릭 수집·대시보드 | `prometheus`, `grafana`, `grafana-db-provision` | No | initialization: grafana-db-provision | current |
| `obs-gpu` | capability | NVIDIA GPU 메트릭 exporter; GPU·driver·Container Toolkit 필요 | `dcgm-exporter` | No | normal service startup; 모든 GPU 예약 | current |
| `obs-host` | capability | 호스트·컨테이너 자원 측정 | `node-exporter`, `cadvisor` | No | normal service startup | current |
| `ollama` | capability | 로컬 모델 추론과 exporter | `ollama`, `ollama-exporter` | No | normal service startup | current |
| `opensearch` | topology | 단일 OpenSearch와 dashboards | `opensearch`, `opensearch-dashboards` | No | normal service startup | current |
| `opensearch-cluster` | topology | 독립 LAB OpenSearch 다중 노드 대안 | `lab-opensearch-dashboards`, `opensearch-node1`, `opensearch-node2`, `opensearch-node3` | No | normal service startup | current |
| `postgres-ha` | topology | 독립 LAB Patroni·etcd PostgreSQL 실험 구성 | `etcd-1`, `etcd-2`, `etcd-3`, `pg-router`, `pg-cluster-init`, `pg-0`, `pg-1`, `pg-2`, `pg-0-exporter`, `pg-1-exporter`, `pg-2-exporter` | No | initialization: pg-cluster-init | current |
| `policy-check` | capability | Conftest Rego 정책 테스트; `infra/` read-only, network 없음 | `conftest` | No | 읽기 전용 검사; 쓰기 없음 | current |
| `profiling` | capability | 연속 프로파일 수집·조회 | `alloy`, `grafana`, `pyroscope` | No | normal service startup | current |
| `quality-results` | capability | 공용 시험 결과 `perf_db`와 명시적 one-shot provision | `dev-pg`, `dev-perf-provision`, `dev-pg-monitor-provision`, `dev-pg-exporter` | No | initialization: dev-perf-provision; HOME 실행·프로젝트 로그인 발급은 별도 승인; monitoring initialization: dev-pg-monitor-provision | current |
| `qdrant` | capability | vector 검색 저장소 | `qdrant` | No | normal service startup | current |
| `registry` | role | 개발 컨테이너 registry | `registry` | No | normal service startup | current |
| `sast` | topology | 독립 LAB `labs/sonarqube/docker-compose.yml`의 소스 정적 분석(SPEC-0262) | `sonarqube` | No | `${LAB_DATA_DIR}/sonarqube` bind; HOME mng-pg는 `LAB_SONARQUBE_DB_HOST` 승인 전 렌더링 전용 | current |
| `seaweedfs` | capability | 분산 파일·S3 호환 저장소 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets` | No | initialization: seaweedfs-buckets | current |
| `secrets` | role | OpenBao secret 관리·Agent | `openbao`, `openbao-agent` | No | normal service startup | current |
| `security` | domain | OpenBao 보안 기반 | `openbao`, `openbao-agent` | No | normal service startup | current |
| `storage` | role | HOME 단일 object 저장소와 bucket 초기화 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets` | No | initialization: seaweedfs-buckets | current |
| `storage-seaweedfs` | role | SeaweedFS object/file 저장 역할 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets` | No | initialization: seaweedfs-buckets | current |
| `surrealdb` | capability | 독립 multi-model 데이터 저장소 | `surrealdb` | No | normal service startup | current |
| `testing` | automation | k6 이미지 확인용 단발 job; root 기본 명령은 `version` | `k6` | No | 비트래픽 version job; 부하는 승인된 격리 runner에서만 실행 | current |
| `tooling` | capability | 개발 registry; SonarQube는 LAB `sast`(SPEC-0262) | `registry` | No | normal service startup | current |
| `tracing` | capability | 분산 trace 수집·조회와 object 저장소 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets`, `tempo`, `alloy`, `grafana` | No | initialization: seaweedfs-buckets | current |
| `valkey-cluster` | topology | 독립 LAB Valkey sharding 실험 구성 | `valkey-node-0`, `valkey-node-1`, `valkey-node-2`, `valkey-node-3`, `valkey-node-4`, `valkey-node-5`, `valkey-cluster-init`, `valkey-cluster-exporter` | No | initialization: valkey-cluster-init | current |
| `workflow` | domain | HOME Airflow·n8n·worker·runner | `airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`, `airflow-init`, `flower`, `airflow-statsd-exporter`, `n8n`, `n8n-worker`, `n8n-task-runner-worker`, `searxng` | No | initialization: airflow-init | current |
| `workflow-airflow` | capability | Airflow 스케줄링·worker·초기화 | `airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`, `airflow-init`, `flower`, `airflow-statsd-exporter` | No | initialization: airflow-init | current |
| `workflow-n8n` | capability | n8n 자동화와 worker·task runner·Assistant 웹 검색 | `n8n`, `n8n-worker`, `n8n-task-runner-worker`, `searxng` | No | normal service startup | current |

## Rules

`Default? = No`는 직접 service target, CLI profile, `COMPOSE_PROFILES` 활성화가
없는 기동에서는 자동 선택되지 않는다는 뜻이다. 직접 지정한 service는 profile을
켜지 않아도 실행될 수 있다. 선택 의미는 [시스템 Guide](../../guides/01-common/0099-system-operations.md#selection-and-readiness)를 따른다.
일반 서비스 기동도 데이터 쓰기를 유발할 수 있다. 추가 부수 효과 열은 초기화·작업·
host mount를 별도로 표시하며 실행 승인을 대신하지 않는다.
`Lifecycle = current`는 추적된 현행 selector라는 뜻이며 HOME 기본 기동·필수성·운영 준비 완료를 뜻하지 않는다. `MIGRATE`는 승인된 전환 작업에만 사용한다.

- **Required**: 정상 root와 각 LAB의 모든 서비스는 명시적 profile을 가져야 한다. 새 이름은 같은 변경에서
  표에 추가하고 마지막 소비자가 은퇴하면 표에서 제거한다. 이름 중복·누락·유령 행을
  허용하지 않는다. 필수 `depends_on` 폐포가 선택 안에서 닫혀야 한다.
- **Allowed**: 한 서비스가 여러 profile에 속할 수 있다. 선택형 대안 종속성은
  `required: false`를 쓸 수 있지만 앱의 실제 endpoint 설정과 일치해야 한다.
- **Disallowed**: 검증되지 않은 broad profile을 HOME 기동 명령으로 사용하거나,
  부수 효과가 있는 update/IaC/load-test 작업을 상시 기동하는 것. LAB 파일을
  root에서 include하거나 LAB profile을 HOME 이름 선택에 넣는 것.

### Typed optional root overlays

선택형 overlay는 `x-hyhome-overlay: {version: 1, base: <repository-relative-path>}`로
역할을 명시한다. 이는 작성된 소스의 분류이며 이미지·권한·실행 준비 수용이 아니다.
파일 이름이나 `override` 접미사만으로 일반 Compose 검사를 면제하지 않는다.

- `version`은 정수1이며 `base`는 비어 있지 않은 저장소 상대 경로다. 절대 경로,
  경로 탈출과 symlink를 허용하지 않는다. base는 추적된 일반 파일이며 정상 root의
  include 집합에 속하고, 다른 overlay가 아닌 유효한 Compose 서비스 원본이어야 한다.
- overlay 자신은 정상 root include에 들어가지 않는다. `services`는 비어 있지 않은
  mapping이며 모든 서비스 이름이 해당 base의 서비스 집합 안에 있어야 한다.
  새 서비스 이름이나 서비스별 `profiles` 재정의는 거부한다.
- `base: docker-compose.yml`인 예외는 정상 root가 include하는 추적된 일반 서비스
  membership만 대상으로 한다. 이 root-base form은 network-only service override다.
  각 `services.<name>` mapping은 정확히 비어 있지 않은 `networks` key 하나만 가지며,
  attachment는 `network-name: {}` 형식만 허용한다. 변경된 각 서비스는 새 internal
  network 하나 이상에 연결해야 하고, 기존 root network 참조는 worker의 `dev_data_net`
  처럼 함께 둘 수 있다. image, build, privileged, command, entrypoint, volumes, ports,
  secrets, depends_on, network_mode 및 다른 runtime field는 금지한다. Compose의
  `!reset` 및 `!override` replacement/reset tag도 이 root-base form에서는 금지한다.
- 이 경우에만 overlay는 기존 root network 정의에 없는 비어 있지 않은 새 이름의
  top-level network를 `internal: true`만으로 선언할 수 있다. 모든 새 network는 위
  서비스에서 참조해야 한다. `external`, `name`, `driver`, `driver_opts`, `ipam` 또는
  다른 network 속성 및 기존 root network 정의의 수정은 허용하지 않는다. 이 예외는
  profile, root `include`, service inventory 권한을 만들지 않는다. leaf-base overlay는
  기존 runtime 및 Compose tag semantics를 그대로 따른다.
- 위의 좁은 경우 외에는 top-level network·volume·secret·config 선언, `include` 및
  독립 project 선언을 추가하지 않는다. 서비스 변경과 YAML 재사용용 `x-` extension만
  허용하며, extension이 별도 profile 또는 서비스 분류 권한을 만들지 않는다.
- 검토한 root와 overlay를 순서대로 명시한 `-f` 조합에서 기존 서비스 profile을
  상속한다. overlay만으로 기동하지 않으며, 상속 대상 서비스의 Guide와 inventory
  행을 중복 생성하지 않는다. 실제 조합의 선택·렌더링 검증은 별도로 수행한다.
- marker의 형식·버전·base·서비스 경계가 잘못되면 fail-closed로 보고한다.
  유효하지 않은 marker를 선택형 면제로 처리하거나 단순히 무시하지 않는다.

이 계약은 일반 root/LAB 서비스의 명시적 profile 의무를 유지한다. Overlay 분류
성공만으로 공급자 이미지, 설치 dependency, DB/S3 grant, private 파일 전달이나
DEV/HOME 실행·복구가 검증된 것은 아니다.

### HOME activation

| Named selection | Profiles | Forbidden categories |
| --- | --- | --- |
| HOME | `core`, `mng`, `ai`, `workflow`, `obs-core`, `obs-host`, `availability`, `logs`, `alerting`, `storage`, `tracing`, `profiling`, `obs-gpu`, `registry` | `automation`, `lifecycle`, `topology` |

`dev-data`는 `dev`·`local`에 포함되지 않는다. 현재 선택은 위 HOME 행과 소유자가 승인한
exact profile을 따르며, 과거에 관측된 profile 조합은 현재 activation 권한이 아니다.

HOME selector 계획은 `--dev-data-expected on`일 때만 위 profile에 `dev-data`를
더한다. 이 값은 root `.env`의 `PROMETHEUS_DEV_DATA_EXPECTED`와 같아야 하며, 다르면
Prometheus 시작 스크립트가 거부한다. `off`이면 HOME 행 그대로이고 DEV 저장소는
선택하지 않는다. 2026-11-09 소유자가 DEV 데이터를 상시 운영하는 HOME에서
selector 기동이 가능하도록 이 선택을 승인했다.

HOME은 위 profile의 이름 있는 선택이며 새 Compose profile이 아니다. 이 선택은 HOME
후보 선택이다. 사용자가 AI와 workflow 상시 필요를 확인했으므로 관리 DB·공유
broker·영속 저장소·관측 종속성을 함께 유지한다. `core`만으로 HOME 앱이 충족되지는
않는다. SPEC-0182 W6(2026-09-25)에서 소유자가 HOME 설정이 이미 전송·수집하는
`tracing`(Tempo), `profiling`(Pyroscope), `obs-gpu`(DCGM exporter)와 기본 사용할
`registry`를 HOME에 추가했다. 그 밖의 새 HOME profile은 추가하지 않는다. OpenBao bootstrap/unseal/Agent 인증,
DB 초기화, 실제 자원 측정 및 backup/restore는 별도 준비 조건이다. config 성공은
무인 재기동이나 live readiness를 증명하지 않는다.

### HOME Compose overlay 등록부와 적용 규칙

이 절이 overlay 적용 규칙의 유일한 소유자다. 다른 문서는 이 절을 링크하고 규칙을
다시 쓰지 않는다. 절차는
[RUN-0098](../../runbooks/01-common/0098-cold-start-and-reboot.md#overlay-적용과-root-compose_file-점검-owner-run)이 소유한다.

- 어떤 overlay도 root `.env`의 `COMPOSE_FILE`로 적용하지 않는다. HOME의 `COMPOSE_FILE`은
  `docker-compose.yml` 하나이거나 미설정이다. 소유자는 평문 `docker compose`를 쓰므로
  HOME에서 항상 실행돼야 하는 변경은 overlay가 아니라 base Compose 파일에 둔다.
- 유지보수·롤백처럼 일시적인 overlay는 파일로 남기고, 해당 Runbook 절차 안에서
  명시적 `-f docker-compose.yml -f <overlay>`로만 적용한다. 절차가 끝나면 base만으로
  서비스를 다시 만든다. 실행 프로세스의 `COMPOSE_FILE` 환경 변수는 적용 근거가 아니다.
- 선택기(`scripts/lib/ops/compose_start.py`)는 `.env`의 `COMPOSE_FILE`이
  `docker-compose.yml` 외의 값이면 값을 출력하지 않고 `compose_file_overlay_forbidden`으로
  fail-closed 거부한다.
- 등록부의 기계 판독 원본은 `infra/compose-overlays.json`이다. `x-hyhome-overlay`
  marker를 가진 추적 파일은 모두 이 표와 JSON에 한 변경으로 함께 등록한다.
  `tests/validation/test_compose_overlay_register.py`가 marker 파일·JSON·이 표의 불일치를
  실패로 보고한다.
- 필수 입력은 이름만 쓰며 값은 문서·로그·`.env.example`에 쓰지 않는다. 입력은 overlay를
  적용하기 전에 준비한다.
- HOME 상시 변경이던 n8n Valkey ACL(`mng-valkey`), n8n Worker와 Ollama 사이
  `n8n_ollama_net`, Opsflow manifest-pipeline의 Airflow 코드 mount·Worker 망과
  `OPSFLOW_SECRET_DIR` mount는 base 파일로 합쳤고 overlay 파일은 없다.
- 선택형 서비스 확장의 형식은 위 [Typed optional root overlays](#typed-optional-root-overlays)가 정한다.

| Overlay | Base | 목적 | 필수 입력(이름만) | 적용 방식 | 소유 문서 |
| --- | --- | --- | --- | --- | --- |
| `infra/07-workflow/n8n/workloads/manifest-outbox-notifier/compose.workflow.override.yml` | `docker-compose.yml` | n8n manifest outbox notifier 망 | 없음 | 명시적 `-f`, HOME 미적용 | [RUN-0053](../../runbooks/08-workflows-and-automation/0053-n8n.md) |
| `infra/08-ai/comfyui/docker-compose.egress.yml` | `infra/08-ai/comfyui/docker-compose.yml` | ComfyUI 외부 망(유지보수 한정) | 없음 | 명시적 `-f`, HOME 미적용 | [RUN-0081](../../runbooks/09-ai-and-search/0081-comfyui.md) |
| `infra/01-gateway/traefik/compose.window-ca.override.yml` | `infra/01-gateway/traefik/docker-compose.yml` | Traefik owner-window CA mount | 없음 | 명시적 `-f`, owner window 한정 | [RUN-0105](../../runbooks/04-security-and-secrets/0105-openbao-maintenance-window.md) |

### Companion, exclusion and side effects

Producer의 모든 profile은 기존 Exporter와 필요한 monitor provision job을 함께
선택한다. 선택 범위가 늘어난 `core`·`local`·기능 profile도 monitor Secret과
provisioning 권한을 먼저 준비한다. 아래 직접 Target 목록은 같은 profile의 다른
서비스가 자동 시작된다고 가정하지 않는다. 실제 기동은 해당 Runbook의 승인·
readiness·백업 조건을 확인한 뒤에만 `up -d <목록>`으로 수행한다. Producer에서
Exporter로 역방향 `depends_on`을 추가하지 않는다. 이 조건은 `depends_on`으로
암묵적으로 기동하는 Producer에도 적용한다. 예를 들어 `mng-pg-init`이나
`kafka-connect`만 Target한 의존성 closure에는 Exporter가 빠지므로 해당 Producer의
아래 companion 목록을 target 합집합에 포함한다. 이 계약은 임의 Docker CLI 명령을
가로채는 장치가 아니며 bare Producer 기동 자체를 Compose 오류라고 주장하지 않는다.
관측 선택을 HOME 전체와 맞추려면 `--target`이 아니라 `--selection HOME`으로 계획한다.

| Producer | Explicit targets |
| --- | --- |
| `mng-pg` | `mng-pg mng-pg-monitor-provision mng-pg-exporter` |
| `mng-valkey` | `mng-valkey mng-valkey-exporter` |
| `dev-pg` | `dev-pg dev-pg-monitor-provision dev-pg-exporter` |
| `dev-valkey` | `dev-valkey dev-valkey-exporter` |
| `kafka-1` | `kafka-1 kafka-exporter` |
| `ollama` | `ollama ollama-exporter` |
| `airflow-apiserver` | `airflow-apiserver airflow-scheduler airflow-dag-processor airflow-triggerer airflow-worker airflow-statsd-exporter` |
| `airflow-scheduler` | `airflow-scheduler airflow-statsd-exporter` |
| `airflow-triggerer` | `airflow-triggerer airflow-statsd-exporter` |
| `airflow-dag-processor` | `airflow-dag-processor airflow-statsd-exporter` |

Airflow, n8n, OAuth2 Proxy는 공유 `mng-valkey`를 쓰며 앱별 전용 Valkey와 Exporter는
없다(ADR-0062 결정 10). n8n 내장 metrics와 Kafka JMX Agent는 별도 Exporter를 중복
생성할 이유가 아니다. `up=1`은 scrape 성공만 뜻하고 `redis_up`/`pg_up`·업무 실행·
Grafana query와 선택 profile의 예상 상태는 별도로 확인한다.

| Selection | Constraint |
| --- | --- |
| nginx with core/local/dev | 기본 ingress 80/443 중복을 해소하거나 gateway 하나만 선택 |
| lab-kafka | `labs/kafka-cluster/docker-compose.yml`의 별도 project·cluster ID·data directory가 필요하다. 3 broker, replication factor 3, `min.insync.replicas=2`로 같은 host의 broker 하나 손실을 견디지만 host HA가 아니다. HOME `kafka-1`은 replication factor 1의 단일 broker이며 장애 내성이 없다 |
| lab-locust | `labs/locust/docker-compose.yml`의 별도 project·network·scenario/result volume을 사용하며 root `testing` profile에 포함되지 않음 |
| opensearch with opensearch-cluster | 서로 다른 Compose project의 대체 토폴로지; LAB은 별도 network·state·credential을 사용 |
| dependency-update | Renovate 전용 작업; tooling/HOME의 암묵적 기동 대상이 아님 |
| testing | root는 k6 버전만 확인; 격리 runner의 부하·샘플 데이터 생성은 대상과 실행량을 별도 승인 |
| iac | OpenTofu/Terrakube 명령·대상·credential·apply 승인 확인 |
| tooling | root는 registry만 선택; SonarQube는 LAB `sast` profile로 `labs/sonarqube/docker-compose.yml`에서만 선택; update/IaC/load 작업 제외 |
| mlops / data-science / analytics-engineering / cdc / contract-testing / bi | 도구 metadata는 `mng-pg`·`mng-pg-init`을 사용한다. dbt·CDC 업무 원천은 `dev-pg`·`dev-platform-provision`을 요구한다. dbt·Superset LAB은 HOME network에 합류하지 않으므로 같은 profile 이름의 root 선택은 그 DB를 LAB에 도달 가능하게 만들지 않는다. 기능 SQL·credential은 각 feature job 소유이며 기본 `mng-pg-init`은 그 secret을 읽지 않는다 |
| cdc with dev-pg | 새 원천의 publication·slot·offset·snapshot은 이전 mng-pg LSN에서 이어지지 않는다. connector 등록과 writer/reader 전환은 별도 승인 후 시행한다 |
| obs-gpu | GPU·driver·Container Toolkit 없는 host에서는 기동 실패; 선택해도 수집 성공을 증명하지 않음 |
| crawl4ai | internal network만 사용하고 외부로는 `crawl4ai-egress`만 통과; 소비자는 승인된 변경으로 `crawl4ai_net`에 합류 |
| n8n-sandbox | runner만 `privileged`(예외: `infra/common-optimizations.exceptions.json`, Conftest, p02 시험); host port·Traefik route·host Docker socket 없음; runner는 n8n 망에 합류하지 않고 API와 `n8n_sandbox_runner_net`, 인터넷과 `n8n_sandbox_outbound_net`만 사용; secret 파일 3개가 있어야 기동 |
| contract-testing | UI·API는 plain HTTP basic auth이므로 host port는 `127.0.0.1`에만 게시하고 route를 추가하지 않음; heartbeat만 공개 |
| lakehouse | 엔진은 `labs/lakehouse/docker-compose.yml` LAB에만 있고 HOME S3·catalog는 `LAB_LAKEHOUSE_*` 입력으로만 찾는다. `spark`는 one-shot 작업이며 `up`은 namespace 조회만 수행; 테이블 쓰기·`rewrite_data_files`·`expire_snapshots`는 `run --rm spark`로 대상 table을 명시. `trino`는 인증 없는 HTTP API이므로 host port는 `127.0.0.1`에만 게시하고 route를 추가하지 않음. `flink-*`도 같으며 REST JAR 업로드는 끔(`web.submit.enable=false`); Flink는 HOME `kafka_net`에 합류하지 않으며 Kafka에는 승인된 도달 가능 endpoint가 필요. `great-expectations`는 one-shot이며 기본 명령은 suite 목록만 출력 |
| bi | Superset LAB은 gateway route 없이 `LAB_HOST_BIND_IP`의 `LAB_SUPERSET_HOST_PORT`에만 게시; native OIDC redirect의 LAB origin 등록은 미결정; 가입 사용자는 `Gamma`(데이터 접근 없음) |
| api-mock | 인증 없는 admin API가 있으므로 host port는 `127.0.0.1`에만 게시하고 route를 추가하지 않음; 컨테이너 소비자는 project default network에서 `wiremock:8080` 사용 |
| experience | Storybook은 `internal: true`인 `experience_ingress_net`에만 연결; Traefik만 이 망과 `edge_net`을 함께 사용. 원격 문서 MCP `storybook-mcp`는 `edge_net`에서 Keycloak issuer를 읽고 Traefik TLS 뒤에서 자기 URL을 audience로 가진 `/admins` bearer token만 받음. HOME 기본 선택에는 포함하지 않음. 브라우저는 기존 `/admins` 인증을 먼저 수행 |
| api-mock load mode | root Compose와 `infra/11-quality/wiremock/wiremock.load.yml`을 같은 model로 결합해 같은 `api-mock` profile의 `wiremock` 설정을 대체; host port와 request journal이 없으며 mock performance만 판정 |

### LAB lifecycle and budget

- profile은 서비스 선택일 뿐 보안 경계가 아니다. 정상 root에서 서비스 이름을 직접
  지정하면 profile과 무관하게 그 서비스가 선택된다. LAB은 root에 없으므로 root의
  `--profile '*'`나 서비스 이름 지정으로 선택되지 않으며 `tests/validation/test_lab_isolation.py`가
  이를 검사한다. 같은 host의 LAB은 network와 data를 분리할 뿐 host 장애 내성은 없다.
- LAB 기동·종료는 `python3 scripts/operations/lab.py`만 사용한다. `up`은 목적과
  `LAB_MAX_LEASE_MINUTES` 이하의 lease를 요구하고, 실행 전 rendered root, 함께 선택한
  LAB, 실행 중 container와의 container·network·host port·쓰기 data 경로 충돌을 거부한다.
  LAB data root가 HOME data 경로와 겹쳐도 거부한다.
- 예산은 실행 중 container와 선택 LAB의 선언 reservation(`deploy.resources.reservations`) 합계에
  [POL-0107](../15-labs/0107-lab-promotion.md#external-workload-allowance)의 외부 workload
  allowance를 한 번 더한 값을 `LAB_HOST_BUDGET_CPUS`·`LAB_HOST_BUDGET_MEMORY_MIB`와 비교하고, 동시
  LAB 수를 `LAB_MAX_CONCURRENT`(기본 1)로 제한한다. 값이 비어 있거나 숫자가 아니면 거부한다.
  render가 없는 실행 중 Compose project, reservation 또는 limit이 없는 서비스는 합할 수 없어
  거부 사유로 보고한다. reservation은 측정 전에는 limit과 같으며 실측이 아니다. 2026-10-08 HOME은
  선언 한도만으로 host(12 CPU, 31 GiB)를 초과했으므로 운영자는 overcommit을 명시한 예산을
  정한다. GPU는 선언 한도에 없으므로 ComfyUI·Ollama 동시 사용은 DCGM의 VRAM 여유를 확인한 뒤
  결정한다. 실측 없이 절감량을 발표하지 않는다.
- `down`은 그 LAB project만 `-v` 없이 정지한다. LAB data와 volume 삭제는 ledger
  (`${LAB_DATA_DIR}/.ledger/<lab>.json`)에 기록된 경로만 대상으로 별도 승인 후 수행하며
  `docker volume prune`·`system prune`은 사용하지 않는다. 만료 lease는 `lab.py reap`이
  정지한다.
- AI·workflow HOME 상주 결정은 유지한다. LAB, lakehouse·analytics 대량 작업, GPU 이미지
  생성은 위 예산 검사와 별도 승인으로 켠다.

### Optional service disposition

#### Current-source reconciliation (P09, 2026-11-03)

이 표는 현재 공개 Compose와 당시 host 관찰을 함께 읽는 운영 안내이며, 삭제 권한이나
현재 운영 성공의 정본이 아니다. P09는 15개 역할 비교에서 현재 source와 named consumer를
확인할 수 있는 행만 채택 근거로 사용하고, 소비자·소유자·보존 또는 복구 근거가 없는 행은
`UNKNOWN`으로 남긴다. 역사 ADR 본문은 보존한다. 특히 ADR-0005의 RabbitMQ, ADR-0006의
MinIO 및 ADR-0010의 MailHog 표기는 당시 결정 문맥이며, 현행 source의 Kafka/SeaweedFS/Mailpit
선택을 대체하거나 현재 설치·전이 의존성 부재를 증명하지 않는다.

2026-10-08 host 관찰은 `docker ps`의 `hy-home-infra` 서비스 목록이며 이후 상태를
보장하지 않는다. "미실행"은 그 시점 관찰이다. 비용은 `.env.example`로 렌더링한 root의
선언 상한(CPU 합계 / 메모리 MiB 합계)이며 측정값이 아니다. 보존 데이터는 그 그룹의
named volume 또는 bind 경로이고, 퇴역 시 함께 다룰 상태다.

| Service group | Role | Consumer | 비용(CPU / MiB) | 보존 데이터 | Decision | 퇴역 조건 | Host 2026-10-08 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Traefik | 기본 ingress·TLS·ForwardAuth | 모든 routed UI | 1 / 512 | 없음(설정은 Git) | HOME 유지 | 대체하지 않음 | 실행 |
| Nginx | 대체 gateway 실습 | 이름 있는 소비자 없음 | 0.5 / 256 | 없음 | OPTIONAL `nginx`; 80/443을 Traefik과 공유하므로 HOME 선택에 넣지 않음 | 실습 수요가 없으면 퇴역 검토 | 미실행 |
| Loki | HOME 로그 저장·Grafana 조회 | Alloy, Grafana | 2 / 2048 | `loki-data` | HOME 유지 | 로그 수집을 다른 backend로 옮길 때 | 실행 |
| Dozzle | 실시간 container 로그 UI | 운영자 | 1 / 512 | `dozzle-data` | OPTIONAL `admin`; 상주는 소유자 선택 | Grafana Loki 조회로 충분해질 때 | 실행 |
| OpenSearch (single) | 전문 검색·분석 실험 | 이름 있는 소비자 없음 | 3 / 2560 | `opensearch-data`, `opensearch-dashboards-data` | OPTIONAL on-demand; 상주하지 않음 | 검색 소비자가 없으면 퇴역 검토 | 미실행 |
| Airflow | 예약 batch·backfill DAG | DAG, Flower | 10 / 9472 | `airflow-dags`·`-config`·`-plugins`·`-logs` | HOME 유지 | 예약 DAG가 없어질 때 | 실행 |
| n8n | 외부 이벤트·webhook·알림 | workflow | 5 / 4608 | `n8n-data`, task runner volume | HOME 유지 | 이벤트 workflow가 없어질 때 | 실행 |
| Mailpit | 개발 SMTP 캡처 | 앱 메일 시험 | 1 / 512 | `mailpit-data` | DEV on-demand | 메일 시험이 없을 때 | 미실행 |
| Stalwart | 실제 메일 서버 | 이름 있는 소비자 없음 | 1.5 / 768 | `stalwart-data`(SPEC-0262 이후 `${LAB_DATA_DIR}/stalwart/data`) | 2026-11-04 LAB `labs/stalwart/docker-compose.yml`로 이전 | 메일 수신 계획이 없으면 퇴역 검토 | 미실행 |
| Kafka `kafka-1`, Schema Registry, Connect, kafbat UI | 단일 broker 메시징·CDC | Debezium Avro connector, kafbat | 7 / 5632 | `kafka-1-data`, `kafka-connect-data` | OPTIONAL `messaging`·`cdc`; Avro 소비자가 있으므로 Schema Registry 유지 | CDC·메시징 소비자가 없어질 때 | 실행 |
| Spark, Flink, Trino, Great Expectations | lakehouse batch·stream·query·검증 | lakehouse 작업 | 8 / 7936 | `flink-checkpoints`(SPEC-0262 이후 `${LAB_DATA_DIR}/lakehouse/flink/checkpoints`); 데이터는 object store | 2026-11-04 LAB `labs/lakehouse/docker-compose.yml`로 이전; one-shot·예산 검사 | 기능·학습 시나리오가 없을 때 선택하지 않음 | 미실행 |
| Superset | BI | 운영자 | 2.5 / 1792 | MNG PostgreSQL DB | 2026-11-04 LAB `labs/superset/docker-compose.yml`로 이전 | 대시보드 소비자가 없을 때 | 미실행 |
| Open WebUI | 채팅·RAG UI | 사용자 1명, 마지막 활동 2026-10-26 | 2 / 2048 | `open-webui`(이전 후 `${LAB_DATA_DIR}/open-webui/data`) | 2026-11-10 LAB `labs/open-webui/docker-compose.yml`로 이전; HOME 컨테이너·volume 퇴역은 별도 승인 | 채팅 실험 수요가 없을 때 | 실행 |
| Neo4j | graph | 이름 있는 소비자 없음 | 1 / 512 | `neo4j-data` | OPTIONAL | graph 시나리오가 없으면 퇴역 검토 | 미실행 |
| RedisInsight | Valkey UI | 운영자 | 1 / 512 | `redisinsight-data`(연결 정의) | OPTIONAL `admin` | Valkey 조회 수요가 없을 때 | 실행 |
| Terrakube | IaC server | 운영자 | 4 / 3072 | MNG PostgreSQL DB | DEV; 상주 금지 | IaC 실습이 없을 때 | 미실행 |
| JupyterLab, MLflow | data science·실험 추적 | MLflow는 JupyterLab | 3.5 / 3328 | MNG PostgreSQL DB, object store artifact | MLflow OPTIONAL; JupyterLab은 2026-11-04 LAB `labs/jupyterlab/docker-compose.yml`로 이전 | 실험 추적 수요가 없을 때 | 미실행 |
| Open Notebook, SurrealDB | notebook | 이름 있는 소비자 없음 | 1.5 / 768 | `open-notebook-data`, `surrealdb-data` | OPTIONAL | 소비자가 없으면 퇴역 검토 | 미실행 |
| Crawl4AI | crawling API | 없음 | 2 / 4096 | 없음 | OPTIONAL; 소비자가 생기지 않으면 퇴역 검토 | 다음 검토까지 소비자가 없을 때 | 미실행 |
| ComfyUI | GPU 이미지 생성 | 명시 선택 `ai-image` | 2 / 4096 | `comfyui-models` 등 7개 volume | HOME 제외(소유자 2026-11-09); GPU를 Ollama와 공유 | 이미지 생성 수요가 없을 때 | 중지 |
| Pact Broker, SonarQube | contract·SAST | 이름 있는 소비자 없음 | 3.5 / 2816 | `sonarqube-*` volume, MNG PostgreSQL DB | Pact Broker OPTIONAL; SonarQube는 2026-11-04 LAB `labs/sonarqube/docker-compose.yml`로 이전 | 계약·SAST 소비자가 없을 때 | 미실행 |
| 독립 `labs/*/docker-compose.yml` | HA·replica·backend·부하 실습 | 실습 목적별 | LAB별 렌더 | `LAB_DATA_DIR` 아래 LAB별 경로 | LAB; `lab.py`로만 실행 | 실습 목적이 없어지면 해당 LAB 퇴역 | `hy-home-lab-*` project 없음 |

LAB 안의 exporter(`pg-*-exporter`, `valkey-cluster-exporter`, `lab-kafka-exporter`)는 LAB
내부 network에만 있으며 HOME Prometheus가 수집하지 않는다(`test_lab_isolation`). 실습 중
`docker exec`로 직접 조회하는 용도다. 소비자도 실행 가능한 image도 없던 MongoDB LAB
exporter는 퇴역했다(SPEC-0215).

이 표는 서비스를 삭제하지 않는다. 퇴역은 소비자 부재를 다시 확인한 별도 변경에서
source·문서·secret을 함께 제거한다.

## Exceptions

정상 root profile은 같은 daemon, network, disk, GPU를 공유할 수 있다. 여러
노드는 물리
고가용성을 증명하지 않는다. 알려진 조합 제약을 숨기기 위해 검증을 우회하지
않으며 승인된 예외는 이유·범위·복구·종료 조건을 current Task에 기록한다.

### Review Cadence

- **Owner**: @buenhyden. Infra/DevOps 역할은 책임 설명이다.
- **Cadence**: profile 또는 서비스 선언을 변경할 때.
- **Trigger**: 서비스 추가·은퇴, topology·host port·작업 부수 효과 변경.

### Traceability

- [Workspace catalog](../../README.md)
- [Independent LAB entrypoints](../../../../labs/postgresql-ha/README.md)
- Convergence specification: SPEC-0180 (retired)
- [Runtime version projection](../../../../infra/tech-stack.versions.json)
- Original enablement decision: SPEC-0156 (retired)
- Sibling resolution: SPEC-0171 (retired)

## Verification

```bash
bash scripts/validation/validate-docker-compose.sh
python3 scripts/validation/check-operations-catalog.py
```

첫 명령은 정상 root의 profile 렌더링과 port 중복을 검사한다. 각 LAB은
`python3 scripts/operations/lab.py check <topology>`로 별도 검증한다. controller는
비공개 `labs/.env`를 기본 입력으로 사용한다. `labs/.env.example`은 빈 required 값을
포함할 수 있는 문서 예시이므로 실행 가능한 render 입력으로 취급하지 않는다. 자동화가
public synthetic env를 쓰면 `--env-file <prepared-public-env>`와 HOME에 겹치지 않는
임시 `LAB_DATA_DIR` 및 필요한 공개 입력·read-only fixture를 함께 준비하고 종료 후
정리한다.
실행 전 LAB 전용 변수와 secret 참조는 `labs/.env.example`, LAB별 README 및
`secrets/labs/` 계약을 확인한다. 두 번째는 정상
root에 포함된 infra Compose와 독립 LAB Compose의 profile 이름·서비스 표 일치,
category/purpose, 중복 행, root include 배제, 명시적 서비스 profile, HOME 안전
category와 필수 dependency 폐포를 검사한다.
숫자 Services 열을 추가한다면 실제 선언 수와 일치해야 한다. 은퇴한 snapshot은
검증 입력이 아니다. 첫 명령의 기본 모드는 HOME 조합도 함께 렌더링하여 profile
사이에만 나타나는 host port 충돌을 같은 검사로 확인한다.

검사에 앞서 [RUN-0086](../../runbooks/10-platform-and-backup/0086-dependency-version-management.md#static-configuration-validation)의
임시 입력 생성·private 읽기 경계를 확인한다. `HYHOME_COMPOSE_PROFILES` override는
기본 every-profile/HOME 검사를 지정 합집합 하나로 바꾸므로 실제 범위를 기록한다.
선택 closure 성공은 optional dependency의 앱 endpoint나 provisioning 완료를
보장하지 않는다. 예를 들어 Grafana DB provisioning 선택과 실제 앱 사용 준비는
[Grafana Guide](../../guides/07-observability/0041-grafana.md)에서 확인한다.

## Related Documents

- [Infrastructure optimization governance](0006-infrastructure-optimization-governance.md)
- [Developer environment](../../guides/10-platform-and-backup/0002-developer-environment.md)
