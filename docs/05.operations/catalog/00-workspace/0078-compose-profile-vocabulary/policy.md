---
title: "Compose Profile Vocabulary Policy"
version: "1.8.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0078"
parent_ids: []
created: "2026-09-04"
---

# Compose Profile Vocabulary Policy

## Overview

추적된 Compose profile의 이름·분류·목적을 소유한다. `include`는 파일을 병합하고
profile은 서비스를 선택한다. 여러 profile 선택은 합집합이며 보안 격리를 제공하지
않는다. 서비스 수는 구현에서 계산하며 본문에 고정하지 않는다.

## Policy Scope

- **Systems**: root가 include하는 Git-tracked `infra/**/{compose,docker-compose}*.{yml,yaml}`.
- **Agents**: Infra/DevOps/Operations 기여자와 검토자.
- **Environments**: HOME, DEV, OPTIONAL, LAB 및 명시적 migration/maintenance 작업.

## Definitions

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
| `analytics-engineering` | capability | dbt 변환 작업과 feature 소유 DB 권한 준비; 명시적 명령만 쓰기 수행 | `mng-pg`, `mng-pg-init`, `dbt-db-provision`, `dbt` | No | initialization: dbt-db-provision (role·grant·target schema); `dbt run`/`build`는 target schema 쓰기 | current |
| `api-mock` | capability | 개발·테스트용 HTTP stub 서버; tracked mapping만 제공 | `wiremock` | No | normal service startup; admin API는 loopback 전용 | current |
| `auth` | domain | 접근 인증과 SSO | `keycloak`, `oauth2-proxy` | No | normal service startup | current |
| `availability` | capability | HTTP 가용성 점검 | `gatus` | No | normal service startup | current |
| `backup` | automation | Restic 백업·SQLite export 작업; host timer와 명시적 명령만 실행 | `restic`, `backup-sqlite-export` | No | backup repository and export staging writes when run | current |
| `batch-metrics` | capability | 배치 작업 메트릭 수집 | `prometheus`, `grafana`, `pushgateway` | No | normal service startup | current |
| `cassandra` | capability | Cassandra 저장소와 exporter | `cassandra-exporter`, `cassandra-node1` | No | normal service startup | current |
| `cdc` | capability | Debezium PostgreSQL CDC 원천 준비와 Connect worker | `mng-pg`, `mng-pg-init`, `kafka-1`, `schema-registry`, `kafka-connect`, `debezium-db-provision` | No | initialization: debezium-db-provision (복제 role·grant·publication); connector 등록·snapshot은 별도 승인 | current |
| `contract-testing` | capability | Pact Broker 계약 저장·검증 결과와 feature 소유 DB 준비 | `mng-pg`, `mng-pg-init`, `pact-broker-db-provision`, `pact-broker` | No | initialization: pact-broker-db-provision (role·database); pact 게시·검증 결과 쓰기 | current |
| `core` | baseline | 접근·인증·secret 기반과 관리 DB; HOME 앱 전체는 아님 | `traefik`, `keycloak`, `oauth2-proxy`, `openbao`, `openbao-agent`, `mng-valkey`, `mng-pg`, `mng-pg-init` | No | initialization: mng-pg-init | current |
| `couchdb` | topology | CouchDB 복제 구성과 초기화 | `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init` | No | initialization: couchdb-cluster-init | current |
| `crawl4ai` | capability | 격리 network의 token 보호 웹 crawler; 현재 소비자 없음 | `crawl4ai` | No | normal service startup | current |
| `data-science` | capability | JupyterLab 단일 사용자 notebook과 MLflow 추적 | `mng-pg`, `mng-pg-init`, `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets`, `mlflow-db-provision`, `mlflow`, `jupyterlab` | No | initialization: mlflow-db-provision, seaweedfs-buckets | current |
| `dedicated-valkey` | topology | 앱별 broker 대안; HOST와 SECRET 매핑도 전환해야 함 | `oauth2-proxy-valkey`, `oauth2-proxy-valkey-exporter`, `airflow-valkey`, `airflow-valkey-exporter`, `n8n-valkey`, `n8n-valkey-exporter` | No | normal service startup | current |
| `dependency-update` | automation | Renovate 갱신 제안 작업; 명시적 실행만 허용 | `renovate` | No | remote dependency proposals when configured | current |
| `dev` | baseline | 개발 접근·관측·메일 캡처; HOME 최소 선택과 다름 | `traefik`, `keycloak`, `oauth2-proxy`, `openbao`, `openbao-agent`, `mng-valkey`, `mng-valkey-exporter`, `mng-pg`, `mng-pg-init`, `mng-pg-exporter`, `prometheus`, `grafana`, `node-exporter`, `cadvisor`, `gatus`, `mailpit` | No | initialization: mng-pg-init | current |
| `graph` | role | 그래프 데이터 저장 | `neo4j` | No | normal service startup | current |
| `iac` | automation | OpenTofu와 Terrakube IaC 작업; apply는 별도 승인; Terrakube state는 `storage`와 함께 선택 | `opentofu`, `terrakube-api`, `terrakube-ui`, `terrakube-executor` | No | operator IaC execution | current |
| `influxdb` | capability | 시계열 데이터 API | `influxdb` | No | normal service startup | current |
| `ksql` | automation | 명시적 스트림 SQL 실험 도구; datagen 컨테이너는 readiness 확인 후 대기 | `ksqldb-server`, `ksqldb-cli`, `ksql-datagen`, `kafka-1`, `schema-registry` | No | 현재 자동 데이터 생성 없음; 생성 명령 추가 시 synthetic data 부수 효과 검토 | current |
| `lakehouse` | capability | Iceberg 테이블 batch·유지보수 작업, SQL 조회와 SeaweedFS REST catalog 저장소 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets`, `seaweedfs-table-bucket`, `spark`, `trino` | No | initialization: seaweedfs-buckets, seaweedfs-table-bucket (table bucket·policy·namespace); 기본 `spark` 명령은 namespace 조회만, 쓰기는 명시적 `run` | current |
| `local` | baseline | 로컬 접근·인증·관리 DB와 메일 캡처 | `traefik`, `keycloak`, `oauth2-proxy`, `openbao`, `openbao-agent`, `mng-valkey`, `mng-pg`, `mng-pg-init`, `mailpit` | No | initialization: mng-pg-init | current |
| `logs` | capability | 로그 수집·조회와 object 저장소 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets`, `loki`, `alloy`, `grafana` | No | initialization: seaweedfs-buckets | current |
| `mail-dev` | capability | 개발 SMTP 캡처 | `mailpit` | No | normal service startup | current |
| `mail-server` | capability | 실제 메일 송수신; 별도 DNS·운영 준비 필요 | `stalwart` | No | normal service startup | current |
| `messaging` | domain | Kafka broker·schema·connect·REST·관리 UI | `kafka-1`, `schema-registry`, `kafka-connect`, `kafka-rest-proxy`, `kafbat-ui`, `kafka-exporter`, `kafka-init` | No | initialization: kafka-init | current |
| `messaging-admin` | role | Kafka 관리 UI와 직접 종속 서비스 | `kafka-1`, `schema-registry`, `kafka-connect`, `kafbat-ui` | No | normal service startup | current |
| `messaging-broker` | role | Kafka 단일 broker·초기화·exporter | `kafka-1`, `kafka-exporter`, `kafka-init` | No | initialization: kafka-init | current |
| `messaging-cluster` | topology | Kafka 다중 broker; 단일 호스트 장애 격리 아님 | `kafka-1`, `kafka-exporter`, `kafka-init`, `kafka-2`, `kafka-3` | No | initialization: kafka-init | current |
| `messaging-connect` | role | Kafka Connect와 broker·schema 종속성 | `kafka-1`, `schema-registry`, `kafka-connect` | No | normal service startup | current |
| `messaging-rest` | role | Kafka REST 접근 | `kafka-1`, `schema-registry`, `kafka-rest-proxy` | No | normal service startup | current |
| `messaging-schema` | role | Kafka schema registry | `kafka-1`, `schema-registry` | No | normal service startup | current |
| `mlops` | capability | MLflow 추적 서버와 feature 소유 DB·bucket 준비 | `mng-pg`, `mng-pg-init`, `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets`, `mlflow-db-provision`, `mlflow` | No | initialization: mlflow-db-provision, seaweedfs-buckets | current |
| `mng` | role | HOME 관리 DB·공유 broker·exporter | `mng-valkey`, `mng-valkey-exporter`, `mng-pg`, `mng-pg-init`, `mng-pg-exporter` | No | initialization: mng-pg-init | current |
| `mongodb` | topology | MongoDB replica set과 초기화·관리 UI | `mongo-key-generator`, `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`, `mongo-init`, `mongo-express`, `mongodb-exporter` | No | initialization: mongo-key-generator, mongo-init | current |
| `nginx` | topology | Traefik 대체 gateway; 기본 ingress port 중복 금지 | `nginx`, `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets` | No | initialization: seaweedfs-buckets | current |
| `notebook` | capability | Open Notebook과 SurrealDB 저장소 | `surrealdb`, `open_notebook` | No | normal service startup | current |
| `obs` | domain | 전체 관측 기능; HOME에 필요한 하위 선택만 권장 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets`, `prometheus`, `loki`, `tempo`, `alloy`, `grafana`, `node-exporter`, `cadvisor`, `gatus`, `pyroscope`, `alertmanager`, `pushgateway` | No | initialization: seaweedfs-buckets | current |
| `obs-core` | capability | 메트릭 수집·대시보드 | `prometheus`, `grafana` | No | normal service startup | current |
| `obs-gpu` | capability | NVIDIA GPU 메트릭 exporter; GPU·driver·Container Toolkit 필요 | `dcgm-exporter` | No | normal service startup; 모든 GPU 예약 | current |
| `obs-host` | capability | 호스트·컨테이너 자원 측정 | `node-exporter`, `cadvisor` | No | normal service startup | current |
| `ollama` | capability | 로컬 모델 추론과 exporter | `ollama`, `ollama-exporter` | No | normal service startup | current |
| `opensearch` | topology | 단일 OpenSearch와 dashboards | `opensearch`, `opensearch-dashboards` | No | normal service startup | current |
| `opensearch-cluster` | topology | OpenSearch 다중 노드 대안 | `opensearch-dashboards`, `opensearch-node1`, `opensearch-node2`, `opensearch-node3` | No | normal service startup | current |
| `postgres-ha` | topology | Patroni·etcd PostgreSQL 실험 구성 | `etcd-1`, `etcd-2`, `etcd-3`, `pg-router`, `pg-cluster-init`, `pg-0`, `pg-1`, `pg-2`, `pg-0-exporter`, `pg-1-exporter`, `pg-2-exporter` | No | initialization: pg-cluster-init | current |
| `policy-check` | capability | Conftest Rego 정책 테스트; `infra/` read-only, network 없음 | `conftest` | No | 읽기 전용 검사; 쓰기 없음 | current |
| `profiling` | capability | 연속 프로파일 수집·조회 | `alloy`, `grafana`, `pyroscope` | No | normal service startup | current |
| `qdrant` | capability | vector 검색 저장소 | `qdrant` | No | normal service startup | current |
| `registry` | role | 개발 컨테이너 registry | `registry` | No | normal service startup | current |
| `sast` | role | 소스 정적 분석 | `sonarqube` | No | normal service startup | current |
| `seaweedfs` | capability | 분산 파일·S3 호환 저장소 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets` | No | initialization: seaweedfs-buckets | current |
| `secrets` | role | OpenBao secret 관리·Agent | `openbao`, `openbao-agent` | No | normal service startup | current |
| `security` | domain | OpenBao 보안 기반 | `openbao`, `openbao-agent` | No | normal service startup | current |
| `starrocks` | capability | 분석용 warehouse | `starrocks-fe`, `starrocks-be` | No | normal service startup | current |
| `storage` | role | HOME 단일 object 저장소와 bucket 초기화 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets` | No | initialization: seaweedfs-buckets | current |
| `storage-seaweedfs` | role | SeaweedFS object/file 저장 역할 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets` | No | initialization: seaweedfs-buckets | current |
| `supabase` | capability | 자체 호스팅 앱 backend 전체 구성 | `studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `imgproxy`, `meta`, `functions`, `analytics`, `db`, `vector`, `supavisor` | No | normal service startup | current |
| `surrealdb` | capability | 독립 multi-model 데이터 저장소 | `surrealdb` | No | normal service startup | current |
| `testing` | automation | 명시적 부하 생성; 대상·제한 확인 후 실행 | `k6`, `locust-master`, `locust-worker` | No | load or synthetic data generation | current |
| `tooling` | domain | 일반 개발 도구 묶음 | `registry`, `sonarqube` | No | normal service startup | current |
| `tracing` | capability | 분산 trace 수집·조회와 object 저장소 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets`, `tempo`, `alloy`, `grafana` | No | initialization: seaweedfs-buckets | current |
| `valkey-cluster` | topology | Valkey sharding 실험 구성 | `valkey-node-0`, `valkey-node-1`, `valkey-node-2`, `valkey-node-3`, `valkey-node-4`, `valkey-node-5`, `valkey-cluster-init`, `valkey-cluster-exporter` | No | initialization: valkey-cluster-init | current |
| `workflow` | domain | HOME Airflow·n8n·worker·runner | `airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`, `airflow-init`, `flower`, `airflow-statsd-exporter`, `n8n`, `n8n-worker`, `n8n-task-runner`, `n8n-task-runner-worker` | No | initialization: airflow-init | current |
| `workflow-airflow` | capability | Airflow 스케줄링·worker·초기화 | `airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`, `airflow-init`, `flower`, `airflow-statsd-exporter` | No | initialization: airflow-init | current |
| `workflow-n8n` | capability | n8n 자동화와 worker·task runner | `n8n`, `n8n-worker`, `n8n-task-runner`, `n8n-task-runner-worker` | No | normal service startup | current |

