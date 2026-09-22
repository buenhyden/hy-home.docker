---
title: "infra_net Architecture Description"
version: "1.2.1"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "architecture"
artifact_id: "AD-0026"
parent_ids:
- "REQ-0023"
created: "2026-04-01"
---
# infra_net Architecture Description

## Context and Stakeholders

infra_net은 repository의 Docker Compose infrastructure service가 공유하는
bridge network다. Maintainer와 operator는 root IPAM, service network
membership, static address allocation의 current owner와 변경 절차를 명확히
구분해야 한다.

## System Boundaries

- Root docker-compose.yml은 infra_net 이름, bridge driver, subnet
  172.19.0.0/16, gateway 172.19.0.1 기본값을 소유한다.
- 동적 주소는 `ip_range` 172.19.1.0/24(`INFRA_IP_RANGE`)에서만 할당되므로
  172.19.0.x의 static allocation과 겹치지 않는다. 기존 network에는 network를
  재생성해야 적용된다.
- infra/**의 service Compose 파일은 network membership과 필요한 static
  ipv4_address를 소유한다.
- Docker internal DNS가 기본 service discovery를 제공한다.
- project_net, k3d-hyhome, cloud VPC, host firewall은 이 아키텍처의 IPAM
  소유 범위 밖이며 기존 연결을 임의로 제거하지 않는다.

## Components

Root Compose가 global network를 정의하고 include된 tier Compose가 service를
연결한다. 현재 tracked static allocation은 다음 그룹 범위로 수렴한다.

| Address or range | Current owner |
| --- | --- |
| 172.19.0.2 | Gateway / Traefik |
| 172.19.0.3-6 | Authentication / Keycloak and OAuth2 Proxy |
| 172.19.0.7 | Tooling registry |
| 172.19.0.8 | InfluxDB |
| 172.19.0.9-10 | Legacy Vault and Vault Agent |
| 172.19.0.11-16 | PostgreSQL and management database core |
| 172.19.0.17-18 | OpenBao and OpenBao Agent |
| 172.19.0.19 | cAdvisor |
| 172.19.0.20-28 | Observability stack |
| 172.19.0.29, 39 | released (MinIO removed, SPEC-0180 S07) |
| 172.19.0.30-38 | Kafka stack |
| 172.19.0.40 | Debezium source provisioning job |
| 172.19.0.41-47 | Valkey cluster |
| 172.19.0.48 | Valkey cluster init job |
| 172.19.0.50-59 | PostgreSQL cluster |
| 172.19.0.61 | Neo4j |
| 172.19.0.70-71 | OpenSearch |
| 172.19.0.72-74 | OpenSearch cluster nodes |
| 172.19.0.80-85 | n8n workflow |
| 172.19.0.90-100 | Airflow workflow |
| 172.19.0.110-111 | MLflow and JupyterLab |
| 172.19.0.112 | DCGM GPU exporter |
| 172.19.0.113-114 | dbt and its provisioning job |
| 172.19.0.115-116 | MLflow provisioning jobs |
| 172.19.0.121 | RedisInsight |
| 172.19.0.122-123 | Open Notebook services |
| 172.19.0.130-132 | ksqlDB stack |
| 172.19.0.140-144 | SeaweedFS |
| 172.19.0.145-148 | released (MinIO cluster removed, SPEC-0180 S07) |
| 172.19.0.150-151 | Cassandra |
| 172.19.0.152-153 | StarRocks FE and BE |
| 172.19.0.160-163 | CouchDB |
| 172.19.0.170-175 | MongoDB |
| 172.19.0.176 | MongoDB key generator job |
| 172.19.0.179-191 | Supabase |
| 172.19.0.201, 211 | Ollama and exporter |
| 172.19.0.202 | Qdrant |
| 172.19.0.203 | ComfyUI |
| 172.19.0.221 | Dozzle |
| 172.19.0.222 | Nginx gateway |
| 172.19.0.223 | SonarQube |
| 172.19.0.224 | OpenTofu |
| 172.19.0.225-227 | Terrakube API, UI, and executor |
| 172.19.0.228 | Stalwart |
| 172.19.0.230 | Mailpit |
| 172.19.0.231 | Gatus |
| 172.19.0.232 | Renovate |
| 172.19.0.250, 253 | Locust |
| 172.19.0.251 | Open WebUI |
| 172.19.0.252 | k6 |
| 172.19.1.0/24 | Dynamic range (`INFRA_IP_RANGE`); no fixed owner |

The Compose files are the executable source for individual addresses. This
table is the current structural allocation view and must be updated in the same
change as an address reassignment.

### Segmented networks (SPEC-0180 S05)

The full `infra_net` mesh is being replaced by networks that each carry one
kind of flow. Phase 1 attaches every service to its target networks beside
`infra_net`; phase 2 removes `infra_net` after live verification. Root Compose
owns the definitions and explicit `10.250.x.0/24` subnets, so Docker's
automatic address pool cannot take one first.

| Network | Subnet | Members | Flow |
| --- | --- | --- | --- |
| `edge_net` | 10.250.1.0/24, dynamic from .128/25 | Traefik (fixed .2, aliases `keycloak.`/`auth.${DEFAULT_URL}`), Nginx, OAuth2 Proxy, every routed backend | gateway → backend; backend → Traefik alias for OIDC discovery |
| `mng_data_net` | 10.250.2.0/24 | `mng-pg`, `mng-valkey`, OAuth2 Proxy Valkey, their exporters and clients | client → PostgreSQL/Valkey |
| `object_net` | 10.250.3.0/24 | `seaweedfs-s3`, Loki, Tempo, MLflow, Terrakube, Nginx, bucket jobs | S3 client → object store |
| `seaweed_internal` | 10.250.4.0/24, internal | SeaweedFS master, volume, filer, S3 | storage-internal only |
| `obs_net` | 10.250.5.0/24 | Prometheus, Alloy, Loki, Tempo, Pyroscope, Grafana, Alertmanager, Pushgateway, exporters, every scrape target, k6 | scrape, push, datasource queries |
| `kafka_net` | 10.250.6.0/24 | brokers, Schema Registry, Connect, REST Proxy, kafbat UI, exporter, init, ksqlDB | broker clients |
| `secrets_net` | 10.250.7.0/24 | OpenBao and its agent; Vault and its agent until S08 | agent → secret store |
| `ai_net` | 10.250.8.0/24 | Ollama, its exporter, Open WebUI, Qdrant, Open Notebook, SurrealDB, JupyterLab, MLflow | AI clients → model, vector and tracking backends |
| `lab_net` | 10.250.9.0/24 | LAB clusters (Valkey, PostgreSQL/etcd, Cassandra, CouchDB, MongoDB, StarRocks) and OpenSearch nodes | cluster-internal and init jobs |
| `airflow_net`, `n8n_net`, `supabase_net`, `terrakube_net` | 10.250.10–13.0/24 | the application's own services and private stores | application-internal |
| `crawl4ai_net` | leaf-owned | Crawl4AI | isolated SSRF-capable egress (unchanged) |
| `k3d-hyhome` | external | Traefik, Prometheus, Alloy, Loki, Tempo, Grafana, `mng-valkey`, OpenBao, `pg-router` | measured k8s consumers; `mng-pg` and Vault leave in phase 2 and S08 |

Services with no container peer (Registry, Renovate, OpenTofu, Locust) use the
project default network in phase 2. `restic` and `backup-sqlite-export` keep
`network_mode: none`. Mail networking is added with Stalwart in S17.

## Data Flow

Services resolve names through Docker DNS and use static addresses only where
tracked Compose explicitly declares them. New allocation selects an unused
address within the appropriate group, updates the owning Compose file and this
view together, and preserves any additional network membership.

A service joins a segmented network only for a peer it actually uses: Traefik
routes and Prometheus scrape targets are the fixed flows, and every other flow
comes from the service's own configuration. Traefik is the only fixed address
on a segmented network because OAuth2 Proxy and Airflow trust it as the proxy;
the OpenSearch cluster nodes hold fixed `lab_net` addresses because they
announce them to each other. A multi-homed server listens on `0.0.0.0`, never
on the address its own name resolves to, because that resolves on only one of
its networks.

## Deployment View

Docker Compose creates infra_net from the root definition. Static verification
uses scripts/validation/validate-docker-compose.sh and a repository search for
infra_net and ipv4_address declarations. Runtime inspection is allowed only in
an approved environment and compares docker network inspect output with the
tracked Compose configuration.

## Quality Attributes

- Reliability: duplicate or out-of-subnet static addresses fail validation.
- Security: services are exposed through the gateway unless their architecture
  explicitly owns another boundary.
- Scalability: the /16 subnet supports grouped allocation without overlapping
  current ranges.
- Operability: one Architecture Description and one Operations subject own the
  structural map and procedure.

## Traceability

- [REQ-0023 Standardize infra_net](../../01.requirements/0023-standardize-infra-net.md)
- [ADR-0026 Standardize infra_net](../decisions/0026-standardize-infra-net.md)
- [SPEC-0180 HOME development convergence](../../03.specs/0180-home-dev-convergence/spec.md)
- [SPEC-0098 completed implementation outcome](../../98.archive/completed/03.specs/0098-standardize-infra-net/spec.md)
- [IP address management guide](../../05.operations/catalog/12-infra-net/0077-ip-address-management/guide.md)
- [IP address management policy](../../05.operations/catalog/12-infra-net/0077-ip-address-management/policy.md)
- [IP address management runbook](../../05.operations/catalog/12-infra-net/0077-ip-address-management/runbook.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
