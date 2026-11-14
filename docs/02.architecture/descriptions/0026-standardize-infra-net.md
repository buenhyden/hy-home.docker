---
title: "Compose Network Segmentation Architecture Description"
version: "1.8.2"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-14"
layer: "architecture"
artifact_id: "AD-0026"
parent_ids:
- "REQ-0023"
created: "2026-04-01"
---

# Compose Network Segmentation Architecture Description

## Overview

### Purpose and Readers

The Compose services once shared one bridge network, `infra_net`, so every
container could reach every other one. SPEC-0180 S05 replaced that mesh with
networks that each carry one kind of flow. Maintainers and operators need to
know which network owns a flow, who declares membership, and what still holds a
fixed address.

### System Boundary

- Root `docker-compose.yml` owns the network definitions and their explicit
  `10.250.x.0/24` subnets, so Docker's automatic pool cannot take one first.
  A few leaf-owned networks are declared by their service package instead.
- `infra/**` service Compose files own membership: a service joins a network
  only for a peer it actually uses.
- Docker internal DNS provides discovery.
- Fixed addresses are the exception and each has a stated reason; everything
  else takes a dynamic address.
- `project_net`, the host firewall and any cloud VPC stay outside this
  architecture's ownership. No service joins `k3d-hyhome`; the owner removed
  the k3d integration on 2026-09-23. This removes shared-bridge membership, not the separately approved Kubernetes LAN endpoints governed by POL-0096.

## Context and Constraints

### Context

Traefik routes gateway traffic to backends over `edge_net` and the per-backend ingress networks, and Prometheus and Alloy scrape targets over `obs_net` and the consumer-only metrics networks. Restic offsite traffic leaves for Cloudflare R2, and the Crawl4AI and n8n egress networks reach public addresses.

### Constraints

Fixed addresses are the exception and each has a stated reason; a service joins a segmented network only for a peer it uses. Duplicate or out-of-subnet static addresses fail validation, and runtime inspection is allowed only in an approved environment.

## Current Structure

### Building Blocks

`infra_net` was removed in two phases: services first joined their target
networks beside it, then it left the services and the root.

#### Networks

