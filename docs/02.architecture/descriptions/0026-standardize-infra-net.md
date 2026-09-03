---
title: infra_net Architecture Description
version: 1.0.0
type: sdlc/architecture-description
layer: architecture
status: active
owner: "@buenhyden"
artifact_id: AD-0026
parent_ids:
  - REQ-0023
created: 2026-04-01
updated: 2026-09-01
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
| 172.19.0.9-10 | Vault and Vault Agent |
| 172.19.0.11-16 | PostgreSQL and management database core |
| 172.19.0.20-28 | Observability stack |
| 172.19.0.29, 39 | MinIO and bucket job |
| 172.19.0.30-38 | Kafka stack |
| 172.19.0.41-47 | Valkey cluster |
| 172.19.0.50-59 | PostgreSQL cluster |
| 172.19.0.61 | Neo4j |
| 172.19.0.70-71 | OpenSearch |
| 172.19.0.80-85 | n8n workflow |
| 172.19.0.90-100 | Airflow workflow |
| 172.19.0.120 | Terraform / Atlantis |
| 172.19.0.121 | RedisInsight |
| 172.19.0.122-123 | Open Notebook services |
| 172.19.0.130-132 | ksqlDB stack |
| 172.19.0.140-144 | SeaweedFS |
| 172.19.0.150-151 | Cassandra |
| 172.19.0.160-163 | CouchDB |
| 172.19.0.170-175 | MongoDB |
| 172.19.0.179-191 | Supabase |
| 172.19.0.200 | RabbitMQ |
| 172.19.0.201, 211 | Ollama and exporter |
| 172.19.0.202 | Qdrant |
| 172.19.0.220-229 | Laboratory, tooling, and mail services |
| 172.19.0.250, 253 | Locust |
| 172.19.0.251 | Open WebUI |

The Compose files are the executable source for individual addresses. This
table is the current structural allocation view and must be updated in the same
change as an address reassignment.

## Data Flow

Services resolve names through Docker DNS and use static addresses only where
tracked Compose explicitly declares them. New allocation selects an unused
address within the appropriate group, updates the owning Compose file and this
view together, and preserves any additional network membership.

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
- [SPEC-0098 completed implementation outcome](../../98.archive/completed/03.specs/0098-standardize-infra-net/spec.md)
- [IP address management guide](../../05.operations/catalog/12-infra-net/0077-ip-address-management/guide.md)
- [IP address management policy](../../05.operations/catalog/12-infra-net/0077-ip-address-management/policy.md)
- [IP address management runbook](../../05.operations/catalog/12-infra-net/0077-ip-address-management/runbook.md)
