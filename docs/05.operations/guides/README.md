---
title: "Operations Guides"
version: "0.1.0"
type: "common/readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-26"
layer: "operations"
---

# Operations Guides

> 정상 운영 맥락, 전제, 공통 점검을 소유하는 Guide 인덱스

## Overview

Guide는 서비스와 작업 공간을 이해하고 정상 상태를 확인하는 데 필요한 맥락을 소유한다. 실행 절차가 필요하면 같은 slug의 Runbook으로 넘긴다.

## Audience

- Operators
- Developers
- SREs
- Security Officers
- AI Agents

## Scope

- 이 디렉터리의 모든 Guide를 도메인별로 한 번씩 나열한다.
- 파일 이름은 `####-<slug>.md`이고 `####`는 문서 자신의 artifact 번호다.
- 같은 slug는 다른 역할 디렉터리에서 같은 subject를 가리킨다.

## Structure

도메인은 경로가 아니라 이 인덱스의 분류다. `관련 문서` 열은 같은 subject의
다른 역할 문서를 가리킨다.

### 00 Workspace

| Guide | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [developer environment](0002-developer-environment.md) | `GDE-0002` | active | — |
| [environment-key comparison](0003-env-key-comparison.md) | `GDE-0003` | active | — |
| [harness engineering](0004-harness-agent-first-engineering.md) | `GDE-0004` | active | [Policy](../policies/0004-harness-agent-first-engineering.md), [Runbook](../runbooks/0004-harness-agent-first-engineering.md) |
| [new-service onboarding](0008-new-service-onboarding.md) | `GDE-0008` | active | — |
| [sensitive environment comparison](0010-sensitive-env-vars-comparison.md) | `GDE-0010` | active | — |
| [Dependency version management](0086-dependency-version-management.md) | `GDE-0086` | draft | [Policy](../policies/0086-dependency-version-management.md), [Runbook](../runbooks/0086-dependency-version-management.md) |

### 01 Gateway

| Guide | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Nginx](0011-nginx.md) | `GDE-0011` | active | [Policy](../policies/0011-nginx.md), [Runbook](../runbooks/0011-nginx.md) |
| [edge routing stack](0012-edge-routing-stack.md) | `GDE-0012` | active | — |
| [Traefik](0013-traefik.md) | `GDE-0013` | active | [Policy](../policies/0013-traefik.md), [Runbook](../runbooks/0013-traefik.md) |

### 02 Auth

| Guide | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Keycloak](0014-keycloak.md) | `GDE-0014` | active | [Policy](../policies/0014-keycloak.md), [Runbook](../runbooks/0014-keycloak.md) |
| [OAuth2 Proxy](0015-oauth2-proxy.md) | `GDE-0015` | active | [Policy](../policies/0015-oauth2-proxy.md), [Runbook](../runbooks/0015-oauth2-proxy.md) |
| [Application authentication integration](0079-application-auth-integration.md) | `GDE-0079` | draft | [Policy](../policies/0079-application-auth-integration.md) |

### 03 Security

| Guide | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [OpenBao](0085-openbao.md) | `GDE-0085` | draft | [Policy](../policies/0085-openbao.md), [Runbook](../runbooks/0085-openbao.md) |

### 04 Data