| Network | Subnet | Members | Flow |
| --- | --- | --- | --- |
| `edge_net` | 10.250.1.0/24, dynamic from .128/25 | Traefik (fixed .2, aliases `keycloak.`/`auth.${DEFAULT_URL}`), OAuth2 Proxy, every routed backend that has its own authentication | gateway → backend; backend → Traefik alias for OIDC discovery |
| `mng_data_net` | 10.250.2.0/24 | `mng-pg`, `mng-valkey`, OAuth2 Proxy Valkey, their exporters and clients (including Pact Broker) | client → PostgreSQL/Valkey |
| `object_net` | 10.250.3.0/24 | `seaweedfs-s3`, Loki, Tempo, MLflow, Terrakube, bucket jobs | S3 client → object store; Iceberg client → REST catalog 8181 |
| `seaweed_internal` | 10.250.4.0/24, internal | SeaweedFS master, volume, filer, S3 | storage-internal only |
| `obs_net` | 10.250.5.0/24 | Prometheus, Alloy, Loki, Tempo, Pyroscope, Grafana, Alertmanager, Pushgateway, exporters, every scrape target, k6 | scrape, push, datasource queries |
| `kafka_net` | 10.250.6.0/24 | brokers, Schema Registry, Connect, REST Proxy, kafbat UI, exporter, init | broker clients |
| `secrets_net` | 10.250.7.0/24 | OpenBao and its agent | agent → secret store |
| `ai_net` | 10.250.8.0/24 | Ollama, its exporter, Open WebUI, Qdrant, Open Notebook, SurrealDB, MLflow | AI clients → model, vector and tracking backends |
| `airflow_net`, `n8n_net`, `terrakube_net` | 10.250.10.0/24, 10.250.11.0/24, 10.250.13.0/24 | the application's own services and private stores | application-internal |
| `mail_net` | 10.250.14.0/24 | Mailpit; no other root service joins it | SMTP capture on Mailpit 1025 |
| `quality_otlp_net` | 10.250.17.0/24, internal | Alloy and the per-run k6 metrics relays that `metrics_relay.py` attaches | relay → authenticated Alloy OTLP receiver 4319 (SPEC-0214) |
| `dev_data_net` | 10.250.15.0/24 | `dev-pg`, `dev-valkey`, their exporters and provision jobs, Kafka Connect, RedisInsight | development client → dev PostgreSQL/Valkey |
| `experience_ingress_net` | 10.250.16.0/24, internal | Traefik and Storybook | gateway → Storybook only |
| `redisinsight_ingress_net` | 10.250.18.0/24, internal, isolated, dynamic from .128/25 | Traefik and RedisInsight (fixed .3) | gateway → RedisInsight only; no host address |
| `<service>_ingress_net` (16) | 10.250.24.0/24–10.250.40.0/24, internal, isolated, dynamic from .128/25 | Traefik and one SSO-only backend each (SPEC-0266, ADR-0061) | gateway → that backend only |
| `seaweedfs_s3_metrics_net` | 10.250.41.0/24, internal, isolated, dynamic from .128/25 | `seaweedfs-s3` (metrics listener bound to fixed .2), Prometheus, Alloy | metrics/pprof scrape of `seaweedfs-s3:9327`; reaches no master/volume/filer API |
| `oauth2_proxy_metrics_net` | 10.250.43.0/24, internal, isolated, dynamic from .128/25 | OAuth2 Proxy (metrics listener bound to fixed .2, alias `oauth2-proxy-metrics`) and Prometheus | metrics scrape of 44180 only (SPEC-0267) |
| `keycloak_management_net` | 10.250.44.0/24, internal, isolated, dynamic from .128/25 | Keycloak (management listener bound to fixed .2, alias `keycloak-management`), Prometheus and Gatus | health and metrics on 9000 only (SPEC-0267) |
| `grafana_pprof_net` | 10.250.45.0/24, internal, isolated, dynamic from .128/25 | Grafana (pprof bound to fixed .2, alias `grafana-pprof`) and Alloy | profile scrape of 6060 only (SPEC-0267) |
| `traefik_metrics_net` | 10.250.46.0/24, internal, isolated, dynamic from .128/25 | Traefik (metrics and ping entrypoint bound to fixed .2, alias `traefik-metrics`) and Prometheus | metrics scrape of 8082 only (SPEC-0267) |
| `seaweedfs_metrics_net` | 10.250.19.0/24, internal, isolated | Prometheus and the SeaweedFS master, volume and filer | metrics scrape only |
| `n8n_blog_ingest_net` | 10.250.20.0/24, internal, isolated | `n8n-worker` and `blog-ingestion` | worker → Blog-data ingestion Gateway |
| `blog_export_net` | 10.250.21.0/24, internal, isolated | Traefik and `blog-ingestion` | exact-path Traefik routes → Gateway; no published port |
| `n8n_worker_runner_net` | 10.250.23.0/24, internal, isolated, dynamic from .128/25 | `n8n-worker` (task broker bound to fixed .2, `10.250.23.2`) with `n8n-task-runner-worker` | broker ↔ its external Code runner only; `10.250.22.0/24` (the removed main runner network, SPEC-0269) is not reused |
| `n8n_search_net` | leaf-owned, internal | `n8n` and `searxng` | n8n Assistant web search → SearXNG only; no egress |
| `n8n_search_outbound_net` | leaf-owned | `searxng` | SearXNG → public search engines; no inbound path, no destination or port limit |
| `n8n_sandbox_net` | 10.250.210.0/24, leaf-owned, internal | `n8n` and `n8n-sandbox-api` | n8n → sandbox API only |
| `n8n_sandbox_runner_net` | 10.250.211.0/24, leaf-owned, internal | `n8n-sandbox-api` and `n8n-sandbox-runner-1` | API ↔ runner registration and control; the runner never shares a network with n8n |
| `n8n_sandbox_outbound_net` | 10.250.212.0/24, leaf-owned | `n8n-sandbox-runner-1` | runner and its sandboxes → internet; the runner's built-in egress rules block sandbox traffic to private, link-local and loopback ranges (measured 2026-11-09); owner decision 2026-11-09 |
| `crawl4ai_net` | leaf-owned, internal | Crawl4AI and admitted consumers (POL-0091) | consumer → Crawl4AI API; no egress |
| `crawl4ai_egress_net` | 10.250.200.0/29, leaf-owned, internal (named egress-isolation exception in REQ-0023-FR-0002) | Crawl4AI (fixed .3) and `crawl4ai-egress` (fixed .2) | crawler → egress gateway |
| `crawl4ai_outbound_net` | leaf-owned | `crawl4ai-egress` | gateway → public addresses on ports 80/443 only; non-global and IPv6 addresses refused |
| `comfyui_egress_net` | 10.250.42.0/24, non-internal, dynamic from .128/25 | ComfyUI, only while the maintenance overlay `docker-compose.egress.yml` is attached | model and custom-node downloads; no other container joins it (SPEC-0268) |
| `restic_offsite_net` | leaf-owned | `restic-offsite` | backup egress to Cloudflare R2 only (ADR-0056) |

