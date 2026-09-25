---
title: "Operations Policies"
version: "0.1.0"
type: "common/readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-26"
layer: "operations"
---

# Operations Policies

> 허용·금지, 승인, 보안, 예외, 검토 주기를 소유하는 Policy 인덱스

## Overview

Policy는 무엇이 허용되고 금지되는지, 누가 승인하는지, 예외와 검토 주기를 소유한다. 명령 순서는 소유하지 않고 같은 slug의 Runbook에 둔다. 에이전트 실행 규칙은 `.agents/`가 소유한다.

## Audience

- Operators
- Developers
- SREs
- Security Officers
- AI Agents

## Scope

- 이 디렉터리의 모든 Policy를 도메인별로 한 번씩 나열한다.
- 파일 이름은 `####-<slug>.md`이고 `####`는 문서 자신의 artifact 번호다.
- 같은 slug는 다른 역할 디렉터리에서 같은 subject를 가리킨다.

## Structure

도메인은 경로가 아니라 이 인덱스의 분류다. `관련 문서` 열은 같은 subject의
다른 역할 문서를 가리킨다.

### 00 Workspace

| Policy | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [common optimization exceptions](0001-common-optimizations-template-exceptions.md) | `POL-0001` | active | — |
| [harness engineering](0004-harness-agent-first-engineering.md) | `POL-0004` | active | [Guide](../guides/0004-harness-agent-first-engineering.md), [Runbook](../runbooks/0004-harness-agent-first-engineering.md) |
| [infrastructure optimization governance](0006-infrastructure-optimization-governance.md) | `POL-0006` | active | — |
| [Compose profile vocabulary](0078-compose-profile-vocabulary.md) | `POL-0078` | active | — |
| [Dependency version management](0086-dependency-version-management.md) | `POL-0086` | draft | [Guide](../guides/0086-dependency-version-management.md), [Runbook](../runbooks/0086-dependency-version-management.md) |

### 01 Gateway

| Policy | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Nginx](0011-nginx.md) | `POL-0011` | active | [Guide](../guides/0011-nginx.md), [Runbook](../runbooks/0011-nginx.md) |
| [Traefik](0013-traefik.md) | `POL-0013` | active | [Guide](../guides/0013-traefik.md), [Runbook](../runbooks/0013-traefik.md) |

### 02 Auth

| Policy | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Keycloak](0014-keycloak.md) | `POL-0014` | active | [Guide](../guides/0014-keycloak.md), [Runbook](../runbooks/0014-keycloak.md) |
| [OAuth2 Proxy](0015-oauth2-proxy.md) | `POL-0015` | active | [Guide](../guides/0015-oauth2-proxy.md), [Runbook](../runbooks/0015-oauth2-proxy.md) |
| [Application authentication integration](0079-application-auth-integration.md) | `POL-0079` | draft | [Guide](../guides/0079-application-auth-integration.md) |

### 03 Security

| Policy | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [OpenBao](0085-openbao.md) | `POL-0085` | draft | [Guide](../guides/0085-openbao.md), [Runbook](../runbooks/0085-openbao.md) |

### 04 Data

