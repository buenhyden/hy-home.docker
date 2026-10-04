---
title: "운영 런북"
version: "0.2.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
layer: "operations"
---

# 운영 런북

> 사용 조건, 명령 순서, 검증, 복구, 에스컬레이션을 소유하는 Runbook 인덱스

## Overview

Runbook은 언제 쓰는지, 어디서 무엇을 입력해 어떤 순서로 실행하는지, 기대 결과, 중단 조건, 검증, 복구, 에스컬레이션을 소유한다.

## Audience

- 운영자
- 개발자
- SREs
- 보안 담당자
- AI 에이전트

## Scope

- 이 디렉터리의 모든 Runbook를 도메인별로 한 번씩 나열한다.
- 파일 이름은 `####-<slug>.md`이고 `####`는 문서 자신의 artifact 번호다.
- 같은 slug는 다른 역할 디렉터리에서 같은 subject를 가리킨다.

## Structure

도메인은 경로가 아니라 이 인덱스의 분류다. `관련 문서` 열은 같은 subject의
다른 역할 문서를 가리킨다.

시스템 전반의 기동·인증·복구·용량·업데이트는 아래 공통 분류에서 시작한다.
티어별 서비스는 01–13 분류에서 찾고, 행의 관련 문서로 같은 subject의 다른 역할을
확인한다. 작업 공간과 공통 연결은 번호 없는 분류이며 별도 인프라 티어가 아니다.
서비스와 공통 문서의 연결은 적용 범위를 설명하며 서비스 소유권을 추가하지 않는다.

### Cross-cutting system and lifecycle

| Runbook | ID | 관련 문서 |
| --- | --- | --- |
| [시스템 교차 서비스 진단](0099-system-operations.md) | `RUN-0099` | [Guide](../guides/0099-system-operations.md) |
| [Dependency version management](0086-dependency-version-management.md) | `RUN-0086` | [Guide](../guides/0086-dependency-version-management.md), [Policy](../policies/0086-dependency-version-management.md) |
| [Cold start and reboot](0098-cold-start-and-reboot.md) | `RUN-0098` | — |
| [Backup and restore](0021-backup-and-restore.md) | `RUN-0021` | [Guide](../guides/0021-backup-and-restore.md), [Policy](../policies/0021-backup-and-restore.md) |
| [Storage exhaustion](0035-storage-exhaustion.md) | `RUN-0035` | — |
| [Optimization hardening](0074-laboratory-optimization-hardening.md) | `RUN-0074` | [Guide](../guides/0074-laboratory-optimization-hardening.md), [Policy](../policies/0074-laboratory-optimization-hardening.md) |

### Cross-cutting workspace

| Runbook | ID | 관련 문서 |
| --- | --- | --- |
| [harness engineering](0004-harness-agent-first-engineering.md) | `RUN-0004` | [Guide](../guides/0004-harness-agent-first-engineering.md), [Policy](../policies/0004-harness-agent-first-engineering.md) |
| [release management](0009-release-management.md) | `RUN-0009` | — |

### 01 Gateway

| Runbook | ID | 관련 문서 |
| --- | --- | --- |
| [Nginx](0011-nginx.md) | `RUN-0011` | [Guide](../guides/0011-nginx.md), [Policy](../policies/0011-nginx.md) |
| [Traefik](0013-traefik.md) | `RUN-0013` | [Guide](../guides/0013-traefik.md), [Policy](../policies/0013-traefik.md) |

### 02 Auth

| Runbook | ID | 관련 문서 |
| --- | --- | --- |
| [Keycloak](0014-keycloak.md) | `RUN-0014` | [Guide](../guides/0014-keycloak.md), [Policy](../policies/0014-keycloak.md) |
| [OAuth2 Proxy](0015-oauth2-proxy.md) | `RUN-0015` | [Guide](../guides/0015-oauth2-proxy.md), [Policy](../policies/0015-oauth2-proxy.md) |

### 03 Security

| Runbook | ID | 관련 문서 |
| --- | --- | --- |
| [OpenBao](0085-openbao.md) | `RUN-0085` | [Guide](../guides/0085-openbao.md), [Policy](../policies/0085-openbao.md) |

### 04 Data

