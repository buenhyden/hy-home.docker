---
title: "Compose Profile Vocabulary Policy"
version: "1.11.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-07"
layer: "operations"
artifact_id: "POL-0078"
created: "2026-09-04"
---

# Compose Profile Vocabulary Policy

## Overview

### Overview

추적된 Compose profile의 이름·분류·목적을 소유한다. `include`는 파일을 병합하고
profile은 서비스를 선택한다. 여러 profile 선택은 합집합이며 보안 격리를 제공하지
않는다. 서비스 수는 구현에서 계산하며 본문에 고정하지 않는다.

## Scope

### Policy Scope

- **Systems**: 정상 root가 include하는 `infra/**/{compose,docker-compose}*.{yml,yaml}`와 독립 `labs/*.yml` entrypoint.
- **Environments**: HOME, DEV, OPTIONAL, LAB 및 명시적 migration/maintenance 작업. LAB은 root의 profile 선택 대상이 아니다.

### Traceability

- [Workspace catalog](../README.md)
- [Independent LAB entrypoints](../../../labs/postgresql-ha.md)
- [Convergence specification](../../98.archive/completed/03.specs/0180-home-dev-convergence/spec.md)
- [Runtime version projection](../../../infra/tech-stack.versions.json)
- [Original enablement decision](../../98.archive/completed/03.specs/0156-compose-enablement-model-convergence/spec.md)
- [Sibling resolution](../../98.archive/completed/03.specs/0171-compose-sibling-pair-resolution/spec.md)