| Policy | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Analytics — InfluxDB](0017-influxdb.md) | `POL-0017` | active | [Guide](../guides/0017-influxdb.md), [Runbook](../runbooks/0017-influxdb.md) |
| [Analytics — OpenSearch](0019-opensearch.md) | `POL-0019` | active | [Guide](../guides/0019-opensearch.md), [Runbook](../runbooks/0019-opensearch.md) |
| [Backup and restore](0021-backup-and-restore.md) | `POL-0021` | active | [Guide](../guides/0021-backup-and-restore.md), [Runbook](../runbooks/0021-backup-and-restore.md) |
| [Cache and KV — Valkey Cluster](0022-valkey-cluster.md) | `POL-0022` | active | [Guide](../guides/0022-valkey-cluster.md), [Runbook](../runbooks/0022-valkey-cluster.md) |
| [Lake and Object — SeaweedFS](0024-seaweedfs.md) | `POL-0024` | active | [Guide](../guides/0024-seaweedfs.md), [Runbook](../runbooks/0024-seaweedfs.md) |
| [NoSQL — Cassandra](0025-cassandra.md) | `POL-0025` | active | [Guide](../guides/0025-cassandra.md), [Runbook](../runbooks/0025-cassandra.md) |
| [NoSQL — CouchDB](0026-couchdb.md) | `POL-0026` | active | [Guide](../guides/0026-couchdb.md), [Runbook](../runbooks/0026-couchdb.md) |
| [NoSQL — MongoDB](0027-mongodb.md) | `POL-0027` | active | [Guide](../guides/0027-mongodb.md), [Runbook](../runbooks/0027-mongodb.md) |
| [Operational — MNG-DB](0028-management-database.md) | `POL-0028` | active | [Guide](../guides/0028-management-database.md), [Runbook](../runbooks/0028-management-database.md) |
| [Operational — Supabase](0029-supabase.md) | `POL-0029` | active | [Guide](../guides/0029-supabase.md), [Runbook](../runbooks/0029-supabase.md) |
| [Optimization hardening](0030-data-optimization-hardening.md) | `POL-0030` | active | [Guide](../guides/0030-data-optimization-hardening.md), [Runbook](../runbooks/0030-data-optimization-hardening.md) |
| [Relational — PostgreSQL Cluster](0031-postgresql-cluster.md) | `POL-0031` | active | [Guide](../guides/0031-postgresql-cluster.md), [Runbook](../runbooks/0031-postgresql-cluster.md) |
| [Specialized — Neo4j](0033-neo4j.md) | `POL-0033` | active | [Guide](../guides/0033-neo4j.md), [Runbook](../runbooks/0033-neo4j.md) |
| [Specialized — Qdrant](0034-qdrant.md) | `POL-0034` | active | [Guide](../guides/0034-qdrant.md), [Runbook](../runbooks/0034-qdrant.md) |
| [Lakehouse — Iceberg engines](0094-lakehouse.md) | `POL-0094` | draft | [Guide](../guides/0094-lakehouse.md), [Runbook](../runbooks/0094-lakehouse.md) |
| [Analytics — Superset](0097-superset.md) | `POL-0097` | draft | [Guide](../guides/0097-superset.md), [Runbook](../runbooks/0097-superset.md) |

### 05 Messaging

| Policy | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Kafka](0036-kafka.md) | `POL-0036` | active | [Guide](../guides/0036-kafka.md), [Runbook](../runbooks/0036-kafka.md) |
| [Messaging hardening](0037-messaging-optimization-hardening.md) | `POL-0037` | active | [Guide](../guides/0037-messaging-optimization-hardening.md), [Runbook](../runbooks/0037-messaging-optimization-hardening.md) |

### 06 Observability

| Policy | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Alertmanager](0039-alertmanager.md) | `POL-0039` | active | [Guide](../guides/0039-alertmanager.md), [Runbook](../runbooks/0039-alertmanager.md) |
| [Alloy](0040-alloy.md) | `POL-0040` | active | [Guide](../guides/0040-alloy.md), [Runbook](../runbooks/0040-alloy.md) |
| [Grafana](0041-grafana.md) | `POL-0041` | active | [Guide](../guides/0041-grafana.md), [Runbook](../runbooks/0041-grafana.md) |
| [Loki](0043-loki.md) | `POL-0043` | active | [Guide](../guides/0043-loki.md), [Runbook](../runbooks/0043-loki.md) |
| [Optimization hardening](0044-observability-optimization-hardening.md) | `POL-0044` | active | [Guide](../guides/0044-observability-optimization-hardening.md), [Runbook](../runbooks/0044-observability-optimization-hardening.md) |
| [Prometheus](0045-prometheus.md) | `POL-0045` | active | [Guide](../guides/0045-prometheus.md), [Runbook](../runbooks/0045-prometheus.md) |
| [Pushgateway](0046-pushgateway.md) | `POL-0046` | active | [Guide](../guides/0046-pushgateway.md), [Runbook](../runbooks/0046-pushgateway.md) |
| [Pyroscope](0047-pyroscope.md) | `POL-0047` | active | [Guide](../guides/0047-pyroscope.md), [Runbook](../runbooks/0047-pyroscope.md) |
| [Retention](0048-telemetry-retention.md) | `POL-0048` | active | — |
| [Tempo](0049-tempo.md) | `POL-0049` | active | [Guide](../guides/0049-tempo.md), [Runbook](../runbooks/0049-tempo.md) |
| [Gatus](0087-gatus.md) | `POL-0087` | draft | [Guide](../guides/0087-gatus.md), [Runbook](../runbooks/0087-gatus.md) |