| Runbook | ID | 관련 문서 |
| --- | --- | --- |
| [Analytics — InfluxDB](0017-influxdb.md) | `RUN-0017` | [Guide](../guides/0017-influxdb.md), [Policy](../policies/0017-influxdb.md) |
| [Analytics — OpenSearch](0019-opensearch.md) | `RUN-0019` | [Guide](../guides/0019-opensearch.md), [Policy](../policies/0019-opensearch.md) |
| [Cache and KV — Valkey Cluster](0022-valkey-cluster.md) | `RUN-0022` | [Guide](../guides/0022-valkey-cluster.md), [Policy](../policies/0022-valkey-cluster.md) |
| [Lake and Object — SeaweedFS](0024-seaweedfs.md) | `RUN-0024` | [Guide](../guides/0024-seaweedfs.md), [Policy](../policies/0024-seaweedfs.md) |
| [NoSQL — Cassandra](0025-cassandra.md) | `RUN-0025` | [Guide](../guides/0025-cassandra.md), [Policy](../policies/0025-cassandra.md) |
| [NoSQL — CouchDB](0026-couchdb.md) | `RUN-0026` | [Guide](../guides/0026-couchdb.md), [Policy](../policies/0026-couchdb.md) |
| [NoSQL — MongoDB](0027-mongodb.md) | `RUN-0027` | [Guide](../guides/0027-mongodb.md), [Policy](../policies/0027-mongodb.md) |
| [Operational — MNG-DB](0028-management-database.md) | `RUN-0028` | [Guide](../guides/0028-management-database.md), [Policy](../policies/0028-management-database.md) |
| [Operational — Development database](0100-development-database.md) | `RUN-0100` | [Guide](../guides/0100-development-database.md), [Policy](../policies/0100-development-database.md) |
| [Operational — Supabase](0029-supabase.md) | `RUN-0029` | [Guide](../guides/0029-supabase.md), [Policy](../policies/0029-supabase.md) |
| [Optimization hardening](0030-data-optimization-hardening.md) | `RUN-0030` | [Guide](../guides/0030-data-optimization-hardening.md), [Policy](../policies/0030-data-optimization-hardening.md) |
| [Relational — PostgreSQL Cluster](0031-postgresql-cluster.md) | `RUN-0031` | [Guide](../guides/0031-postgresql-cluster.md), [Policy](../policies/0031-postgresql-cluster.md) |
| [PostgreSQL logical upgrade restore rehearsal](0032-postgresql-logical-upgrade-restore-rehearsal.md) | `RUN-0032` | — |
| [Specialized — Neo4j](0033-neo4j.md) | `RUN-0033` | [Guide](../guides/0033-neo4j.md), [Policy](../policies/0033-neo4j.md) |
| [Specialized — Qdrant](0034-qdrant.md) | `RUN-0034` | [Guide](../guides/0034-qdrant.md), [Policy](../policies/0034-qdrant.md) |
| [RedisInsight](0076-redisinsight.md) | `RUN-0076` | [Guide](../guides/0076-redisinsight.md), [Policy](../policies/0076-redisinsight.md) |

### 05 Messaging

| Runbook | ID | 관련 문서 |
| --- | --- | --- |
| [Kafka](0036-kafka.md) | `RUN-0036` | [Guide](../guides/0036-kafka.md), [Policy](../policies/0036-kafka.md) |
| [Messaging hardening](0037-messaging-optimization-hardening.md) | `RUN-0037` | [Guide](../guides/0037-messaging-optimization-hardening.md), [Policy](../policies/0037-messaging-optimization-hardening.md) |

### 06 Observability

| Runbook | ID | 관련 문서 |
| --- | --- | --- |
| [Alertmanager](0039-alertmanager.md) | `RUN-0039` | [Guide](../guides/0039-alertmanager.md), [Policy](../policies/0039-alertmanager.md) |
| [Alloy](0040-alloy.md) | `RUN-0040` | [Guide](../guides/0040-alloy.md), [Policy](../policies/0040-alloy.md) |
| [Grafana](0041-grafana.md) | `RUN-0041` | [Guide](../guides/0041-grafana.md), [Policy](../policies/0041-grafana.md) |
| [Loki](0043-loki.md) | `RUN-0043` | [Guide](../guides/0043-loki.md), [Policy](../policies/0043-loki.md) |
| [Optimization hardening](0044-observability-optimization-hardening.md) | `RUN-0044` | [Guide](../guides/0044-observability-optimization-hardening.md), [Policy](../policies/0044-observability-optimization-hardening.md) |
| [Prometheus](0045-prometheus.md) | `RUN-0045` | [Guide](../guides/0045-prometheus.md), [Policy](../policies/0045-prometheus.md) |
| [Pushgateway](0046-pushgateway.md) | `RUN-0046` | [Guide](../guides/0046-pushgateway.md), [Policy](../policies/0046-pushgateway.md) |
| [Pyroscope](0047-pyroscope.md) | `RUN-0047` | [Guide](../guides/0047-pyroscope.md), [Policy](../policies/0047-pyroscope.md) |
| [Tempo](0049-tempo.md) | `RUN-0049` | [Guide](../guides/0049-tempo.md), [Policy](../policies/0049-tempo.md) |
| [Gatus](0087-gatus.md) | `RUN-0087` | [Guide](../guides/0087-gatus.md), [Policy](../policies/0087-gatus.md) |
| [Dozzle](0072-dozzle.md) | `RUN-0072` | [Guide](../guides/0072-dozzle.md), [Policy](../policies/0072-dozzle.md) |

