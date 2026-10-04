---
title: "운영 가이드"
version: "0.2.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
layer: "operations"
---

# 운영 가이드

> 정상 운영 맥락, 전제, 공통 점검을 소유하는 Guide 인덱스

## Overview

Guide는 서비스와 작업 공간을 이해하고 정상 상태를 확인하는 데 필요한 맥락을 소유한다. 실행 절차가 필요하면 같은 slug의 Runbook으로 넘긴다. 아래 표는 도메인별로 등록된 모든 Guide를 한 번씩 나열하며 각 행의 관련 문서 열에서 같은 subject의 Policy와 Runbook을 찾을 수 있다.

## Audience

- 운영자
- 개발자
- SREs
- 보안 담당자
- AI 에이전트

## Scope

- 이 디렉터리의 모든 Guide를 도메인별로 한 번씩 나열한다.
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

| Guide | ID | 관련 문서 |
| --- | --- | --- |
| [시스템 운영](0099-system-operations.md) | `GDE-0099` | [Runbook](../runbooks/0099-system-operations.md); 공통 Policy는 Guide에서 연결 |
| [Dependency version management](0086-dependency-version-management.md) | `GDE-0086` | [Policy](../policies/0086-dependency-version-management.md), [Runbook](../runbooks/0086-dependency-version-management.md) |
| [Backup and restore](0021-backup-and-restore.md) | `GDE-0021` | [Policy](../policies/0021-backup-and-restore.md), [Runbook](../runbooks/0021-backup-and-restore.md) |
| [Optimization hardening](0074-laboratory-optimization-hardening.md) | `GDE-0074` | [Policy](../policies/0074-laboratory-optimization-hardening.md), [Runbook](../runbooks/0074-laboratory-optimization-hardening.md) |

### Cross-cutting workspace

| Guide | ID | 관련 문서 |
| --- | --- | --- |
| [developer environment](0002-developer-environment.md) | `GDE-0002` | — |
| [environment-key comparison](0003-env-key-comparison.md) | `GDE-0003` | — |
| [harness engineering](0004-harness-agent-first-engineering.md) | `GDE-0004` | [Policy](../policies/0004-harness-agent-first-engineering.md), [Runbook](../runbooks/0004-harness-agent-first-engineering.md) |
| [new-service onboarding](0008-new-service-onboarding.md) | `GDE-0008` | — |
| [sensitive environment comparison](0010-sensitive-env-vars-comparison.md) | `GDE-0010` | — |

### 01 Gateway

| Guide | ID | 관련 문서 |
| --- | --- | --- |
| [Nginx](0011-nginx.md) | `GDE-0011` | [Policy](../policies/0011-nginx.md), [Runbook](../runbooks/0011-nginx.md) |
| [edge routing stack](0012-edge-routing-stack.md) | `GDE-0012` | — |
| [Traefik](0013-traefik.md) | `GDE-0013` | [Policy](../policies/0013-traefik.md), [Runbook](../runbooks/0013-traefik.md) |

### 02 Auth

| Guide | ID | 관련 문서 |
| --- | --- | --- |
| [Keycloak](0014-keycloak.md) | `GDE-0014` | [Policy](../policies/0014-keycloak.md), [Runbook](../runbooks/0014-keycloak.md) |
| [OAuth2 Proxy](0015-oauth2-proxy.md) | `GDE-0015` | [Policy](../policies/0015-oauth2-proxy.md), [Runbook](../runbooks/0015-oauth2-proxy.md) |
| [Application authentication integration](0079-application-auth-integration.md) | `GDE-0079` | [Policy](../policies/0079-application-auth-integration.md) |

### 03 Security

| Guide | ID | 관련 문서 |
| --- | --- | --- |
| [OpenBao](0085-openbao.md) | `GDE-0085` | [Policy](../policies/0085-openbao.md), [Runbook](../runbooks/0085-openbao.md) |

### 04 Data

