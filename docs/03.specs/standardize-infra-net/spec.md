---
status: completed
---

<!-- Target: docs/03.specs/standardize-infra-net/spec.md -->

# Standardize `infra_net` Technical Specification

## Overview

This document defines detailed instructions for applying the `infra_net` network to all infrastructure services and fixing the subnet to `172.19.0.0/16`. It translates PRD requirements into concrete Docker Compose configuration values.

## Strategic Boundaries & Non-goals

- **SPEC Owns**:
  - `networks` IPAM settings in the root `docker-compose.yml`.
  - Adding `infra_net` to each service-level `networks` block.
  - Preserving existing static IP assignments for existing services.
- **SPEC Does Not Own**:
  - IPAM changes for other networks such as `project_net`.
  - Direct edits to `/etc/hosts` inside containers; Docker DNS is recommended instead.

## Related Inputs

- **PRD**: [../../01.requirements/023-standardize-infra-net.md](../../01.requirements/023-standardize-infra-net.md)
- **ARD**: [../../02.architecture/requirements/0026-standardize-infra-net.md](../../02.architecture/requirements/0026-standardize-infra-net.md)
- **Related ADRs**: [../../02.architecture/decisions/0026-standardize-infra-net.md](../../02.architecture/decisions/0026-standardize-infra-net.md)

## Contracts

- **Config Contract**:
  - `networks.infra_net.ipam.config.subnet` == `172.19.0.0/16`
  - `services.*.networks` list must contain `infra_net`.
- **Governance Contract**:
  - Every service in included files must reference the global `infra_net`.
  - Existing `k3d-hyhome` settings must never be removed when present.

## Core Design

- **Component Boundary**: Docker Compose runtime environment.
- **Key Dependencies**: Docker Compose V2.20+ with `include` support.
- **Tech Stack**: YAML, Docker Engine.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Follow the Docker Compose `networks` and `services.networks` schemas.
- **Transition Plan**:
  1. Check and adjust the IPAM settings in the root file.
  2. Update individual service files in sequence.
  3. Verify the merged result with `docker compose config`.

## Interfaces & Data Structures

### Network Definition Example (Root)

```yaml
networks:
  infra_net:
    name: infra_net
    driver: bridge
    ipam:
      config:
        - subnet: ${INFRA_SUBNET:-172.19.0.0/16}
          gateway: ${INFRA_GATEWAY:-172.19.0.1}
```

### Assigned IP Mapping Table (Authoritative)

