# Qdrant

> High-performance vector similarity search engine.

## Overview

The `qdrant` service provides the vector database layer for AI/ML applications, enabling fast semantic search for high-dimensional embeddings. It is a critical component for Retrieval-Augmented Generation (RAG) workflows, localized within the `04-data/specialized` tier.

## Audience

이 README의 주요 독자:

- AI/ML Engineers (Vector search integration)
- Operators (Resource tuning and snapshots)
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Qdrant unprivileged container configuration (`docker-compose.yml`)
- Dual protocol networking (REST 6333, gRPC 6334)
- Snapshot storage configuration (`/qdrant/storage/snapshots`)
- Telemetry and service health monitoring

### Out of Scope

- Vector embedding generation (Handled by upstream models)
- Collection-level schema design (See [Technical Guide](../../../../docs/05.operations/guides/04-data/specialized/qdrant.md))
- Global backup policies (See [Operations Policy](../../../../docs/05.operations/guides/04-data/specialized/qdrant.md))
- Disaster recovery procedures (See [Recovery Runbook](../../../../docs/05.operations/guides/04-data/specialized/qdrant.md))

## Structure

```text
qdrant/
├── docker-compose.yml    # Service definition
└── README.md            # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Qdrant service leaf in `04-data`; services: `qdrant`; root include active via [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/specialized/qdrant/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `QDRANT__TELEMETRY_DISABLED`, `QDRANT__SERVICE__HTTP_PORT`, `QDRANT__SERVICE__GRPC_PORT`, `QDRANT__STORAGE__SNAPSHOTS_PATH`, `QDRANT__STORAGE__TEMP_PATH`; profiles: `ai`, `data`, `dev` |
| Compose linkage | root include active via [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/specialized/qdrant/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `qdrant-data:/qdrant/storage:rw`, `qdrant-data` |
| Ports | `${QDRANT_PORT:-6333}`, `${QDRANT_GRPC_PORT:-6334}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.qdrant.rule`, `traefik.http.routers.qdrant.entrypoints`, `traefik.http.routers.qdrant.tls`, `traefik.http.routers.qdrant.middlewares`, `traefik.http.services.qdrant.loadbalancer.server.port`, `traefik.tcp.routers.qdrant-grpc.rule`, plus 5 more |
| Secret refs | Not declared |
| Healthcheck | Compose healthcheck declared for `qdrant` |
| Operations | [Guide](../../../../docs/05.operations/guides/04-data/specialized/qdrant.md), [Policy](../../../../docs/05.operations/policies/04-data/specialized/qdrant.md), [Runbook](../../../../docs/05.operations/runbooks/04-data/specialized/qdrant.md) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. Review the [Technical Guide](../../../../docs/05.operations/guides/04-data/specialized/qdrant.md) for RAG integration patterns.
2. Ensure the `ai` or `data` profiles are active when deploying.
3. Snapshots are stored within the persistent volume; verify path mapping before backup operations.
4. Monitor health via the `/readyz` endpoint.

## Tech Stack

| Category   | Technology   | Notes                          |
| ---------- | ------------ | ------------------------------ |
| Engine     | Qdrant       | Version v1.17 (Unprivileged)   |
| REST API   | HTTP         | Port 6333                      |
| gRPC API   | gRPC         | Port 6334                      |
| Persistence| Local Bind   | `${DEFAULT_DATA_DIR}/qdrant`   |

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect Qdrant.
- Run `bash scripts/validation/check-repo-contracts.sh` to keep Qdrant documentation and operation links synchronized.

## Troubleshooting

- Start with `docker compose config` to confirm Qdrant volume, network, and label references render.
- Check Qdrant logs and the linked runbook before changing collection, snapshot, or persistence settings.

## Related Documents

- [05.analytical-specialized-dbs.md](../../../../docs/05.operations/guides/04-data/05.analytical-specialized-dbs.md)
- [Qdrant Technical Guide](../../../../docs/05.operations/guides/04-data/specialized/qdrant.md)
- [Qdrant Operations Policy](../../../../docs/05.operations/guides/04-data/specialized/qdrant.md)
- [Qdrant Recovery Runbook](../../../../docs/05.operations/guides/04-data/specialized/qdrant.md)