| Guide | ID | 관련 문서 |
| --- | --- | --- |
| [Analytics — InfluxDB](0017-influxdb.md) | `GDE-0017` | [Policy](../policies/0017-influxdb.md), [Runbook](../runbooks/0017-influxdb.md) |
| [Analytics — OpenSearch](0019-opensearch.md) | `GDE-0019` | [Policy](../policies/0019-opensearch.md), [Runbook](../runbooks/0019-opensearch.md) |
| [Cache and KV — Valkey Cluster](0022-valkey-cluster.md) | `GDE-0022` | [Policy](../policies/0022-valkey-cluster.md), [Runbook](../runbooks/0022-valkey-cluster.md) |
| [Lake and Object — SeaweedFS](0024-seaweedfs.md) | `GDE-0024` | [Policy](../policies/0024-seaweedfs.md), [Runbook](../runbooks/0024-seaweedfs.md) |
| [NoSQL — Cassandra](0025-cassandra.md) | `GDE-0025` | [Policy](../policies/0025-cassandra.md), [Runbook](../runbooks/0025-cassandra.md) |
| [NoSQL — CouchDB](0026-couchdb.md) | `GDE-0026` | [Policy](../policies/0026-couchdb.md), [Runbook](../runbooks/0026-couchdb.md) |
| [NoSQL — MongoDB](0027-mongodb.md) | `GDE-0027` | [Policy](../policies/0027-mongodb.md), [Runbook](../runbooks/0027-mongodb.md) |
| [Operational — MNG-DB](0028-management-database.md) | `GDE-0028` | [Policy](../policies/0028-management-database.md), [Runbook](../runbooks/0028-management-database.md) |
| [Operational — Development database](0100-development-database.md) | `GDE-0100` | [Policy](../policies/0100-development-database.md), [Runbook](../runbooks/0100-development-database.md) |
| [Operational — Supabase](0029-supabase.md) | `GDE-0029` | [Policy](../policies/0029-supabase.md), [Runbook](../runbooks/0029-supabase.md) |
| [Optimization hardening](0030-data-optimization-hardening.md) | `GDE-0030` | [Policy](../policies/0030-data-optimization-hardening.md), [Runbook](../runbooks/0030-data-optimization-hardening.md) |
| [Relational — PostgreSQL Cluster](0031-postgresql-cluster.md) | `GDE-0031` | [Policy](../policies/0031-postgresql-cluster.md), [Runbook](../runbooks/0031-postgresql-cluster.md) |
| [Specialized — Neo4j](0033-neo4j.md) | `GDE-0033` | [Policy](../policies/0033-neo4j.md), [Runbook](../runbooks/0033-neo4j.md) |
| [Specialized — Qdrant](0034-qdrant.md) | `GDE-0034` | [Policy](../policies/0034-qdrant.md), [Runbook](../runbooks/0034-qdrant.md) |
| [RedisInsight](0076-redisinsight.md) | `GDE-0076` | [Policy](../policies/0076-redisinsight.md), [Runbook](../runbooks/0076-redisinsight.md) |

### 05 Messaging

| Guide | ID | 관련 문서 |
| --- | --- | --- |
| [Kafka](0036-kafka.md) | `GDE-0036` | [Policy](../policies/0036-kafka.md), [Runbook](../runbooks/0036-kafka.md) |
| [Messaging hardening](0037-messaging-optimization-hardening.md) | `GDE-0037` | [Policy](../policies/0037-messaging-optimization-hardening.md), [Runbook](../runbooks/0037-messaging-optimization-hardening.md) |

### 06 Observability

