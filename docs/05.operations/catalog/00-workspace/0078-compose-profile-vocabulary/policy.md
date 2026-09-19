---
title: "Compose Profile Vocabulary Policy"
version: "1.3.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
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

- **Systems**: root가 include하는 추적된 `infra/**/docker-compose*.yml` 및 `.yaml`.
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
| `admin` | domain | 데이터·로그·노트북 관리 UI | `surrealdb`, `dozzle`, `open_notebook`, `redisinsight` | No | normal service startup | current |
| `admin-data` | role | Valkey 데이터 탐색 UI | `redisinsight` | No | normal service startup | current |
| `admin-logs` | role | 컨테이너 로그 UI | `dozzle` | No | normal service startup | current |
| `ai` | domain | HOME 언어·이미지 AI와 vector 저장소 | `qdrant`, `ollama`, `ollama-exporter`, `open-webui`, `comfyui` | No | normal service startup | current |
| `ai-image` | capability | GPU 이미지 생성 | `comfyui` | No | normal service startup | current |
| `ai-llm` | capability | 언어 모델 추론·채팅·검색 저장소 | `qdrant`, `ollama`, `ollama-exporter`, `open-webui` | No | normal service startup | current |
| `alerting` | capability | 메트릭 경보 전달 | `prometheus`, `grafana`, `alertmanager` | No | normal service startup | current |
| `auth` | domain | 접근 인증과 SSO | `keycloak`, `oauth2-proxy` | No | normal service startup | current |
| `availability` | capability | HTTP 가용성 점검 | `gatus` | No | normal service startup | current |
| `batch-metrics` | capability | 배치 작업 메트릭 수집 | `prometheus`, `grafana`, `pushgateway` | No | normal service startup | current |
| `cassandra` | capability | Cassandra 저장소와 exporter | `cassandra-exporter`, `cassandra-node1` | No | normal service startup | current |
| `core` | baseline | 접근·인증·secret 기반과 관리 DB; HOME 앱 전체는 아님 | `traefik`, `keycloak`, `oauth2-proxy`, `openbao`, `openbao-agent`, `mng-valkey`, `mng-pg`, `mng-pg-init` | No | initialization: mng-pg-init | current |
| `couchdb` | topology | CouchDB 복제 구성과 초기화 | `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init` | No | initialization: couchdb-cluster-init | current |
| `dedicated-valkey` | topology | 앱별 broker 대안; HOST와 SECRET 매핑도 전환해야 함 | `oauth2-proxy-valkey`, `oauth2-proxy-valkey-exporter`, `airflow-valkey`, `airflow-valkey-exporter`, `n8n-valkey`, `n8n-valkey-exporter` | No | normal service startup | current |
| `dependency-update` | automation | Renovate 갱신 제안 작업; 명시적 실행만 허용 | `renovate` | No | remote dependency proposals when configured | current |
| `dev` | baseline | 개발 접근·관측·메일 캡처; HOME 최소 선택과 다름 | `traefik`, `keycloak`, `oauth2-proxy`, `openbao`, `openbao-agent`, `mng-valkey`, `mng-valkey-exporter`, `mng-pg`, `mng-pg-init`, `mng-pg-exporter`, `prometheus`, `grafana`, `node-exporter`, `cadvisor`, `gatus`, `mailpit` | No | initialization: mng-pg-init | current |
| `graph` | role | 그래프 데이터 저장 | `neo4j` | No | normal service startup | current |
| `iac` | automation | OpenTofu와 Terrakube IaC 작업; apply는 별도 승인 | `opentofu`, `terrakube-api`, `terrakube-ui`, `terrakube-executor` | No | operator IaC execution | current |
| `influxdb` | capability | 시계열 데이터 API | `influxdb` | No | normal service startup | current |
| `ksql` | capability | Kafka 기반 스트림 SQL과 데이터 생성 작업 | `ksqldb-server`, `ksqldb-cli`, `ksql-datagen`, `kafka-1`, `schema-registry` | No | load or synthetic data generation | current |
| `legacy-vault` | lifecycle | 기존 Vault 마이그레이션 전용; HOME 제외 | `vault`, `vault-agent` | No | normal service startup | MIGRATE |
| `local` | baseline | 로컬 접근·인증·관리 DB와 메일 캡처 | `traefik`, `keycloak`, `oauth2-proxy`, `openbao`, `openbao-agent`, `mng-valkey`, `mng-pg`, `mng-pg-init`, `mailpit` | No | initialization: mng-pg-init | current |
| `logs` | capability | 로그 수집·조회와 object 저장소 | `minio`, `minio-create-buckets`, `loki`, `alloy`, `grafana` | No | initialization: minio-create-buckets | current |
| `mail-dev` | capability | 개발 SMTP 캡처 | `mailpit` | No | normal service startup | current |
| `mail-server` | capability | 실제 메일 송수신; 별도 DNS·운영 준비 필요 | `stalwart` | No | normal service startup | current |
| `messaging` | domain | Kafka broker·schema·connect·REST·관리 UI | `kafka-1`, `schema-registry`, `kafka-connect`, `kafka-rest-proxy`, `kafbat-ui`, `kafka-exporter`, `kafka-init` | No | initialization: kafka-init | current |
| `messaging-admin` | role | Kafka 관리 UI와 직접 종속 서비스 | `kafka-1`, `schema-registry`, `kafka-connect`, `kafbat-ui` | No | normal service startup | current |
| `messaging-broker` | role | Kafka 단일 broker·초기화·exporter | `kafka-1`, `kafka-exporter`, `kafka-init` | No | initialization: kafka-init | current |
| `messaging-cluster` | topology | Kafka 다중 broker; 단일 호스트 장애 격리 아님 | `kafka-1`, `kafka-exporter`, `kafka-init`, `kafka-2`, `kafka-3` | No | initialization: kafka-init | current |
| `messaging-connect` | role | Kafka Connect와 broker·schema 종속성 | `kafka-1`, `schema-registry`, `kafka-connect` | No | normal service startup | current |
| `messaging-rest` | role | Kafka REST 접근 | `kafka-1`, `schema-registry`, `kafka-rest-proxy` | No | normal service startup | current |
| `messaging-schema` | role | Kafka schema registry | `kafka-1`, `schema-registry` | No | normal service startup | current |
| `mng` | role | HOME 관리 DB·공유 broker·exporter | `mng-valkey`, `mng-valkey-exporter`, `mng-pg`, `mng-pg-init`, `mng-pg-exporter` | No | initialization: mng-pg-init | current |
| `mongodb` | topology | MongoDB replica set과 초기화·관리 UI | `mongo-key-generator`, `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`, `mongo-init`, `mongo-express`, `mongodb-exporter` | No | initialization: mongo-key-generator, mongo-init | current |
| `nginx` | topology | Traefik 대체 gateway; 기본 ingress port 중복 금지 | `nginx`, `minio` | No | normal service startup | current |
| `notebook` | capability | Open Notebook과 SurrealDB 저장소 | `surrealdb`, `open_notebook` | No | normal service startup | current |
| `obs` | domain | 전체 관측 기능; HOME에 필요한 하위 선택만 권장 | `minio`, `minio-create-buckets`, `prometheus`, `loki`, `tempo`, `alloy`, `grafana`, `node-exporter`, `cadvisor`, `gatus`, `pyroscope`, `alertmanager`, `pushgateway` | No | initialization: minio-create-buckets | current |
| `obs-core` | capability | 메트릭 수집·대시보드 | `prometheus`, `grafana` | No | normal service startup | current |
| `obs-host` | capability | 호스트·컨테이너 자원 측정 | `node-exporter`, `cadvisor` | No | normal service startup | current |
| `ollama` | capability | 로컬 모델 추론과 exporter | `ollama`, `ollama-exporter` | No | normal service startup | current |
| `opensearch` | topology | 단일 OpenSearch와 dashboards | `opensearch`, `opensearch-dashboards` | No | normal service startup | current |
| `opensearch-cluster` | topology | OpenSearch 다중 노드 대안 | `opensearch-dashboards`, `opensearch-node1`, `opensearch-node2`, `opensearch-node3` | No | normal service startup | current |
| `postgres-ha` | topology | Patroni·etcd PostgreSQL 실험 구성 | `etcd-1`, `etcd-2`, `etcd-3`, `pg-router`, `pg-cluster-init`, `pg-0`, `pg-1`, `pg-2`, `pg-0-exporter`, `pg-1-exporter`, `pg-2-exporter` | No | initialization: pg-cluster-init | current |
| `profiling` | capability | 연속 프로파일 수집·조회 | `alloy`, `grafana`, `pyroscope` | No | normal service startup | current |
| `qdrant` | capability | vector 검색 저장소 | `qdrant` | No | normal service startup | current |
| `registry` | role | 개발 컨테이너 registry | `registry` | No | normal service startup | current |
| `sast` | role | 소스 정적 분석 | `sonarqube` | No | normal service startup | current |
| `seaweedfs` | capability | 분산 파일·S3 호환 저장소 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3` | No | normal service startup | current |
| `seaweedfs-mount` | capability | FUSE host mount와 필수 서버; host 부작용 있음 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-mount` | No | host FUSE mount | current |
| `secrets` | role | OpenBao secret 관리·Agent | `openbao`, `openbao-agent` | No | normal service startup | current |
| `security` | domain | OpenBao 보안 기반 | `openbao`, `openbao-agent` | No | normal service startup | current |
| `starrocks` | capability | 분석용 warehouse | `starrocks-fe`, `starrocks-be` | No | normal service startup | current |
| `storage` | role | HOME 단일 object 저장소와 bucket 초기화 | `minio`, `minio-create-buckets` | No | initialization: minio-create-buckets | current |
| `storage-cluster` | topology | 다중 MinIO 대안; endpoint·data 전환 필요 | `minio1`, `minio2`, `minio3`, `minio4` | No | normal service startup | current |
| `storage-seaweedfs` | role | SeaweedFS object/file 저장 역할 | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3` | No | normal service startup | current |
| `supabase` | capability | 자체 호스팅 앱 backend 전체 구성 | `studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `imgproxy`, `meta`, `functions`, `analytics`, `db`, `vector`, `supavisor` | No | normal service startup | current |
| `surrealdb` | capability | 독립 multi-model 데이터 저장소 | `surrealdb` | No | normal service startup | current |
| `testing` | automation | 명시적 부하 생성; 대상·제한 확인 후 실행 | `k6`, `locust-master` | No | load or synthetic data generation | current |
| `tooling` | domain | 개발 도구 묶음; IaC 작업 부작용 검토 필요 | `locust-master`, `locust-worker`, `registry`, `sonarqube`, `opentofu`, `terrakube-api`, `terrakube-ui`, `terrakube-executor` | No | operator IaC execution; load or synthetic data generation | current |
| `tracing` | capability | 분산 trace 수집·조회와 object 저장소 | `minio`, `minio-create-buckets`, `tempo`, `alloy`, `grafana` | No | initialization: minio-create-buckets | current |
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

`core mng ai workflow obs-core obs-host availability logs alerting storage`는 HOME
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
| storage-cluster with storage/logs | 서로 다른 object store; endpoint·data migration 없이 교체 불가 |
| seaweedfs-mount | master·volume·filer 폐포 포함; FUSE host mount 권한과 해제 계획 확인 |
| legacy-vault with HOME | 정상 HOME에서 제외; 보존된 상태의 migration 승인 후에만 사용 |
| dependency-update | Renovate 전용 작업; tooling/HOME의 암묵적 기동 대상이 아님 |
| testing or ksql | 부하·샘플 데이터 생성 가능; 대상과 실행량을 명시 |
| iac or tooling | OpenTofu/Terrakube가 포함됨; 명령·대상·credential·apply 승인 확인 |
| supabase with surrealdb/notebook/admin | 기본 host 8000 중복 가능; 함께 선택하기 전에 host binding 조정 |

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
명시적 서비스 profile을 검사한다. 숫자 Services 열을 추가한다면 실제 선언 수와
일치해야 한다. 은퇴한 snapshot은 검증 입력이 아니다. 함께 선택할 조합도 별도로
렌더링하고 필수 종속성·부수 효과·runtime readiness를 확인한다.

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