| Guide | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Analytics — InfluxDB](0017-influxdb.md) | `GDE-0017` | active | [Policy](../policies/0017-influxdb.md), [Runbook](../runbooks/0017-influxdb.md) |
| [Analytics — OpenSearch](0019-opensearch.md) | `GDE-0019` | active | [Policy](../policies/0019-opensearch.md), [Runbook](../runbooks/0019-opensearch.md) |
| [Backup and restore](0021-backup-and-restore.md) | `GDE-0021` | draft | [Policy](../policies/0021-backup-and-restore.md), [Runbook](../runbooks/0021-backup-and-restore.md) |
| [Cache and KV — Valkey Cluster](0022-valkey-cluster.md) | `GDE-0022` | active | [Policy](../policies/0022-valkey-cluster.md), [Runbook](../runbooks/0022-valkey-cluster.md) |
| [Lake and Object — SeaweedFS](0024-seaweedfs.md) | `GDE-0024` | active | [Policy](../policies/0024-seaweedfs.md), [Runbook](../runbooks/0024-seaweedfs.md) |
| [NoSQL — Cassandra](0025-cassandra.md) | `GDE-0025` | active | [Policy](../policies/0025-cassandra.md), [Runbook](../runbooks/0025-cassandra.md) |
| [NoSQL — CouchDB](0026-couchdb.md) | `GDE-0026` | active | [Policy](../policies/0026-couchdb.md), [Runbook](../runbooks/0026-couchdb.md) |
| [NoSQL — MongoDB](0027-mongodb.md) | `GDE-0027` | active | [Policy](../policies/0027-mongodb.md), [Runbook](../runbooks/0027-mongodb.md) |
| [Operational — MNG-DB](0028-management-database.md) | `GDE-0028` | active | [Policy](../policies/0028-management-database.md), [Runbook](../runbooks/0028-management-database.md) |
| [Operational — Supabase](0029-supabase.md) | `GDE-0029` | active | [Policy](../policies/0029-supabase.md), [Runbook](../runbooks/0029-supabase.md) |
| [Optimization hardening](0030-data-optimization-hardening.md) | `GDE-0030` | active | [Policy](../policies/0030-data-optimization-hardening.md), [Runbook](../runbooks/0030-data-optimization-hardening.md) |
| [Relational — PostgreSQL Cluster](0031-postgresql-cluster.md) | `GDE-0031` | active | [Policy](../policies/0031-postgresql-cluster.md), [Runbook](../runbooks/0031-postgresql-cluster.md) |
| [Specialized — Neo4j](0033-neo4j.md) | `GDE-0033` | active | [Policy](../policies/0033-neo4j.md), [Runbook](../runbooks/0033-neo4j.md) |
| [Specialized — Qdrant](0034-qdrant.md) | `GDE-0034` | active | [Policy](../policies/0034-qdrant.md), [Runbook](../runbooks/0034-qdrant.md) |
| [Lakehouse — Iceberg engines](0094-lakehouse.md) | `GDE-0094` | draft | [Policy](../policies/0094-lakehouse.md), [Runbook](../runbooks/0094-lakehouse.md) |
| [Analytics — Superset](0097-superset.md) | `GDE-0097` | draft | [Policy](../policies/0097-superset.md), [Runbook](../runbooks/0097-superset.md) |

### 05 Messaging

| Guide | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Kafka](0036-kafka.md) | `GDE-0036` | active | [Policy](../policies/0036-kafka.md), [Runbook](../runbooks/0036-kafka.md) |
| [Messaging hardening](0037-messaging-optimization-hardening.md) | `GDE-0037` | active | [Policy](../policies/0037-messaging-optimization-hardening.md), [Runbook](../runbooks/0037-messaging-optimization-hardening.md) |

### 06 Observability

| Guide | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Alertmanager](0039-alertmanager.md) | `GDE-0039` | active | [Policy](../policies/0039-alertmanager.md), [Runbook](../runbooks/0039-alertmanager.md) |
| [Alloy](0040-alloy.md) | `GDE-0040` | active | [Policy](../policies/0040-alloy.md), [Runbook](../runbooks/0040-alloy.md) |
| [Grafana](0041-grafana.md) | `GDE-0041` | active | [Policy](../policies/0041-grafana.md), [Runbook](../runbooks/0041-grafana.md) |
| [LGTM stack](0042-lgtm-stack.md) | `GDE-0042` | active | — |
| [Loki](0043-loki.md) | `GDE-0043` | active | [Policy](../policies/0043-loki.md), [Runbook](../runbooks/0043-loki.md) |
| [Optimization hardening](0044-observability-optimization-hardening.md) | `GDE-0044` | active | [Policy](../policies/0044-observability-optimization-hardening.md), [Runbook](../runbooks/0044-observability-optimization-hardening.md) |
| [Prometheus](0045-prometheus.md) | `GDE-0045` | active | [Policy](../policies/0045-prometheus.md), [Runbook](../runbooks/0045-prometheus.md) |
| [Pushgateway](0046-pushgateway.md) | `GDE-0046` | active | [Policy](../policies/0046-pushgateway.md), [Runbook](../runbooks/0046-pushgateway.md) |
| [Pyroscope](0047-pyroscope.md) | `GDE-0047` | active | [Policy](../policies/0047-pyroscope.md), [Runbook](../runbooks/0047-pyroscope.md) |
| [Tempo](0049-tempo.md) | `GDE-0049` | active | [Policy](../policies/0049-tempo.md), [Runbook](../runbooks/0049-tempo.md) |
| [Gatus](0087-gatus.md) | `GDE-0087` | draft | [Policy](../policies/0087-gatus.md), [Runbook](../runbooks/0087-gatus.md) |