| Guide | ID | 관련 문서 |
| --- | --- | --- |
| [Alertmanager](0039-alertmanager.md) | `GDE-0039` | [Policy](../policies/0039-alertmanager.md), [Runbook](../runbooks/0039-alertmanager.md) |
| [Alloy](0040-alloy.md) | `GDE-0040` | [Policy](../policies/0040-alloy.md), [Runbook](../runbooks/0040-alloy.md) |
| [Grafana](0041-grafana.md) | `GDE-0041` | [Policy](../policies/0041-grafana.md), [Runbook](../runbooks/0041-grafana.md) |
| [LGTM stack](0042-lgtm-stack.md) | `GDE-0042` | — |
| [Loki](0043-loki.md) | `GDE-0043` | [Policy](../policies/0043-loki.md), [Runbook](../runbooks/0043-loki.md) |
| [Optimization hardening](0044-observability-optimization-hardening.md) | `GDE-0044` | [Policy](../policies/0044-observability-optimization-hardening.md), [Runbook](../runbooks/0044-observability-optimization-hardening.md) |
| [Prometheus](0045-prometheus.md) | `GDE-0045` | [Policy](../policies/0045-prometheus.md), [Runbook](../runbooks/0045-prometheus.md) |
| [Pushgateway](0046-pushgateway.md) | `GDE-0046` | [Policy](../policies/0046-pushgateway.md), [Runbook](../runbooks/0046-pushgateway.md) |
| [Pyroscope](0047-pyroscope.md) | `GDE-0047` | [Policy](../policies/0047-pyroscope.md), [Runbook](../runbooks/0047-pyroscope.md) |
| [Tempo](0049-tempo.md) | `GDE-0049` | [Policy](../policies/0049-tempo.md), [Runbook](../runbooks/0049-tempo.md) |
| [Gatus](0087-gatus.md) | `GDE-0087` | [Policy](../policies/0087-gatus.md), [Runbook](../runbooks/0087-gatus.md) |
| [Dozzle](0072-dozzle.md) | `GDE-0072` | [Policy](../policies/0072-dozzle.md), [Runbook](../runbooks/0072-dozzle.md) |

### 07 Workflow

| Guide | ID | 관련 문서 |
| --- | --- | --- |
| [Airflow](0050-airflow.md) | `GDE-0050` | [Policy](../policies/0050-airflow.md), [Runbook](../runbooks/0050-airflow.md) |
| [DAG deployment](0051-airflow-dag-lifecycle.md) | `GDE-0051` | [Policy](../policies/0052-airflow-dag-lifecycle.md) |
| [n8n](0053-n8n.md) | `GDE-0053` | [Policy](../policies/0053-n8n.md), [Runbook](../runbooks/0053-n8n.md) |
| [Optimization hardening](0054-workflow-optimization-hardening.md) | `GDE-0054` | [Policy](../policies/0054-workflow-optimization-hardening.md), [Runbook](../runbooks/0054-workflow-optimization-hardening.md) |

### 08 AI

| Guide | ID | 관련 문서 |
| --- | --- | --- |
| [Ollama](0056-ollama.md) | `GDE-0056` | [Policy](../policies/0056-ollama.md), [Runbook](../runbooks/0056-ollama.md) |
| [Open WebUI](0057-open-webui.md) | `GDE-0057` | [Policy](../policies/0057-open-webui.md), [Runbook](../runbooks/0057-open-webui.md) |
| [Optimization hardening](0058-ai-optimization-hardening.md) | `GDE-0058` | [Policy](../policies/0058-ai-optimization-hardening.md), [Runbook](../runbooks/0058-ai-optimization-hardening.md) |
| [RAG workflow](0059-rag-workflow.md) | `GDE-0059` | — |
| [ComfyUI](0081-comfyui.md) | `GDE-0081` | [Policy](../policies/0081-comfyui.md), [Runbook](../runbooks/0081-comfyui.md) |
| [Crawl4AI](0091-crawl4ai.md) | `GDE-0091` | [Policy](../policies/0091-crawl4ai.md), [Runbook](../runbooks/0091-crawl4ai.md) |
| [Open Notebook](0073-open-notebook.md) | `GDE-0073` | [Policy](../policies/0073-open-notebook.md), [Runbook](../runbooks/0073-open-notebook.md) |
| [SurrealDB](0080-surrealdb.md) | `GDE-0080` | [Policy](../policies/0080-surrealdb.md), [Runbook](../runbooks/0080-surrealdb.md) |
| [MLflow](0088-mlflow.md) | `GDE-0088` | [Policy](../policies/0088-mlflow.md), [Runbook](../runbooks/0088-mlflow.md) |

### 09 Platform Operations