| IP Address         | Service Name / Group      | Folder Path                                   |
| :----------------- | :------------------------ | :-------------------------------------------- |
| `172.19.0.5`       | oauth2-proxy-valkey       | `infra/02-auth/oauth2-proxy`                  |
| `172.19.0.7`       | registry                  | `infra/09-tooling/registry`                   |
| `172.19.0.11-16`   | Relational / Mng DB Core  | `infra/04-data/relational`, `operational`     |
| `172.19.0.20-28`   | Observability Stack       | `infra/06-observability`                      |
| `172.19.0.29`      | MinIO                     | `infra/04-data/lake-and-object/minio`         |
| `172.19.0.30-38`   | Kafka Stack               | `infra/05-messaging/kafka`                    |
| `172.19.0.39`      | MinIO bucket job          | `infra/04-data/lake-and-object/minio`         |
| `172.19.0.50-59`   | PostgreSQL Cluster        | `infra/04-data/relational/postgresql-cluster` |
| `172.19.0.61`      | Neo4j                     | `infra/04-data/specialized/neo4j`             |
| `172.19.0.80-85`   | n8n Workflow              | `infra/07-workflow/n8n`                       |
| `172.19.0.90-100`  | Airflow Workflow          | `infra/07-workflow/airflow`                   |
| `172.19.0.120`     | Terraform / Atlantis      | `infra/09-tooling/terraform`                  |
| `172.19.0.121`     | RedisInsight              | `infra/11-laboratory/redisinsight`            |
| `172.19.0.122-123` | SurrealDB / Open Notebook | `infra/11-laboratory/open-notebook`           |
| `172.19.0.150-151` | Cassandra                 | `infra/04-data/nosql/cassandra`               |
| `172.19.0.160-163` | CouchDB                   | `infra/04-data/nosql/couchdb`                 |
| `172.19.0.170-175` | MongoDB                   | `infra/04-data/nosql/mongodb`                 |
| `172.19.0.179-191` | Supabase Stack            | `infra/04-data/operational/supabase`          |
| `172.19.0.200`     | RabbitMQ                  | `infra/05-messaging/rabbitmq`                 |
| `172.19.0.201`     | Ollama                    | `infra/08-ai/ollama`                          |
| `172.19.0.202`     | Qdrant                    | `infra/04-data/specialized/qdrant`            |
| `172.19.0.211`     | Ollama Exporter           | `infra/08-ai/ollama`                          |
| `172.19.0.220`     | Portainer                 | `infra/11-laboratory/portainer`               |
| `172.19.0.221`     | Dozzle                    | `infra/11-laboratory/dozzle`                  |
| `172.19.0.222`     | Homer Dashboard           | `infra/11-laboratory/dashboard`               |
| `172.19.0.223`     | SonarQube                 | `infra/09-tooling/sonarqube`                  |
| `172.19.0.224`     | Syncthing                 | `infra/09-tooling/syncthing`                  |
| `172.19.0.225-227` | Terrakube API/UI/Executor | `infra/09-tooling/terrakube`                  |
| `172.19.0.250`     | Locust Master             | `infra/09-tooling/locust`                     |
| `172.19.0.251`     | Open-WebUI                | `infra/08-ai/open-webui`                      |
| `172.19.0.253`     | Locust Worker             | `infra/09-tooling/locust`                     |
| `172.19.0.228-229` | Stalwart Mail / MailHog   | `infra/10-communication/mail`                 |

### Service Assignment Example

```yaml
services:
  registry:
    networks:
      infra_net:
        ipv4_address: 172.19.0.7
```

When a service already has an additional `k3d-hyhome` network block, preserve
its existing value verbatim while adding or normalizing the `infra_net` block.

## Edge Cases & Error Handling

- **Error 1: IP Conflict**: Already-assigned static IPs must be adjusted if they fall outside the new subnet range.
- **Error 2: Multiple Default Networks**: When services without explicit network settings join `infra_net`, verify communication with any existing default network.

## Verification

```bash
# Check overall configuration integrity
docker compose config
# Check the infra_net subnet
docker compose config | grep -A 5 "infra_net:"
# Confirm k3d-hyhome preservation
docker compose config | grep "k3d-hyhome"
```

## Success Criteria & Verification Plan

- **VAL-SPC-NET-001**: `infra_net` subnet and gateway resolve to the approved IPAM contract.
- **VAL-SPC-NET-002**: service compose files preserve existing static IP assignments and join `infra_net`.
- **VAL-SPC-NET-003**: `k3d-hyhome` references remain present where they existed before the network standardization.
- **VAL-SPC-NET-004**: operations guide and runbook point to the canonical `docs/05.operations` buckets.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Plan**: [../../04.execution/plans/2026-04-01-standardize-infra-net.md](../../04.execution/plans/2026-04-01-standardize-infra-net.md)
- **Tasks**: [../../04.execution/tasks/2026-04-01-standardize-infra-net.md](../../04.execution/tasks/2026-04-01-standardize-infra-net.md)
- **Guide**: [../../05.operations/guides/12-infra-net/standardize-infra-net.md](../../05.operations/guides/12-infra-net/standardize-infra-net.md)
- **Policy**: [../../05.operations/policies/12-infra-net/standardize-infra-net.md](../../05.operations/policies/12-infra-net/standardize-infra-net.md)
- **Runbook**: [../../05.operations/runbooks/12-infra-net/standardize-infra-net.md](../../05.operations/runbooks/12-infra-net/standardize-infra-net.md)