### 07 Workflow

| Policy | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Airflow](0050-airflow.md) | `POL-0050` | active | [Guide](../guides/0050-airflow.md), [Runbook](../runbooks/0050-airflow.md) |
| [DAG deployment](0052-airflow-dag-lifecycle.md) | `POL-0052` | active | [Guide](../guides/0051-airflow-dag-lifecycle.md) |
| [n8n](0053-n8n.md) | `POL-0053` | active | [Guide](../guides/0053-n8n.md), [Runbook](../runbooks/0053-n8n.md) |
| [Optimization hardening](0054-workflow-optimization-hardening.md) | `POL-0054` | active | [Guide](../guides/0054-workflow-optimization-hardening.md), [Runbook](../runbooks/0054-workflow-optimization-hardening.md) |

### 08 AI

| Policy | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Ollama](0056-ollama.md) | `POL-0056` | active | [Guide](../guides/0056-ollama.md), [Runbook](../runbooks/0056-ollama.md) |
| [Open WebUI](0057-open-webui.md) | `POL-0057` | active | [Guide](../guides/0057-open-webui.md), [Runbook](../runbooks/0057-open-webui.md) |
| [Optimization hardening](0058-ai-optimization-hardening.md) | `POL-0058` | active | [Guide](../guides/0058-ai-optimization-hardening.md), [Runbook](../runbooks/0058-ai-optimization-hardening.md) |
| [ComfyUI](0081-comfyui.md) | `POL-0081` | draft | [Guide](../guides/0081-comfyui.md), [Runbook](../runbooks/0081-comfyui.md) |
| [Crawl4AI](0091-crawl4ai.md) | `POL-0091` | active | [Guide](../guides/0091-crawl4ai.md), [Runbook](../runbooks/0091-crawl4ai.md) |

### 09 Tooling

