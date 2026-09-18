---
title: "Reference: Local Docker Service Consolidation"
version: "0.4.0"
type: "reference/research"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-18"
layer: "references"
artifact_id: "RES-0002-m0021"
parent_ids:
- "RES-0002"
created: "2026-09-18"
observed_at: "2026-09-18"
---

# Reference: Local Docker Service Consolidation

## Question

Which services in `infra/` should remain available for local Docker use, which
belong in optional profiles, and which are candidates for removal because their
role is unused or duplicated?

## Evidence Boundary

This is non-normative research. Tracked Compose definitions and the observed
local container list do not prove business necessity, data ownership, backup
success, or safe deletion. No service was stopped, removed, migrated, or
reconfigured during this observation.

The repository currently contains 41 Compose definitions under `infra/`. The
2026-09-18 local observation showed active workloads spanning gateway, identity,
security, management data, object storage, messaging, workflow, AI, and
observability. The observation also showed stopped or created one-shot jobs;
those states are not evidence that their parent service is unused.

## Consolidated Research Ownership

This member is the single owner for the functional service map: overlap,
open-source/license suitability, local Docker availability, baseline versus
optional profile, and removal-candidate reasoning.

| Existing research surface | Retained responsibility | Consolidation result |
| --- | --- | --- |
| [RES-0002-m0005](m0005-docker-compose-infrastructure.md) | Compose include/profile semantics, topology, static inventory, hardening, image provenance, and validation | Do not repeat service-role or removal recommendations there. |
| [RES-0002-m0020](m0020-workspace-baseline.md) | Current repository counts, evidence classes, and baseline routing | Cite this member for service-role conclusions instead of copying its tables. |
| [RES-0085](../0085-workspace-engineering-main-baseline-assessment/README.md) | Dated 2026-09-05 assessment envelope and identity recovery | Historical carrier only; it is not a current service inventory. |
| [RES-0096](../0096-archive-disposition-consistency/README.md) | Stage 98 archive consistency review | Out of scope for local service classification. |

No duplicate service-classification member is created. Future service overlap,
license, or local-removal findings should update this member or create a new
member only when the question and evidence model are materially different.

## Selection Rules

1. Keep a service when it has a distinct workload contract or is an active
   dependency of another local service.
2. Move a service to an optional profile when it is useful but not required for
   the local baseline.
3. Remove a service only after its repository consumers, persistent data,
   secrets, ports, routes, and operational documents have been dispositioned.
4. A retained service must have an official or project-maintained Docker image
   or Compose deployment and a license acceptable to the repository owner.
5. A compatible datastore is not automatically a replacement: migration,
   backup, client compatibility, and recovery evidence are required.

## Findings

### 2026-09-18 Local Runtime Reconciliation

Docker Engine `29.8.1`, Docker Compose `v5.5.1`, and the root
`docker compose config --quiet` check succeeded. The local container listing
showed `influxdb`, `comfyui`, `neo4j`, and `qdrant` running and healthy. They
are not removal candidates based on this observation. `schema-registry` also
runs as part of the Kafka stack and must not be treated as an independent
unused service.

Homer, RabbitMQ, and Portainer were not present in the local container listing.
After approval, their Compose leaves, root includes, active environment/secret
registry entries, routes, tier references, hardening checks, and active Stage 05
service documents were removed. Historical archive and migration records remain
unchanged. No running data service was stopped or migrated.

| Candidate | Runtime observation | Current disposition | Required next evidence |
| --- | --- | --- | --- |
| Homer | Not present | Removed after approval | Historical references remain only in archive evidence. |
| RabbitMQ | Not present | Removed after approval | No active AMQP consumer was found; historical references remain only in archive evidence. |
| Portainer | Not present | Removed after approval | Docker-socket management UI and its active route/operations contract were removed. |
| InfluxDB | Running healthy | Keep optional; no deletion | Confirm retention and dashboard consumers before any data migration or volume disposition. |
| ComfyUI | Running healthy | Keep optional | Review third-party image and GPU workload ownership; do not infer redundancy with Ollama. |
| Neo4j | Running healthy | Keep optional | Confirm graph datasets and dashboards before removal. |
| Qdrant | Running healthy | Keep optional | Confirm vector collections and RAG consumers before removal. |
| Open Notebook, Supabase, PostgreSQL cluster, Terrakube, Syncthing, Registry, SonarQube, k6, Locust | Not observed in the current container listing | Keep as optional profiles | Check application consumers, persistent data, secrets, routes, and Stage 05 ownership individually. |

No Compose service or Stage 05 document is deleted by this observation. A
future approved cleanup must retire the service definition, root include,
profile vocabulary, env/secret declarations, routes, infra README entry,
service README, and Stage 05 guide/policy/runbook as one traceable change.