### 07 Workflow

| Guide | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Airflow](0050-airflow.md) | `GDE-0050` | active | [Policy](../policies/0050-airflow.md), [Runbook](../runbooks/0050-airflow.md) |
| [DAG deployment](0051-airflow-dag-lifecycle.md) | `GDE-0051` | active | [Policy](../policies/0052-airflow-dag-lifecycle.md) |
| [n8n](0053-n8n.md) | `GDE-0053` | active | [Policy](../policies/0053-n8n.md), [Runbook](../runbooks/0053-n8n.md) |
| [Optimization hardening](0054-workflow-optimization-hardening.md) | `GDE-0054` | active | [Policy](../policies/0054-workflow-optimization-hardening.md), [Runbook](../runbooks/0054-workflow-optimization-hardening.md) |

### 08 AI

| Guide | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Ollama](0056-ollama.md) | `GDE-0056` | active | [Policy](../policies/0056-ollama.md), [Runbook](../runbooks/0056-ollama.md) |
| [Open WebUI](0057-open-webui.md) | `GDE-0057` | active | [Policy](../policies/0057-open-webui.md), [Runbook](../runbooks/0057-open-webui.md) |
| [Optimization hardening](0058-ai-optimization-hardening.md) | `GDE-0058` | active | [Policy](../policies/0058-ai-optimization-hardening.md), [Runbook](../runbooks/0058-ai-optimization-hardening.md) |
| [RAG workflow](0059-rag-workflow.md) | `GDE-0059` | active | — |
| [ComfyUI](0081-comfyui.md) | `GDE-0081` | draft | [Policy](../policies/0081-comfyui.md), [Runbook](../runbooks/0081-comfyui.md) |
| [Crawl4AI](0091-crawl4ai.md) | `GDE-0091` | active | [Policy](../policies/0091-crawl4ai.md), [Runbook](../runbooks/0091-crawl4ai.md) |

### 09 Tooling

| Guide | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [k6](0061-k6.md) | `GDE-0061` | active | [Policy](../policies/0061-k6.md), [Runbook](../runbooks/0061-k6.md) |
| [Locust](0062-locust.md) | `GDE-0062` | active | [Policy](../policies/0062-locust.md), [Runbook](../runbooks/0062-locust.md) |
| [Optimization hardening](0063-tooling-optimization-hardening.md) | `GDE-0063` | active | [Policy](../policies/0063-tooling-optimization-hardening.md), [Runbook](../runbooks/0063-tooling-optimization-hardening.md) |
| [Performance testing](0064-performance-testing.md) | `GDE-0064` | active | [Policy](../policies/0064-performance-testing.md), [Runbook](../runbooks/0064-performance-testing.md) |
| [Registry](0065-registry.md) | `GDE-0065` | active | [Policy](../policies/0065-registry.md), [Runbook](../runbooks/0065-registry.md) |
| [SonarQube](0066-sonarqube.md) | `GDE-0066` | active | [Policy](../policies/0066-sonarqube.md), [Runbook](../runbooks/0066-sonarqube.md) |
| [Terraform](0068-terraform.md) | `GDE-0068` | active | [Policy](../policies/0068-terraform.md), [Runbook](../runbooks/0068-terraform.md) |
| [Terrakube](0069-terrakube.md) | `GDE-0069` | active | [Policy](../policies/0069-terrakube.md), [Runbook](../runbooks/0069-terrakube.md) |
| [OpenTofu](0082-opentofu.md) | `GDE-0082` | draft | [Policy](../policies/0082-opentofu.md), [Runbook](../runbooks/0082-opentofu.md) |
| [Renovate](0083-renovate.md) | `GDE-0083` | draft | [Policy](../policies/0083-renovate.md), [Runbook](../runbooks/0083-renovate.md) |
| [dbt](0090-dbt.md) | `GDE-0090` | active | [Policy](../policies/0090-dbt.md), [Runbook](../runbooks/0090-dbt.md) |
| [WireMock](0092-wiremock.md) | `GDE-0092` | active | [Policy](../policies/0092-wiremock.md), [Runbook](../runbooks/0092-wiremock.md) |
| [Pact Broker](0093-pact-broker.md) | `GDE-0093` | active | [Policy](../policies/0093-pact-broker.md), [Runbook](../runbooks/0093-pact-broker.md) |
| [Conftest](0095-conftest.md) | `GDE-0095` | draft | [Policy](../policies/0095-conftest.md), [Runbook](../runbooks/0095-conftest.md) |