| Policy | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [IaC deployment policy](0060-iac-deployment.md) | `POL-0060` | active | — |
| [k6](0061-k6.md) | `POL-0061` | active | [Guide](../guides/0061-k6.md), [Runbook](../runbooks/0061-k6.md) |
| [Locust](0062-locust.md) | `POL-0062` | active | [Guide](../guides/0062-locust.md), [Runbook](../runbooks/0062-locust.md) |
| [Optimization hardening](0063-tooling-optimization-hardening.md) | `POL-0063` | active | [Guide](../guides/0063-tooling-optimization-hardening.md), [Runbook](../runbooks/0063-tooling-optimization-hardening.md) |
| [Performance testing](0064-performance-testing.md) | `POL-0064` | active | [Guide](../guides/0064-performance-testing.md), [Runbook](../runbooks/0064-performance-testing.md) |
| [Registry](0065-registry.md) | `POL-0065` | active | [Guide](../guides/0065-registry.md), [Runbook](../runbooks/0065-registry.md) |
| [SonarQube](0066-sonarqube.md) | `POL-0066` | active | [Guide](../guides/0066-sonarqube.md), [Runbook](../runbooks/0066-sonarqube.md) |
| [Terraform](0068-terraform.md) | `POL-0068` | active | [Guide](../guides/0068-terraform.md), [Runbook](../runbooks/0068-terraform.md) |
| [Terrakube](0069-terrakube.md) | `POL-0069` | active | [Guide](../guides/0069-terrakube.md), [Runbook](../runbooks/0069-terrakube.md) |
| [OpenTofu](0082-opentofu.md) | `POL-0082` | draft | [Guide](../guides/0082-opentofu.md), [Runbook](../runbooks/0082-opentofu.md) |
| [Renovate](0083-renovate.md) | `POL-0083` | draft | [Guide](../guides/0083-renovate.md), [Runbook](../runbooks/0083-renovate.md) |
| [dbt](0090-dbt.md) | `POL-0090` | active | [Guide](../guides/0090-dbt.md), [Runbook](../runbooks/0090-dbt.md) |
| [WireMock](0092-wiremock.md) | `POL-0092` | active | [Guide](../guides/0092-wiremock.md), [Runbook](../runbooks/0092-wiremock.md) |
| [Pact Broker](0093-pact-broker.md) | `POL-0093` | active | [Guide](../guides/0093-pact-broker.md), [Runbook](../runbooks/0093-pact-broker.md) |
| [Conftest](0095-conftest.md) | `POL-0095` | draft | [Guide](../guides/0095-conftest.md), [Runbook](../runbooks/0095-conftest.md) |

### 10 Communication

| Policy | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Stalwart mail](0070-mail.md) | `POL-0070` | active | [Guide](../guides/0070-mail.md), [Runbook](../runbooks/0070-mail.md) |
| [Mailpit](0084-mailpit.md) | `POL-0084` | draft | [Guide](../guides/0084-mailpit.md), [Runbook](../runbooks/0084-mailpit.md) |

### 11 Laboratory

| Policy | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Dozzle](0072-dozzle.md) | `POL-0072` | active | [Guide](../guides/0072-dozzle.md), [Runbook](../runbooks/0072-dozzle.md) |
| [Open Notebook](0073-open-notebook.md) | `POL-0073` | active | [Guide](../guides/0073-open-notebook.md), [Runbook](../runbooks/0073-open-notebook.md) |
| [Optimization hardening](0074-laboratory-optimization-hardening.md) | `POL-0074` | active | [Guide](../guides/0074-laboratory-optimization-hardening.md), [Runbook](../runbooks/0074-laboratory-optimization-hardening.md) |
| [RedisInsight](0076-redisinsight.md) | `POL-0076` | active | [Guide](../guides/0076-redisinsight.md), [Runbook](../runbooks/0076-redisinsight.md) |
| [SurrealDB](0080-surrealdb.md) | `POL-0080` | draft | [Guide](../guides/0080-surrealdb.md), [Runbook](../runbooks/0080-surrealdb.md) |
| [MLflow](0088-mlflow.md) | `POL-0088` | active | [Guide](../guides/0088-mlflow.md), [Runbook](../runbooks/0088-mlflow.md) |
| [JupyterLab](0089-jupyterlab.md) | `POL-0089` | active | [Guide](../guides/0089-jupyterlab.md), [Runbook](../runbooks/0089-jupyterlab.md) |

### 12 Infra Net

| Policy | ID | 상태 | 관련 문서 |
| --- | --- | --- | --- |
| [Compose network membership](0077-ip-address-management.md) | `POL-0077` | active | [Guide](../guides/0077-ip-address-management.md), [Runbook](../runbooks/0077-ip-address-management.md) |
| [hy-home.k8s integration](0096-k8s-integration.md) | `POL-0096` | draft | [Guide](../guides/0096-k8s-integration.md), [Runbook](../runbooks/0096-k8s-integration.md) |

## How to Work in This Area

1. 새 Policy는 [Policy template](../../99.templates/templates/operations/policy.template.md)으로 시작한다.
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