Services with no container peer (Renovate, OpenTofu) use the project default
network. WireMock also uses it until a named consumer exists;
that network is then its trust boundary, and the consumer gets a scoped network. `restic`, `backup-sqlite-export` and Conftest keep
`network_mode: none`, and `node-exporter` uses `network_mode: host`; only `restic-offsite` has egress. Registry joins `obs_net` for its metrics scrape; its loopback host publication remains separately declared. Mailpit uses `mailpit_ingress_net` for its routed UI and `mail_net` for SMTP. LABs, including Stalwart, declare their own networks in their standalone projects.

### Runtime and Deployment

#### Runtime View

Services resolve names through Docker DNS and use static addresses only where
tracked Compose explicitly declares them. New allocation selects an unused
address within the appropriate group, updates the owning Compose file and this
view together, and preserves any additional network membership.

A service joins a segmented network only for a peer it actually uses: Traefik
routes and Prometheus scrape targets are the fixed flows, and every other flow
comes from the service's own configuration. Traefik is the only fixed address
on `edge_net` because OAuth2 Proxy and Airflow trust it as the proxy; the other
fixed addresses are RedisInsight on `redisinsight_ingress_net`, the
Crawl4AI pair on `crawl4ai_egress_net`, and the `.2` address of each
consumer-only metrics or management network: `seaweedfs_s3_metrics_net`
(10.250.41.2), `n8n_worker_runner_net` (10.250.23.2, the n8n broker),
`oauth2_proxy_metrics_net` (10.250.43.2), `keycloak_management_net`
(10.250.44.2), `grafana_pprof_net` (10.250.45.2) and `traefik_metrics_net`
(10.250.46.2). 10.250.9.0/24 is no longer allocated in the root. A
multi-homed server listens on `0.0.0.0`, never on the address its own name
resolves to, because that resolves on only one of its networks. The exception
is a listener without its own authentication: it binds only to its fixed `.2`
address on its consumer-only internal network, so no other network reaches it.

#### Deployment View

Docker Compose creates every network from the root definition. Static
verification uses `scripts/validation/validate-docker-compose.sh`, the
`NetworkSegmentationContractTests` contracts and a repository search for
`ipv4_address` declarations. Runtime inspection is allowed only in an approved
environment and compares `docker network inspect` output with the tracked
Compose configuration.

## Interfaces

### Contracts

- Each network in the Networks table names its subnet, members and flow.
- Services resolve names through Docker DNS and use static addresses only where tracked Compose declares them.
- A multi-homed server listens on `0.0.0.0`, and a listener without its own authentication binds only to its fixed `.2` address.

### Failure Boundaries

Internal and isolated networks keep a flow from reaching any other member, and a listener without its own authentication binds only to its consumer-only network. A network named here but absent from the root definition, or a member list that drifts from the leaf Compose files, misleads allocation; the leaf files win.

## Decisions

### Decision Links

- [ADR-0055 Segmented per-flow networks](../decisions/0055-segmented-per-flow-networks.md)

### Quality and Risks

#### Quality Attributes

- Reliability: duplicate or out-of-subnet static addresses fail validation.
- Security: services are exposed through the gateway unless their architecture
  explicitly owns another boundary.
- Scalability: each /24 holds its members with a dynamic range reserved above
  the fixed addresses.
- Operability: one Architecture Description and one Operations subject own the
  structural map and procedure.

#### Risks

- A network named here but absent from the root definition, or a member list
  that drifts from the leaf Compose files, misleads allocation; the leaf files
  win.

## Traceability

### Requirement Mapping

- [REQ-0023 Compose network segmentation](../../01.requirements/0023-standardize-infra-net.md)

### Currentness and Lineage

- SPEC-0180 HOME development convergence and SPEC-0098 (retired; version history)
- [IP address management guide](../../05.operations/guides/02-gateway-and-networking/0077-ip-address-management.md)
- [IP address management policy](../../05.operations/policies/02-gateway-and-networking/0077-ip-address-management.md)
- [IP address management runbook](../../05.operations/runbooks/02-gateway-and-networking/0077-ip-address-management.md)
- This document carries the SPEC-0267 secondary-listener hardening outcome; that package is retired and its body is in version history.

#### Evolution

- WireMock moves to a scoped network once a named consumer exists.

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
