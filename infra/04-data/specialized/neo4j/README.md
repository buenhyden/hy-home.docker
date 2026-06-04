# Neo4j

> Native property-graph database for connected data.

## Overview

The `neo4j` service provides a specialized graph storage layer for relationship-intensive data models. It enables efficient querying of deep hierarchies and complex network structures using the Cypher query language. This infrastructure is localized within the `04-data/specialized` tier and is optimized for the Community edition.

## Audience

이 README의 주요 독자:

- Operators (Database Administrators)
- Backend Developers (Graph modeling)
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Neo4j Community Edition container configuration (`docker-compose.yml`)
- Service-specific security (Secret-based authentication)
- Graph-specific networking (Bolt and HTTP/S protocols)
- JVM memory tuning for graph workloads

### Out of Scope

- Application-level graph modeling (See [Technical Guide](../../../../docs/05.operations/guides/04-data/specialized/neo4j.md))
- Operational controls (See [Operations Policy](../../../../docs/05.operations/policies/04-data/specialized/neo4j.md))
- Health and recovery triage (See [Recovery Runbook](../../../../docs/05.operations/runbooks/04-data/specialized/neo4j.md))

## Structure

```text
neo4j/
├── scripts/
│   └── neo4j-entrypoint-with-secrets.sh   # Secret-aware entrypoint
├── docker-compose.yml                     # Service definition
└── README.md                              # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Neo4j service leaf in `04-data`; services: `neo4j`; root include active via [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/specialized/neo4j/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `NEO4J_server_memory_heap_initial__size`, `NEO4J_server_memory_heap_max__size`, `NEO4J_server_memory_pagecache_size`, `NEO4J_server_default__listen__address`, `NEO4J_server_bolt_advertised__address`, `NEO4J_server_http_advertised__address`; profiles: `data`, `graph` |
| Compose linkage | root include active via [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/specialized/neo4j/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `neo4j-data:/data:rw`, `./scripts/neo4j-entrypoint-with-secrets.sh:/startup/neo4j-entrypoint-with-secrets.sh:ro`, `neo4j-data` |
| Ports | `${NEO4J_BOLT_PORT:-7687}`, `${NEO4J_HTTP_PORT:-7474}`, `${NEO4J_HTTPS_PORT:-7473}`, `${NEO4J_METRICS_PORT:-2004}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.neo4j.rule`, `traefik.http.routers.neo4j.entrypoints`, `traefik.http.routers.neo4j.tls`, `traefik.http.services.neo4j.loadbalancer.server.port`, `traefik.http.routers.neo4j.middlewares` |
| Secret refs | names: `neo4j_password`; mounts: `/run/secrets/neo4j_password` |
| Healthcheck | Compose healthcheck declared for `neo4j` |
| Operations | [Guide](../../../../docs/05.operations/guides/04-data/specialized/neo4j.md), [Policy](../../../../docs/05.operations/policies/04-data/specialized/neo4j.md), [Runbook](../../../../docs/05.operations/runbooks/04-data/specialized/neo4j.md) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. Start by reviewing the [Technical Guide](../../../../docs/05.operations/guides/04-data/specialized/neo4j.md) for architectural context.
2. Ensure the `neo4j_password` secret is provisioned before starting the service.
3. Follow the `template-stateful-med` service extension in `docker-compose.yml` for resource consistency.
4. Verify connectivity via container-local `cypher-shell` or the Traefik-backed Neo4j Browser route.

## Tech Stack

| Category   | Technology        | Notes                     |
| ---------- | ----------------- | ------------------------- |
| Engine     | `neo4j:5.26.26-community` | Community single service |
| Protocol   | Bolt / HTTP / S   | Exposed internally as 7687 / 7474 / 7473 |
| Security   | Docker Secrets    | `neo4j_password`          |
| Route      | Traefik HTTP      | `neo4j.${DEFAULT_URL}` to `${NEO4J_HTTP_PORT:-7474}` |

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect Neo4j.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking Neo4j documentation ready.

## Troubleshooting

- Start with `docker compose config` to confirm Neo4j volume, network, and secret references render.
- Check Neo4j logs and the linked runbook before changing graph persistence or password settings.

## Related Documents

- [Specialized Guides](../../../../docs/05.operations/guides/04-data/specialized/README.md)
- [Neo4j Technical Guide](../../../../docs/05.operations/guides/04-data/specialized/neo4j.md)
- [Neo4j Operations Policy](../../../../docs/05.operations/policies/04-data/specialized/neo4j.md)
- [Neo4j Recovery Runbook](../../../../docs/05.operations/runbooks/04-data/specialized/neo4j.md)