## Controls

`Default? = No`는 profile을 명시하지 않으면 자동 선택되지 않는다는 뜻이다.
일반 서비스 기동도 데이터 쓰기를 유발할 수 있다. 추가 부수 효과 열은 초기화·작업·
host mount를 별도로 표시하며 실행 승인을 대신하지 않는다.
`Lifecycle = current`는 추적된 현행 selector라는 뜻이며 HOME 기본 기동·필수성·운영 준비 완료를 뜻하지 않는다. `MIGRATE`는 승인된 전환 작업에만 사용한다.

- **Required**: 모든 서비스는 명시적 profile을 가져야 한다. 새 이름은 같은 변경에서
  표에 추가하고 마지막 소비자가 은퇴하면 표에서 제거한다. 이름 중복·누락·유령 행을
  허용하지 않는다. 필수 `depends_on` 폐포가 선택 안에서 닫혀야 한다.
- **Allowed**: 한 서비스가 여러 profile에 속할 수 있다. 선택형 대안 종속성은
  `required: false`를 쓸 수 있지만 앱의 실제 endpoint 설정과 일치해야 한다.
- **Disallowed**: 검증되지 않은 broad profile을 HOME 기동 명령으로 사용하거나,
  부수 효과가 있는 update/IaC/load-test 작업을 상시 기동하는 것.

