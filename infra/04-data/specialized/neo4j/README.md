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

- Application-level graph modeling (See [Technical Guide](../../../docs/07.guides/04-data/specialized/neo4j.md))
- Global backup policies (See [Operations Policy](../../../docs/08.operations/04-data/specialized/neo4j.md))
- Disaster recovery procedures (See [Recovery Runbook](../../../docs/09.runbooks/04-data/specialized/neo4j.md))

## Structure

```text
neo4j/
├── scripts/
│   └── neo4j-entrypoint-with-secrets.sh   # Secret-aware entrypoint
├── docker-compose.yml                     # Service definition
└── README.md                              # This file
```

## How to Work in This Area

1. Start by reviewing the [Technical Guide](../../../docs/07.guides/04-data/specialized/neo4j.md) for architectural context.
2. Ensure the `neo4j_password` secret is provisioned before starting the service.
3. Follow the `template-stateful-med` service extension in `docker-compose.yml` for resource consistency.
4. Verify connectivity via the Cypher Shell or Neo4j Browser.

## Tech Stack

| Category   | Technology        | Notes                     |
| ---------- | ----------------- | ------------------------- |
| Engine     | Neo4j Community   | Version 5.26.23           |
| Protocol   | Bolt / HTTP / S   | Port 7687 / 7474 / 7473   |
| Security   | Docker Secrets    | `neo4j_password`          |
| Extension  | APOC (Optional)   | Mount to `/plugins`       |

## Related References

- [05.analytical-specialized-dbs.md](../../../docs/07.guides/04-data/05.analytical-specialized-dbs.md)
- [Neo4j Technical Guide](../../../docs/07.guides/04-data/specialized/neo4j.md)
- [Neo4j Operations Policy](../../../docs/08.operations/04-data/specialized/neo4j.md)
- [Neo4j Recovery Runbook](../../../docs/09.runbooks/04-data/specialized/neo4j.md)