## Rules

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
| `ai` | domain | HOME 언어·이미지 AI와 vector 저장소 | `qdrant`, `ollama`, `ollama-exporter`, `open-webui`, `comfyui` | No | normal service startup | current |
| `ai-image` | capability | GPU 이미지 생성 | `comfyui` | No | normal service startup | current |
| `ai-llm` | capability | 언어 모델 추론·채팅·검색 저장소 | `qdrant`, `ollama`, `ollama-exporter`, `open-webui` | No | normal service startup | current |
| `alerting` | capability | 메트릭 경보 전달 | `prometheus`, `grafana`, `alertmanager` | No | normal service startup | current |
| `analytics-engineering` | capability | dbt 업무 원천은 dev-pg; 다른 관리 도구 metadata는 mng-pg에 유지 | `dev-pg`, `dev-platform-provision`, `dbt-db-provision`, `dbt` | No | initialization: dbt-db-provision (role·grant·target schema); `dbt run`/`build`는 target schema 쓰기 | current |
| `api-mock` | capability | 개발·기능 테스트용 HTTP stub 서버; bounded journal과 tracked mapping 제공 | `wiremock` | No | normal service startup; host 게시만 loopback 전용이며 project default network peer는 인증 없는 admin API에 접근 가능 | current |
| `auth` | domain | 접근 인증과 SSO | `keycloak`, `oauth2-proxy` | No | normal service startup | current |
| `availability` | capability | HTTP 가용성 점검 | `gatus` | No | normal service startup | current |
| `backup` | automation | Restic 백업·SQLite export·R2 offsite copy 작업; host timer와 명시적 명령만 실행 | `restic`, `restic-offsite`, `backup-sqlite-export` | No | backup repository and export staging writes when run; `restic-offsite`는 R2 원격 저장소에 추가만 함 | current |
| `bi` | capability | Superset BI 웹과 feature 소유 metadata DB; Keycloak native OIDC | `mng-pg`, `mng-pg-init`, `superset-db-provision`, `superset-init`, `superset` | No | initialization: superset-db-provision (role·database), superset-init (migration·role 동기화·`lakehouse` DB 등록); Trino는 `lakehouse` profile로 함께 선택 | current |
| `batch-metrics` | capability | 배치 작업 메트릭 수집 | `prometheus`, `grafana`, `pushgateway` | No | normal service startup | current |
| `cassandra` | topology | 독립 LAB 단일 Cassandra 노드; 내부망 무인증 | `cassandra-node1` | No | normal service startup; 실제 기동은 별도 승인 | current |
| `cdc` | capability | Debezium 원천은 dev-pg; 다른 관리 도구 metadata는 mng-pg에 유지 | `dev-pg`, `dev-platform-provision`, `kafka-1`, `schema-registry`, `kafka-connect`, `debezium-db-provision` | No | initialization: debezium-db-provision (복제 role·grant·publication); connector 등록·snapshot은 별도 승인 | current |
| `contract-testing` | capability | Pact Broker 계약 저장·검증 결과와 feature 소유 DB 준비 | `mng-pg`, `mng-pg-init`, `pact-broker-db-provision`, `pact-broker` | No | initialization: pact-broker-db-provision (role·database); pact 게시·검증 결과 쓰기 | current |
| `core` | baseline | 접근·인증·secret 기반과 관리 DB; HOME 앱 전체는 아님 | `traefik`, `keycloak`, `oauth2-proxy`, `openbao`, `openbao-agent`, `mng-valkey`, `mng-pg`, `mng-pg-init` | No | initialization: mng-pg-init | current |
| `couchdb` | topology | 독립 LAB CouchDB 복제 구성과 초기화 | `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init` | No | initialization: couchdb-cluster-init | current |
| `crawl4ai` | capability | 격리 network의 token 보호 웹 crawler; 현재 소비자 없음 | `crawl4ai` | No | normal service startup | current |
| `data-science` | capability | JupyterLab 단일 사용자 notebook과 MLflow 추적 | `mng-pg`, `mng-pg-init`, `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets`, `mlflow-db-provision`, `mlflow`, `jupyterlab` | No | initialization: mlflow-db-provision, seaweedfs-buckets | current |
| `dedicated-valkey` | topology | 앱별 broker 대안; HOST와 SECRET 매핑도 전환해야 함 | `oauth2-proxy-valkey`, `oauth2-proxy-valkey-exporter`, `airflow-valkey`, `airflow-valkey-exporter`, `n8n-valkey`, `n8n-valkey-exporter` | No | normal service startup | current |
| `dependency-update` | automation | Renovate 갱신 제안 작업; 명시적 실행만 허용 | `renovate` | No | remote dependency proposals when configured | current |
| `dev` | baseline | 개발 접근·관측·메일 캡처; HOME 최소 선택과 다름 | `traefik`, `keycloak`, `oauth2-proxy`, `openbao`, `openbao-agent`, `mng-valkey`, `mng-valkey-exporter`, `mng-pg`, `mng-pg-init`, `mng-pg-exporter`, `prometheus`, `grafana`, `grafana-db-provision`, `node-exporter`, `cadvisor`, `gatus`, `mailpit` | No | initialization: mng-pg-init, grafana-db-provision | current |
| `dev-data` | capability | 단일 개발 PG·Valkey와 그 지표 exporter를 명시적으로 선택 | `dev-pg`, `dev-pg-monitor-provision`, `dev-pg-exporter`, `dev-valkey`, `dev-valkey-exporter` | No | 새 개발 저장소 기동; 관리 DB·Valkey와 상태 분리; initialization: dev-pg-monitor-provision | current |
| `experience` | capability | 관리자 전용 공유 Storybook 정적 UI 검토 | `storybook` | No | 정적 origin startup; `unless-stopped` 재시작 정책은 명시적 중지 전 reboot에도 유지 | current |
| `graph` | role | 그래프 데이터 저장 | `neo4j` | No | normal service startup | current |
| `iac` | automation | OpenTofu와 Terrakube IaC 작업; apply는 별도 승인; Terrakube state는 `storage`와 함께 선택 | `opentofu`, `terrakube-api`, `terrakube-ui`, `terrakube-executor` | No | operator IaC execution | current |
| `lab-kafka` | topology | 독립 LAB Kafka 3-broker KRaft 구성·exporter·초기화 | `lab-kafka-1`, `lab-kafka-2`, `lab-kafka-3`, `lab-kafka-exporter`, `lab-kafka-init` | No | initialization: lab-kafka-init | current |
| `lab-locust` | topology | root에서 분리된 Locust master/worker headless 부하 LAB | `lab-locust-master`, `lab-locust-worker` | No | `labs/locust.yml`의 별도 project/network/volume; target 승인 후에만 트래픽 생성 | current |
| `lakehouse` | capability | Iceberg 테이블 batch·유지보수 작업, SQL 조회, streaming 적재, 데이터 품질 검사와 SeaweedFS REST catalog 저장소 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets`, `seaweedfs-table-bucket`, `spark`, `trino`, `flink-jobmanager`, `flink-taskmanager`, `great-expectations` | No | initialization: seaweedfs-buckets, seaweedfs-table-bucket (table bucket·policy·namespace); 기본 `spark` 명령은 namespace 조회만, 쓰기는 명시적 `run` | current |
| `local` | baseline | 로컬 접근·인증·관리 DB와 메일 캡처 | `traefik`, `keycloak`, `oauth2-proxy`, `openbao`, `openbao-agent`, `mng-valkey`, `mng-pg`, `mng-pg-init`, `mailpit` | No | initialization: mng-pg-init | current |
| `logs` | capability | 로그 수집·조회와 object 저장소 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets`, `loki`, `alloy`, `grafana` | No | initialization: seaweedfs-buckets | current |
| `mail-dev` | capability | 개발 SMTP 캡처 | `mailpit` | No | normal service startup | current |
| `mail-server` | capability | 내부 전용 메일 서버; host port·relay 없음, `mail_net` 제출 | `stalwart`, `stalwart-config` | No | initialization: stalwart-config (도메인·listener·relay 금지 plan 적용; listener 변경은 재시작 후) | current |
| `messaging` | domain | Kafka broker·schema·connect·REST·관리 UI | `kafka-1`, `schema-registry`, `kafka-connect`, `kafka-rest-proxy`, `kafbat-ui`, `kafka-exporter`, `kafka-init` | No | initialization: kafka-init | current |
| `messaging-admin` | role | Kafka 관리 UI와 직접 종속 서비스 | `kafka-1`, `schema-registry`, `kafka-connect`, `kafbat-ui` | No | normal service startup | current |
| `messaging-broker` | role | Kafka 단일 broker·초기화·exporter | `kafka-1`, `kafka-exporter`, `kafka-init` | No | initialization: kafka-init | current |
| `messaging-connect` | role | Kafka Connect와 broker·schema 종속성 | `kafka-1`, `schema-registry`, `kafka-connect` | No | normal service startup | current |
| `messaging-rest` | role | Kafka REST 접근 | `kafka-1`, `schema-registry`, `kafka-rest-proxy` | No | normal service startup | current |
| `messaging-schema` | role | Kafka schema registry | `kafka-1`, `schema-registry` | No | normal service startup | current |
| `mlops` | capability | MLflow 추적 서버와 feature 소유 DB·bucket 준비 | `mng-pg`, `mng-pg-init`, `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets`, `mlflow-db-provision`, `mlflow` | No | initialization: mlflow-db-provision, seaweedfs-buckets | current |
| `mng` | role | HOME 관리 DB·공유 broker·exporter | `mng-valkey`, `mng-valkey-exporter`, `mng-pg`, `mng-pg-init`, `mng-pg-exporter` | No | initialization: mng-pg-init | current |
| `mongodb` | topology | 독립 LAB MongoDB replica set과 초기화·관리 UI | `mongo-key-generator`, `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`, `mongo-init`, `mongo-express`, `mongodb-exporter` | No | initialization: mongo-key-generator, mongo-init | current |
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
| `quality-results` | capability | 공용 시험 결과 `perf_db`와 명시적 one-shot provision | `dev-pg`, `dev-perf-provision` | No | initialization: dev-perf-provision; HOME 실행·프로젝트 로그인 발급은 별도 승인 | current |
| `qdrant` | capability | vector 검색 저장소 | `qdrant` | No | normal service startup | current |
| `registry` | role | 개발 컨테이너 registry | `registry` | No | normal service startup | current |
| `sast` | role | 소스 정적 분석 | `sonarqube` | No | normal service startup | current |
| `seaweedfs` | capability | 분산 파일·S3 호환 저장소 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets` | No | initialization: seaweedfs-buckets | current |
| `secrets` | role | OpenBao secret 관리·Agent | `openbao`, `openbao-agent` | No | normal service startup | current |
| `security` | domain | OpenBao 보안 기반 | `openbao`, `openbao-agent` | No | normal service startup | current |
| `storage` | role | HOME 단일 object 저장소와 bucket 초기화 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets` | No | initialization: seaweedfs-buckets | current |
| `storage-seaweedfs` | role | SeaweedFS object/file 저장 역할 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets` | No | initialization: seaweedfs-buckets | current |
| `supabase` | capability | 자체 호스팅 앱 backend 전체 구성 | `studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `imgproxy`, `meta`, `functions`, `analytics`, `db`, `vector`, `supavisor` | No | normal service startup | current |
| `surrealdb` | capability | 독립 multi-model 데이터 저장소 | `surrealdb` | No | normal service startup | current |
| `testing` | automation | k6 이미지 확인용 단발 job; root 기본 명령은 `version` | `k6` | No | 비트래픽 version job; 부하는 승인된 격리 runner에서만 실행 | current |
| `tooling` | domain | 일반 개발 도구 묶음 | `registry`, `sonarqube` | No | normal service startup | current |
| `tracing` | capability | 분산 trace 수집·조회와 object 저장소 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets`, `tempo`, `alloy`, `grafana` | No | initialization: seaweedfs-buckets | current |
| `valkey-cluster` | topology | 독립 LAB Valkey sharding 실험 구성 | `valkey-node-0`, `valkey-node-1`, `valkey-node-2`, `valkey-node-3`, `valkey-node-4`, `valkey-node-5`, `valkey-cluster-init`, `valkey-cluster-exporter` | No | initialization: valkey-cluster-init | current |
| `workflow` | domain | HOME Airflow·n8n·worker·runner | `airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`, `airflow-init`, `flower`, `airflow-statsd-exporter`, `n8n`, `n8n-worker`, `n8n-task-runner`, `n8n-task-runner-worker` | No | initialization: airflow-init | current |
| `workflow-airflow` | capability | Airflow 스케줄링·worker·초기화 | `airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`, `airflow-init`, `flower`, `airflow-statsd-exporter` | No | initialization: airflow-init | current |
| `workflow-n8n` | capability | n8n 자동화와 worker·task runner | `n8n`, `n8n-worker`, `n8n-task-runner`, `n8n-task-runner-worker` | No | normal service startup | current |

### Controls

`Default? = No`는 직접 service target, CLI profile, `COMPOSE_PROFILES` 활성화가
없는 기동에서는 자동 선택되지 않는다는 뜻이다. 직접 지정한 service는 profile을
켜지 않아도 실행될 수 있다. 선택 의미는 [시스템 Guide](../guides/0099-system-operations.md#selection-and-readiness)를 따른다.
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

### HOME activation

| Named selection | Profiles | Forbidden categories |
| --- | --- | --- |
| HOME | `core`, `mng`, `ai`, `workflow`, `obs-core`, `obs-host`, `availability`, `logs`, `alerting`, `storage`, `tracing`, `profiling`, `obs-gpu`, `registry` | `automation`, `lifecycle`, `topology` |

> Historical evidence (not current authority; source: Git history):
> Source: `c26bc8026254dffd7d51fc45b4081a1f80f855f2`, POL-0078 HOME activation.
> 소유자가 2026-09-21 현재 운영 중이라고 밝힌 명령은 `local`, `core`, `mng`, `ai`,
> `dev`, `workflow`, `obs`, `admin` 8개 profile 조합이다. 이는 관측된 운영 선택이며
> 재실행·재시작·새 기능 활성화 승인이 아니다. 이 조합은 `mlops`, `data-science`,
> `analytics-engineering`, `cdc`, `obs-gpu`, `crawl4ai`, `notebook`을 선택하지 않고,
> 2026-09-21 변경 전후 렌더링 서비스 이름 집합이 같다. 새 기능은 필요할 때 이
> 조합에 profile을 명시적으로 추가한다.

새 `dev-data`는 과거 HOME 선택의 `dev`·`local`에 포함되지 않는다. 현재 선택은
위 HOME 행과 소유자가 승인한 exact profile을 따른다. 과거 조합에
대한 추가 지침은 현재 activation 권한이 아니다.

HOME은 위 profile의 이름 있는 선택이며 새 Compose profile이 아니다. 이 선택은 HOME
후보 선택이다. 사용자가 AI와 workflow 상시 필요를 확인했으므로 관리 DB·공유
broker·영속 저장소·관측 종속성을 함께 유지한다. `core`만으로 HOME 앱이 충족되지는
않는다. SPEC-0182 W6(2026-09-25)에서 소유자가 HOME 설정이 이미 전송·수집하는
`tracing`(Tempo), `profiling`(Pyroscope), `obs-gpu`(DCGM exporter)와 기본 사용할
`registry`를 HOME에 추가했다. 그 밖의 새 HOME profile은 추가하지 않는다. OpenBao bootstrap/unseal/Agent 인증,
DB 초기화, 실제 자원 측정 및 backup/restore는 별도 준비 조건이다. config 성공은
무인 재기동이나 live readiness를 증명하지 않는다.

### Companion, exclusion and side effects

| Selection | Constraint |
| --- | --- |
| nginx with core/local/dev | 기본 ingress 80/443 중복을 해소하거나 gateway 하나만 선택 |
| dedicated-valkey with application profiles | HOST·secret 매핑도 전환; profile만 추가하면 broker가 자동 선택되지 않음 |
| lab-kafka | `labs/kafka-cluster.yml`의 별도 project·cluster ID·data directory가 필요하며 물리 HA가 아님 |
| lab-locust | `labs/locust.yml`의 별도 project·network·scenario/result volume을 사용하며 root `testing` profile에 포함되지 않음 |
| opensearch with opensearch-cluster | 서로 다른 Compose project의 대체 토폴로지; LAB은 별도 network·state·credential을 사용 |
| dependency-update | Renovate 전용 작업; tooling/HOME의 암묵적 기동 대상이 아님 |
| testing | root는 k6 버전만 확인; 격리 runner의 부하·샘플 데이터 생성은 대상과 실행량을 별도 승인 |
| iac | OpenTofu/Terrakube 명령·대상·credential·apply 승인 확인 |
| tooling | registry와 SonarQube 일반 개발 도구만 선택; update/IaC/load 작업 제외 |
| supabase with surrealdb/notebook/admin | 현재 SurrealDB host8000 게시 선언은 주석이고 Open Notebook host API는5055이므로 기본 충돌을 단정하지 않는다. SurrealDB host8000을 별도 활성화하면 Supabase Kong과 충돌 여부를 확인한 뒤 binding을 조정한다. |
| mlops / data-science / analytics-engineering / cdc / contract-testing / bi | 도구 metadata는 `mng-pg`·`mng-pg-init`을 사용한다. dbt·CDC 업무 원천은 `dev-pg`·`dev-platform-provision`을 요구한다. 기능 SQL·credential은 각 feature job 소유이며 기본 `mng-pg-init`은 그 secret을 읽지 않는다 |
| cdc with dev-pg | 새 원천의 publication·slot·offset·snapshot은 이전 mng-pg LSN에서 이어지지 않는다. connector 등록과 writer/reader 전환은 별도 승인 후 시행한다 |
| obs-gpu | GPU·driver·Container Toolkit 없는 host에서는 기동 실패; 선택해도 수집 성공을 증명하지 않음 |
| crawl4ai | 다른 repository network에 연결하지 않음; 소비자는 `crawl4ai_net`에 명시적으로 합류 |
| contract-testing | UI·API는 plain HTTP basic auth이므로 host port는 `127.0.0.1`에만 게시하고 route를 추가하지 않음; heartbeat만 공개 |
| lakehouse | `spark`는 one-shot 작업이며 `up`은 namespace 조회만 수행; 테이블 쓰기·`rewrite_data_files`·`expire_snapshots`는 `run --rm spark`로 대상 table을 명시. `trino`는 인증 없는 HTTP API이므로 host port는 `127.0.0.1`에만 게시하고 route를 추가하지 않음. `flink-*`도 같으며 REST JAR 업로드는 끔(`web.submit.enable=false`); Kafka는 별도 profile로 선택. `great-expectations`는 one-shot이며 기본 명령은 suite 목록만 출력 |
| bi | native OIDC 서비스이므로 router는 `gateway-standard-chain@file`만 사용하고 host port 없음; 가입 사용자는 `Gamma`(데이터 접근 없음) |
| api-mock | 인증 없는 admin API가 있으므로 host port는 `127.0.0.1`에만 게시하고 route를 추가하지 않음; 컨테이너 소비자는 project default network에서 `wiremock:8080` 사용 |
| experience | Storybook은 `internal: true`인 `experience_ingress_net`에만 연결; Traefik만 이 망과 `edge_net`을 함께 사용. HOME 기본 선택과 원격 MCP는 포함하지 않음. 브라우저는 기존 `/admins` 인증을 먼저 수행 |
| api-mock load mode | root Compose와 `infra/11-quality/wiremock/wiremock.load.yml`을 같은 model로 결합해 같은 `api-mock` profile의 `wiremock` 설정을 대체; host port와 request journal이 없으며 mock performance만 판정 |

### Verification

```bash
bash scripts/validation/validate-docker-compose.sh
python3 scripts/validation/check-operations-catalog.py
```

첫 명령은 정상 root의 profile 렌더링과 port 중복을 검사한다. 각 LAB은
`docker compose --env-file labs/.env.example -f labs/<topology>.yml --profile <LAB-profile> config --quiet`로 별도 렌더링한다.
실행 전 LAB 전용 변수·secret 참조는 `labs/.env.example`과 `secrets/labs/`의
계약을 확인하며 정상 root의 환경·secret 범위를 재사용하지 않는다. 두 번째는 정상
root에 포함된 infra Compose와 독립 LAB Compose의 profile 이름·서비스 표 일치,
category/purpose, 중복 행, root include 배제, 명시적 서비스 profile, HOME 안전
category와 필수 dependency 폐포를 검사한다.
숫자 Services 열을 추가한다면 실제 선언 수와 일치해야 한다. 은퇴한 snapshot은
검증 입력이 아니다. 첫 명령의 기본 모드는 HOME 조합도 함께 렌더링하여 profile
사이에만 나타나는 host port 충돌을 같은 검사로 확인한다.

검사에 앞서 [RUN-0086](../runbooks/0086-dependency-version-management.md#static-configuration-validation)의
임시 입력 생성·private 읽기 경계를 확인한다. `HYHOME_COMPOSE_PROFILES` override는
기본 every-profile/HOME 검사를 지정 합집합 하나로 바꾸므로 실제 범위를 기록한다.
선택 closure 성공은 optional dependency의 앱 endpoint나 provisioning 완료를
보장하지 않는다. 예를 들어 Grafana DB provisioning 선택과 실제 앱 사용 준비는
[Grafana Guide](../guides/0041-grafana.md)에서 확인한다.

### Review Cadence

- **Owner**: @buenhyden. Infra/DevOps 역할은 책임 설명이다.
- **Cadence**: profile 또는 서비스 선언을 변경할 때.
- **Trigger**: 서비스 추가·은퇴, topology·host port·작업 부수 효과 변경.

## Exceptions

### Exceptions

정상 root profile은 같은 daemon, network, disk, GPU를 공유할 수 있다. 여러
노드는 물리
고가용성을 증명하지 않는다. 알려진 조합 제약을 숨기기 위해 검증을 우회하지
않으며 승인된 예외는 이유·범위·복구·종료 조건을 current Task에 기록한다.

## Related Documents

- [Infrastructure optimization governance](0006-infrastructure-optimization-governance.md)
- [Developer environment](../guides/0002-developer-environment.md)