### HOME activation

| Named selection | Profiles | Forbidden categories |
| --- | --- | --- |
| HOME | `core`, `mng`, `ai`, `workflow`, `obs-core`, `obs-host`, `availability`, `logs`, `alerting`, `storage` | `automation`, `lifecycle`, `topology` |

소유자가 2026-09-21 현재 운영 중이라고 밝힌 명령은 `local`, `core`, `mng`, `ai`,
`dev`, `workflow`, `obs`, `admin` 8개 profile 조합이다. 이는 관측된 운영 선택이며
재실행·재시작·새 기능 활성화 승인이 아니다. 이 조합은 `mlops`, `data-science`,
`analytics-engineering`, `cdc`, `obs-gpu`, `crawl4ai`, `notebook`을 선택하지 않고,
2026-09-21 변경 전후 렌더링 서비스 이름 집합이 같다. 새 기능은 필요할 때 이
조합에 profile을 명시적으로 추가한다.

HOME은 위 profile의 이름 있는 선택이며 새 Compose profile이 아니다. 이 선택은 HOME
후보 선택이다. 사용자가 AI와 workflow 상시 필요를 확인했으므로 관리 DB·공유
broker·영속 저장소·관측 종속성을 함께 유지한다. `core`만으로 HOME 앱이 충족되지는
않는다. 새 HOME profile은 추가하지 않는다. OpenBao bootstrap/unseal/Agent 인증,
DB 초기화, 실제 자원 측정 및 backup/restore는 별도 준비 조건이다. config 성공은
무인 재기동이나 live readiness를 증명하지 않는다.