| Service group | Role relationship | Official source evidence | Disposition |
| --- | --- | --- | --- |
| Kafka / RabbitMQ | Kafka is durable event streaming; RabbitMQ is AMQP/task messaging | [Kafka documentation](https://kafka.apache.org/documentation/), [RabbitMQ documentation](https://www.rabbitmq.com/docs), [RabbitMQ license](https://github.com/rabbitmq/rabbitmq-server/blob/main/LICENSE-MPL-RabbitMQ) | Keep Kafka as the local event baseline. Keep RabbitMQ optional unless no AMQP consumer exists. |
| MinIO / SeaweedFS | Both provide object storage, but SeaweedFS also targets distributed file and filer workloads | [MinIO license](https://github.com/minio/minio/blob/master/LICENSE), [SeaweedFS license](https://github.com/seaweedfs/seaweedfs/blob/master/LICENSE), [SeaweedFS Docker guide](https://github.com/seaweedfs/seaweedfs/wiki/Getting-Started) | Do not run both by default. Retain MinIO while current observability and tooling consumers use it; consider SeaweedFS only through a migration task. |
| mng-db / Supabase / PostgreSQL cluster | Management PostgreSQL, application platform PostgreSQL, and HA PostgreSQL are different contracts | [PostgreSQL license](https://github.com/postgres/postgres/blob/master/COPYRIGHT), [Supabase self-hosted Docker](https://supabase.com/docs/guides/self-hosting/docker), [Patroni license](https://github.com/patroni/patroni/blob/master/LICENSE) | Keep mng-db. Make Supabase and PostgreSQL cluster optional. Do not merge databases without migration and rollback evidence. |
| Valkey / Redis / RedisInsight | Valkey and Redis are datastores; RedisInsight is an admin UI | [Valkey license](https://raw.githubusercontent.com/valkey-io/valkey/unstable/COPYING), [Valkey Docker image](https://hub.docker.com/r/valkey/valkey), [Redis licenses](https://redis.io/legal/licenses/), [RedisInsight license](https://github.com/RedisInsight/RedisInsight/blob/main/LICENSE) | Keep Valkey. Keep RedisInsight optional and separately review its SSPL license. Remove any Redis server definition only after checking client and module compatibility. |
| Ollama / ComfyUI | Text/multimodal inference versus visual-generation workflows | [Ollama Docker](https://docs.ollama.com/docker), [Ollama license](https://github.com/ollama/ollama/blob/main/LICENSE), [ComfyUI repository](https://github.com/Comfy-Org/ComfyUI), [ComfyUI license](https://github.com/Comfy-Org/ComfyUI/blob/master/LICENSE) | Keep as separate optional AI profiles. Remove ComfyUI only if visual generation is not a requirement. Review the current third-party ComfyUI image separately. |
| Portainer / Dozzle / Homer / RedisInsight | Docker control, log viewing, dashboard links, and datastore administration | [Portainer Docker install](https://docs.portainer.io/start/install-ce/server/docker/linux), [Dozzle Docker guide](https://dozzle.dev/guide/getting-started), [Dozzle license](https://github.com/amir20/dozzle/blob/master/LICENSE), [Homer license](https://github.com/bastienwirtz/homer/blob/main/LICENSE) | Keep Portainer and Dozzle optional-admin services. Homer is the first removal candidate if its dashboard links are unused. RedisInsight remains datastore-specific. |
| Prometheus / Loki / Tempo / InfluxDB | Metrics, logs, traces, and general-purpose time-series analytics | [Prometheus overview](https://prometheus.io/docs/introduction/overview/), [Loki license](https://github.com/grafana/loki/blob/main/LICENSE), [Tempo Compose examples](https://github.com/grafana/tempo/tree/main/example/docker-compose), [InfluxDB Docker Compose](https://docs.influxdata.com/influxdb/v2/install/use-docker-compose/) | Keep the LGTM stack. Make InfluxDB optional; remove only after checking Telegraf, Flux/InfluxQL, dashboards, and retained data. |
| SonarQube / Terrakube / Syncthing / Registry / k6 / Locust | Distinct code quality, Terraform orchestration, file sync, image registry, and test workloads | [SonarQube image](https://hub.docker.com/_/sonarqube), [Terrakube repository](https://github.com/terrakube-io/terrakube), [Syncthing license](https://github.com/syncthing/syncthing/blob/main/LICENSE), [Distribution Registry](https://distribution.github.io/distribution/) | Keep optional. Remove only unused tooling after checking CI, Terraform state, synchronized paths, image cache, and test scripts. |
| Open Notebook / Neo4j / Qdrant | Research notebook, graph database, and vector database | [Open Notebook repository](https://github.com/lfnovo/open-notebook), [Neo4j Docker](https://neo4j.com/docs/operations-manual/current/docker/introduction/), [Qdrant quickstart](https://qdrant.tech/documentation/quickstart/) | Keep separate optional services. No evidence supports treating any one as a drop-in replacement for the other. |

## Recommended Local Baseline

The conservative baseline is Traefik, Keycloak, OAuth2 Proxy, Vault, mng-db,
Valkey, MinIO, Kafka, the LGTM observability stack, Ollama, and n8n. Everything
else should be explicitly optional until a local workload claims it. This is a
profile recommendation, not permission to delete definitions.

## First Removal Review Queue

1. Homer, if its dashboard is not used.
2. RabbitMQ, if no AMQP producer or consumer exists.
3. InfluxDB, if no Flux/InfluxQL workload, dashboard, or retained data exists.
4. Unused Neo4j, Qdrant, Open Notebook, ComfyUI, Supabase, PostgreSQL cluster,
   Terrakube, Syncthing, Registry, SonarQube, k6, or Locust profiles.
5. Any Redis server definition that is not required by a client or module;
   Valkey is the preferred local key/value implementation in this repository.

## Required Follow-up Before Deletion

- Confirm the service is absent from application configuration, scripts, and
  Stage 05 operations documents.
- Confirm no persistent volume, secret, route, external network, or backup is
  owned by the candidate.
- Export or retain data where required and record a recovery path.
- Remove root `include` entries, profile vocabulary, secrets, README rows, and
  operational links in one approved change.
- Render the root Compose model and run the scoped infrastructure validator.

## Sources and Date

External sources above were checked on 2026-09-18 against official project
documentation, repositories, license files, or official image documentation.
Repository evidence was read from `infra/`, the root `docker-compose.yml`,
`infra/README.md`, Stage 05 operation documents, and the local Docker container
listing observed on the same date.

## Related Documents

- [Research pack](README.md)
- [Infrastructure surface](../../../../infra/README.md)
- [Root Compose](../../../../docker-compose.yml)
- [Infrastructure validation skill](../../../../.agents/skills/infra-validate/SKILL.md)