### 07 Workflow

| Runbook | ID | 관련 문서 |
| --- | --- | --- |
| [Airflow](0050-airflow.md) | `RUN-0050` | [Guide](../guides/0050-airflow.md), [Policy](../policies/0050-airflow.md) |
| [n8n](0053-n8n.md) | `RUN-0053` | [Guide](../guides/0053-n8n.md), [Policy](../policies/0053-n8n.md) |
| [Optimization hardening](0054-workflow-optimization-hardening.md) | `RUN-0054` | [Guide](../guides/0054-workflow-optimization-hardening.md), [Policy](../policies/0054-workflow-optimization-hardening.md) |

### 08 AI

| Runbook | ID | 관련 문서 |
| --- | --- | --- |
| [GPU recovery](0055-gpu-recovery.md) | `RUN-0055` | — |
| [Ollama](0056-ollama.md) | `RUN-0056` | [Guide](../guides/0056-ollama.md), [Policy](../policies/0056-ollama.md) |
| [Open WebUI](0057-open-webui.md) | `RUN-0057` | [Guide](../guides/0057-open-webui.md), [Policy](../policies/0057-open-webui.md) |
| [Optimization hardening](0058-ai-optimization-hardening.md) | `RUN-0058` | [Guide](../guides/0058-ai-optimization-hardening.md), [Policy](../policies/0058-ai-optimization-hardening.md) |
| [ComfyUI](0081-comfyui.md) | `RUN-0081` | [Guide](../guides/0081-comfyui.md), [Policy](../policies/0081-comfyui.md) |
| [Crawl4AI](0091-crawl4ai.md) | `RUN-0091` | [Guide](../guides/0091-crawl4ai.md), [Policy](../policies/0091-crawl4ai.md) |
| [Open Notebook](0073-open-notebook.md) | `RUN-0073` | [Guide](../guides/0073-open-notebook.md), [Policy](../policies/0073-open-notebook.md) |
| [SurrealDB](0080-surrealdb.md) | `RUN-0080` | [Guide](../guides/0080-surrealdb.md), [Policy](../policies/0080-surrealdb.md) |
| [MLflow](0088-mlflow.md) | `RUN-0088` | [Guide](../guides/0088-mlflow.md), [Policy](../policies/0088-mlflow.md) |

### 09 Platform Operations

| Runbook | ID | 관련 문서 |
| --- | --- | --- |
| [Optimization hardening](0063-tooling-optimization-hardening.md) | `RUN-0063` | [Guide](../guides/0063-tooling-optimization-hardening.md), [Policy](../policies/0063-tooling-optimization-hardening.md) |
| [Registry](0065-registry.md) | `RUN-0065` | [Guide](../guides/0065-registry.md), [Policy](../policies/0065-registry.md) |
| [Terraform](0068-terraform.md) | `RUN-0068` | [Guide](../guides/0068-terraform.md), [Policy](../policies/0068-terraform.md) |
| [Terrakube](0069-terrakube.md) | `RUN-0069` | [Guide](../guides/0069-terrakube.md), [Policy](../policies/0069-terrakube.md) |
| [OpenTofu](0082-opentofu.md) | `RUN-0082` | [Guide](../guides/0082-opentofu.md), [Policy](../policies/0082-opentofu.md) |
| [Renovate](0083-renovate.md) | `RUN-0083` | [Guide](../guides/0083-renovate.md), [Policy](../policies/0083-renovate.md) |

