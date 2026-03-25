# Neo4j

> Native property-graph database for connected data.

## 1. Context & Objective (SSoT)

The `neo4j` service provides a specialized graph storage layer for relationship-intensive data models. It allows for efficient querying of deep hierarchies and complex network structures using the Cypher query language.

- **Status**: Production / Graph
- **Role**: Relationship-intensive Storage
- **SSoT Documentation**: [03.specialized-dbs.md](../../../docs/07.guides/04-data/03.specialized-dbs.md)

## 2. Requirements & Constraints

- **Resources**: JVM Heap settings (128M initial/256M max) and page cache (128M) are optimized for the Community edition.
- **Security**: Admin password managed via Docker secrets.
- **Protocols**:
  - `Bolt` (7687): Binary protocol for drivers.
  - `HTTP/S` (7474/7473): Browser UI and REST API.

## 3. Setup & Installation

The service is part of the `data` profile.

```bash
docker compose up -d neo4j
```

### Persistence

- **Volume**: `neo4j-data` (`/data`)
- **Host Path**: `${DEFAULT_DATA_DIR}/neo4j/data`

## 4. Usage & Integration

### Integration Points

- **Bolt URL**: `bolt://neo4j.${DEFAULT_URL}:7687` (requires TLS)
- **Browser UI**: `https://neo4j.${DEFAULT_URL}`

### Cypher Example

```cypher
CREATE (a:Person {name: 'Alice'})-[r:KNOWS]->(b:Person {name: 'Bob'})
RETURN a, r, b;
```

## 5. Maintenance & Safety

- **Backups**: Use `neo4j-admin database dump` for offline backups or specialized online backup tools (Enterprise).
- **Health**: Monitor via `/_cluster/health` or `cypher-shell` health checks.
- **Plugins**: APOC and other plugins can be mounted to `/plugins`.

---
Copyright (c) 2026. Licensed under the MIT License.