| Guide | ID | 관련 문서 |
| --- | --- | --- |
| [Optimization hardening](0063-tooling-optimization-hardening.md) | `GDE-0063` | [Policy](../policies/0063-tooling-optimization-hardening.md), [Runbook](../runbooks/0063-tooling-optimization-hardening.md) |
| [Registry](0065-registry.md) | `GDE-0065` | [Policy](../policies/0065-registry.md), [Runbook](../runbooks/0065-registry.md) |
| [Terraform](0068-terraform.md) | `GDE-0068` | [Policy](../policies/0068-terraform.md), [Runbook](../runbooks/0068-terraform.md) |
| [Terrakube](0069-terrakube.md) | `GDE-0069` | [Policy](../policies/0069-terrakube.md), [Runbook](../runbooks/0069-terrakube.md) |
| [OpenTofu](0082-opentofu.md) | `GDE-0082` | [Policy](../policies/0082-opentofu.md), [Runbook](../runbooks/0082-opentofu.md) |
| [Renovate](0083-renovate.md) | `GDE-0083` | [Policy](../policies/0083-renovate.md), [Runbook](../runbooks/0083-renovate.md) |

### 10 Communication

| Guide | ID | 관련 문서 |
| --- | --- | --- |
| [Stalwart mail](0070-mail.md) | `GDE-0070` | [Policy](../policies/0070-mail.md), [Runbook](../runbooks/0070-mail.md) |

### 11 Quality

| Guide | ID | 관련 문서 |
| --- | --- | --- |
| [k6](0061-k6.md) | `GDE-0061` | [Policy](../policies/0061-k6.md), [Runbook](../runbooks/0061-k6.md) |
| [Locust](0062-locust.md) | `GDE-0062` | [Policy](../policies/0062-locust.md), [Runbook](../runbooks/0062-locust.md) |
| [Performance testing](0064-performance-testing.md) | `GDE-0064` | [Policy](../policies/0064-performance-testing.md), [Runbook](../runbooks/0064-performance-testing.md) |
| [SonarQube](0066-sonarqube.md) | `GDE-0066` | [Policy](../policies/0066-sonarqube.md), [Runbook](../runbooks/0066-sonarqube.md) |
| [WireMock](0092-wiremock.md) | `GDE-0092` | [Policy](../policies/0092-wiremock.md), [Runbook](../runbooks/0092-wiremock.md) |
| [Pact Broker](0093-pact-broker.md) | `GDE-0093` | [Policy](../policies/0093-pact-broker.md), [Runbook](../runbooks/0093-pact-broker.md) |
| [Conftest](0095-conftest.md) | `GDE-0095` | [Policy](../policies/0095-conftest.md), [Runbook](../runbooks/0095-conftest.md) |
| [Mailpit](0084-mailpit.md) | `GDE-0084` | [Policy](../policies/0084-mailpit.md), [Runbook](../runbooks/0084-mailpit.md) |

### 12 Analytics

| Guide | ID | 관련 문서 |
| --- | --- | --- |
| [Lakehouse — Iceberg engines](0094-lakehouse.md) | `GDE-0094` | [Policy](../policies/0094-lakehouse.md), [Runbook](../runbooks/0094-lakehouse.md) |
| [Analytics — Superset](0097-superset.md) | `GDE-0097` | [Policy](../policies/0097-superset.md), [Runbook](../runbooks/0097-superset.md) |
| [dbt](0090-dbt.md) | `GDE-0090` | [Policy](../policies/0090-dbt.md), [Runbook](../runbooks/0090-dbt.md) |
| [JupyterLab](0089-jupyterlab.md) | `GDE-0089` | [Policy](../policies/0089-jupyterlab.md), [Runbook](../runbooks/0089-jupyterlab.md) |

### 13 Experience

| Guide | ID | 관련 문서 |
| --- | --- | --- |
| [Shared Storybook](0101-storybook.md) | `GDE-0101` | [Policy](../policies/0101-storybook.md), [Runbook](../runbooks/0101-storybook.md) |

### Cross-cutting connectivity

| Guide | ID | 관련 문서 |
| --- | --- | --- |
| [Compose network membership](0077-ip-address-management.md) | `GDE-0077` | [Policy](../policies/0077-ip-address-management.md), [Runbook](../runbooks/0077-ip-address-management.md) |
| [hy-home.k8s integration](0096-k8s-integration.md) | `GDE-0096` | [Policy](../policies/0096-k8s-integration.md), [Runbook](../runbooks/0096-k8s-integration.md) |

## Usage

1. 새 Guide는 [Guide template](../../99.templates/templates/operations/guide.template.md)으로 시작한다.
2. 새 subject 번호는 subject마다 하나를 발급하고 그 subject의 역할 문서가 같은 번호와 slug를 쓴다.
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