### 10 Communication

| Runbook | ID | 관련 문서 |
| --- | --- | --- |
| [Stalwart mail](0070-mail.md) | `RUN-0070` | [Guide](../guides/0070-mail.md), [Policy](../policies/0070-mail.md) |

### 11 Quality

| Runbook | ID | 관련 문서 |
| --- | --- | --- |
| [k6](0061-k6.md) | `RUN-0061` | [Guide](../guides/0061-k6.md), [Policy](../policies/0061-k6.md) |
| [Locust](0062-locust.md) | `RUN-0062` | [Guide](../guides/0062-locust.md), [Policy](../policies/0062-locust.md) |
| [Performance testing](0064-performance-testing.md) | `RUN-0064` | [Guide](../guides/0064-performance-testing.md), [Policy](../policies/0064-performance-testing.md) |
| [SonarQube](0066-sonarqube.md) | `RUN-0066` | [Guide](../guides/0066-sonarqube.md), [Policy](../policies/0066-sonarqube.md) |
| [WireMock](0092-wiremock.md) | `RUN-0092` | [Guide](../guides/0092-wiremock.md), [Policy](../policies/0092-wiremock.md) |
| [Pact Broker](0093-pact-broker.md) | `RUN-0093` | [Guide](../guides/0093-pact-broker.md), [Policy](../policies/0093-pact-broker.md) |
| [Conftest](0095-conftest.md) | `RUN-0095` | [Guide](../guides/0095-conftest.md), [Policy](../policies/0095-conftest.md) |
| [Mailpit](0084-mailpit.md) | `RUN-0084` | [Guide](../guides/0084-mailpit.md), [Policy](../policies/0084-mailpit.md) |

### 12 Analytics

| Runbook | ID | 관련 문서 |
| --- | --- | --- |
| [Lakehouse — Iceberg engines](0094-lakehouse.md) | `RUN-0094` | [Guide](../guides/0094-lakehouse.md), [Policy](../policies/0094-lakehouse.md) |
| [Analytics — Superset](0097-superset.md) | `RUN-0097` | [Guide](../guides/0097-superset.md), [Policy](../policies/0097-superset.md) |
| [dbt](0090-dbt.md) | `RUN-0090` | [Guide](../guides/0090-dbt.md), [Policy](../policies/0090-dbt.md) |
| [JupyterLab](0089-jupyterlab.md) | `RUN-0089` | [Guide](../guides/0089-jupyterlab.md), [Policy](../policies/0089-jupyterlab.md) |

### 13 Experience

| Runbook | ID | 관련 문서 |
| --- | --- | --- |
| [Shared Storybook](0101-storybook.md) | `RUN-0101` | [Guide](../guides/0101-storybook.md), [Policy](../policies/0101-storybook.md) |

### Cross-cutting connectivity

| Runbook | ID | 관련 문서 |
| --- | --- | --- |
| [Compose network membership](0077-ip-address-management.md) | `RUN-0077` | [Guide](../guides/0077-ip-address-management.md), [Policy](../policies/0077-ip-address-management.md) |
| [hy-home.k8s integration](0096-k8s-integration.md) | `RUN-0096` | [Guide](../guides/0096-k8s-integration.md), [Policy](../policies/0096-k8s-integration.md) |

## Usage

1. 새 Runbook는 [Runbook template](../../99.templates/templates/operations/runbook.template.md)으로 시작한다.
2. 새 subject 번호는 subject마다 하나를 발급하고, 그 subject의 역할 문서가 같은 번호와 slug를 쓴다.
3. 문서를 추가, 이동, 삭제하면 이 인덱스에 한 줄로 반영한다. 검증기는 모든 구성원이 정확히 한 번 연결되었는지 확인한다.
4. Compose 서비스가 연결된 subject는 Guide/Policy/Runbook 세 역할을 모두 유지한다.
   서비스 연결이 없는 공통·작업 공간 subject는 필요한 역할만 두고 빈 문서를 만들지 않는다.
   공통 통제·절차는 소유 문서로 연결하고 서비스별 적용 조건과 차이를 각 역할에 남긴다.

## Related Documents

- [Operations](../README.md)
- [Guides](../guides/README.md)
- [Policies](../policies/README.md)
- [Runbooks](../runbooks/README.md)
- [Incidents](../incidents/README.md)
- [Documentation protocol](../../../.agents/governance/documentation-protocol.md#role-specific-authoring)