### 10 Communication

| Guide | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Stalwart mail](0070-mail.md) | `GDE-0070` | active | [Policy](../policies/0070-mail.md), [Runbook](../runbooks/0070-mail.md) |
| [Mailpit](0084-mailpit.md) | `GDE-0084` | draft | [Policy](../policies/0084-mailpit.md), [Runbook](../runbooks/0084-mailpit.md) |

### 11 Laboratory

| Guide | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Dozzle](0072-dozzle.md) | `GDE-0072` | active | [Policy](../policies/0072-dozzle.md), [Runbook](../runbooks/0072-dozzle.md) |
| [Open Notebook](0073-open-notebook.md) | `GDE-0073` | active | [Policy](../policies/0073-open-notebook.md), [Runbook](../runbooks/0073-open-notebook.md) |
| [Optimization hardening](0074-laboratory-optimization-hardening.md) | `GDE-0074` | active | [Policy](../policies/0074-laboratory-optimization-hardening.md), [Runbook](../runbooks/0074-laboratory-optimization-hardening.md) |
| [RedisInsight](0076-redisinsight.md) | `GDE-0076` | active | [Policy](../policies/0076-redisinsight.md), [Runbook](../runbooks/0076-redisinsight.md) |
| [SurrealDB](0080-surrealdb.md) | `GDE-0080` | draft | [Policy](../policies/0080-surrealdb.md), [Runbook](../runbooks/0080-surrealdb.md) |
| [MLflow](0088-mlflow.md) | `GDE-0088` | active | [Policy](../policies/0088-mlflow.md), [Runbook](../runbooks/0088-mlflow.md) |
| [JupyterLab](0089-jupyterlab.md) | `GDE-0089` | active | [Policy](../policies/0089-jupyterlab.md), [Runbook](../runbooks/0089-jupyterlab.md) |

### 12 Infra Net

| Guide | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Compose network membership](0077-ip-address-management.md) | `GDE-0077` | active | [Policy](../policies/0077-ip-address-management.md), [Runbook](../runbooks/0077-ip-address-management.md) |
| [hy-home.k8s integration](0096-k8s-integration.md) | `GDE-0096` | draft | [Policy](../policies/0096-k8s-integration.md), [Runbook](../runbooks/0096-k8s-integration.md) |

## How to Work in This Area

1. 새 Guide는 [Guide template](../../99.templates/templates/operations/guide.template.md)으로 시작한다.
2. 새 subject 번호는 subject마다 하나를 발급하고, 그 subject의 역할 문서가 같은 번호와 slug를 쓴다.
3. 문서를 추가, 이동, 삭제하면 이 인덱스에 한 줄로 반영한다. 검증기는 모든 구성원이 정확히 한 번 연결되었는지 확인한다.
4. 해당 역할이 필요 없는 subject에는 빈 문서를 만들지 않는다.

## Related Documents

- [Operations](../README.md)
- [Guides](../guides/README.md)
- [Policies](../policies/README.md)
- [Runbooks](../runbooks/README.md)
- [Incidents](../incidents/README.md)
- [Documentation protocol](../../../.agents/governance/documentation-protocol.md#role-specific-authoring)