### Companion, exclusion and side effects

| Selection | Constraint |
| --- | --- |
| nginx with core/local/dev | 기본 ingress 80/443 중복을 해소하거나 gateway 하나만 선택 |
| dedicated-valkey with application profiles | HOST·secret 매핑도 전환; profile만 추가하면 broker가 자동 선택되지 않음 |
| messaging-cluster | 현재 선언이 kafka-1도 포함; quorum·지속성 검증은 별도이며 물리 HA가 아님 |
| opensearch with opensearch-cluster | 대체 토폴로지; 기본 port 충돌을 피하고 dashboards endpoint를 일치시킴 |
| dependency-update | Renovate 전용 작업; tooling/HOME의 암묵적 기동 대상이 아님 |
| testing | 부하·샘플 데이터 생성 대상과 실행량을 명시 |
| ksql | 현재 datagen 명령은 readiness 확인 후 대기하며 자동 생성하지 않음; 생성 명령 추가 시 대상·실행량을 명시 |
| iac | OpenTofu/Terrakube 명령·대상·credential·apply 승인 확인 |
| tooling | registry와 SonarQube 일반 개발 도구만 선택; update/IaC/load 작업 제외 |
| supabase with surrealdb/notebook/admin | 기본 host 8000 중복 가능; 함께 선택하기 전에 host binding 조정 |
| mlops / data-science / analytics-engineering / cdc / contract-testing | 단독 선택도 `mng-pg`·`mng-pg-init`(및 필요 시 SeaweedFS·Kafka)를 폐포로 함께 선택한다. 기능 SQL·credential은 각 feature job 소유이며 기본 `mng-pg-init`은 그 secret을 읽지 않는다 |
| cdc with running mng-pg | 선언된 `wal_level=logical` 명령은 승인된 `mng-pg` 재생성 후에만 적용되며 관리 DB 소비자 전체가 재시작된다 |
| obs-gpu | GPU·driver·Container Toolkit 없는 host에서는 기동 실패; 선택해도 수집 성공을 증명하지 않음 |
| crawl4ai | 다른 repository network에 연결하지 않음; 소비자는 `crawl4ai_net`에 명시적으로 합류 |
| contract-testing | UI·API는 plain HTTP basic auth이므로 host port는 `127.0.0.1`에만 게시하고 route를 추가하지 않음; heartbeat만 공개 |
| lakehouse | `spark`는 one-shot 작업이며 `up`은 namespace 조회만 수행; 테이블 쓰기·`rewrite_data_files`·`expire_snapshots`는 `run --rm spark`로 대상 table을 명시. `trino`는 인증 없는 HTTP API이므로 host port는 `127.0.0.1`에만 게시하고 route를 추가하지 않음 |
| api-mock | 인증 없는 admin API가 있으므로 host port는 `127.0.0.1`에만 게시하고 route를 추가하지 않음; 컨테이너 소비자는 project default network에서 `wiremock:8080` 사용 |

