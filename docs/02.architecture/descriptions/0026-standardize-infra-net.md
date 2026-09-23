---
title: "Compose Network Segmentation Architecture Description"
version: "1.2.4"
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
# Compose Network Segmentation Architecture Description

## Context and Stakeholders

The Compose services once shared one bridge network, `infra_net`, so every
container could reach every other one. SPEC-0180 S05 replaced that mesh with
networks that each carry one kind of flow. Maintainers and operators need to
know which network owns a flow, who declares membership, and what still holds a
fixed address.

## System Boundaries

- Root `docker-compose.yml` owns the network definitions and their explicit
  `10.250.x.0/24` subnets, so Docker's automatic pool cannot take one first.
- `infra/**` service Compose files own membership: a service joins a network
  only for a peer it actually uses.
- Docker internal DNS provides discovery. A name shared across networks
  resolves on the first-ranked network, so a multi-homed server binds
  `0.0.0.0` and never the address of its own name.
- Fixed addresses are the exception and each has a stated reason; everything
  else takes a dynamic address.
- `project_net`, `k3d-hyhome`, the host firewall and any cloud VPC stay outside
  this architecture's ownership and keep their existing connections.

## Components

### Networks (SPEC-0180 S05)

Phase 1 attached every service to its target networks beside `infra_net`;
phase 2 removed `infra_net` from the services and from the root. Root Compose
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
| `secrets_net` | 10.250.7.0/24 | OpenBao and its agent | agent → secret store |
| `ai_net` | 10.250.8.0/24 | Ollama, its exporter, Open WebUI, Qdrant, Open Notebook, SurrealDB, JupyterLab, MLflow | AI clients → model, vector and tracking backends |
| `lab_net` | 10.250.9.0/24 | LAB clusters (Valkey, PostgreSQL/etcd, Cassandra, CouchDB, MongoDB, StarRocks) and OpenSearch nodes | cluster-internal and init jobs |
| `airflow_net`, `n8n_net`, `supabase_net`, `terrakube_net` | 10.250.10–13.0/24 | the application's own services and private stores | application-internal |
| `crawl4ai_net` | leaf-owned | Crawl4AI | isolated SSRF-capable egress (unchanged) |
| `k3d-hyhome` | external | Traefik, Prometheus, Alloy, Loki, Tempo, Grafana, `mng-valkey`, OpenBao, `pg-router` | measured k8s consumers |

Services with no container peer (Registry, Renovate, OpenTofu, Locust) use the
project default network. WireMock also uses it until a named consumer exists;
that network is then its trust boundary, and the consumer gets a scoped network. `restic` and `backup-sqlite-export` keep
`network_mode: none`. Stalwart and Mailpit are on `edge_net`; a dedicated mail network is added in S17.

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

Docker Compose creates every network from the root definition. Static
verification uses scripts/validation/validate-docker-compose.sh, the
`NetworkSegmentationContractTests` contracts and a repository search for
`ipv4_address` declarations. Runtime inspection is allowed only in an approved
environment and compares `docker network inspect` output with the tracked
Compose configuration.

## Quality Attributes

- Reliability: duplicate or out-of-subnet static addresses fail validation.
- Security: services are exposed through the gateway unless their architecture
  explicitly owns another boundary.
- Scalability: each /24 holds its members with a dynamic range reserved above
  the fixed addresses.
- Operability: one Architecture Description and one Operations subject own the
  structural map and procedure.

## Traceability

- [REQ-0023 Compose network segmentation](../../01.requirements/0023-standardize-infra-net.md)
- [ADR-0026 Standardize infra_net (the superseded single-mesh decision)](../decisions/0026-standardize-infra-net.md)
- [SPEC-0180 HOME development convergence](../../03.specs/0180-home-dev-convergence/spec.md)
- [SPEC-0098 completed implementation outcome](../../98.archive/completed/03.specs/0098-standardize-infra-net/spec.md)
- [IP address management guide](../../05.operations/catalog/12-infra-net/0077-ip-address-management/guide.md)
- [IP address management policy](../../05.operations/catalog/12-infra-net/0077-ip-address-management/policy.md)
- [IP address management runbook](../../05.operations/catalog/12-infra-net/0077-ip-address-management/runbook.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
