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
- Collection-level schema design (See [Technical Guide](../../../docs/07.guides/04-data/specialized/qdrant.md))
- Global backup policies (See [Operations Policy](../../../docs/08.operations/04-data/specialized/qdrant.md))
- Disaster recovery procedures (See [Recovery Runbook](../../../docs/09.runbooks/04-data/specialized/qdrant.md))

## Structure

```text
qdrant/
├── docker-compose.yml    # Service definition
└── README.md            # This file
```

## How to Work in This Area

1. Review the [Technical Guide](../../../docs/07.guides/04-data/specialized/qdrant.md) for RAG integration patterns.
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

## Related References

- [05.analytical-specialized-dbs.md](../../../docs/07.guides/04-data/05.analytical-specialized-dbs.md)
- [Qdrant Technical Guide](../../../docs/07.guides/04-data/specialized/qdrant.md)
- [Qdrant Operations Policy](../../../docs/08.operations/04-data/specialized/qdrant.md)
- [Qdrant Recovery Runbook](../../../docs/09.runbooks/04-data/specialized/qdrant.md)