## Exceptions

profile은 같은 daemon, network, disk, GPU를 공유할 수 있다. 여러 노드는 물리
고가용성을 증명하지 않는다. 알려진 조합 제약을 숨기기 위해 검증을 우회하지
않으며 승인된 예외는 이유·범위·복구·종료 조건을 current Task에 기록한다.

## Verification

```bash
bash scripts/validation/validate-docker-compose.sh
python3 scripts/validation/check-operations-catalog.py
```

첫 명령은 실제 profile 렌더링과 port 중복을 검사한다. 두 번째는 추적된 Compose
이름과 표의 정확한 집합 일치, category/purpose, 중복 행, root include 도달성 및
명시적 서비스 profile, HOME 안전 category와 필수 dependency 폐포를 검사한다.
숫자 Services 열을 추가한다면 실제 선언 수와 일치해야 한다. 은퇴한 snapshot은
검증 입력이 아니다. 첫 명령의 기본 모드는 HOME 조합도 함께 렌더링하여 profile
사이에만 나타나는 host port 충돌을 같은 검사로 확인한다.

## Review Cadence

- **Owner**: Infra/DevOps Engineer.
- **Cadence**: profile 또는 서비스 선언을 변경할 때.
- **Trigger**: 서비스 추가·은퇴, topology·host port·작업 부수 효과 변경.

## Traceability

- [Workspace catalog](../README.md)
- [Convergence specification](../../../../03.specs/0180-home-dev-convergence/spec.md)
- [Runtime version projection](../../../../../infra/tech-stack.versions.json)
- [Original enablement decision](../../../../98.archive/completed/03.specs/0156-compose-enablement-model-convergence/spec.md)
- [Sibling resolution](../../../../98.archive/completed/03.specs/0171-compose-sibling-pair-resolution/spec.md)

## Related Documents

- [Infrastructure optimization governance](../0006-infrastructure-optimization-governance/policy.md)
- [Developer environment](../0002-developer-environment/guide.md)
