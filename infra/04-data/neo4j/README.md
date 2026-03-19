# Neo4j Graph Database

Neo4j is a native property-graph database using the Cypher query language, optimized for highly connected data and relationship traversals.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `neo4j` | `bitnami/neo4j` | Graph Database | 1.0 CPU / 1GB RAM |

## Networking

- **Internal DNS**: `neo4j:7687` (Bolt, within `infra_net`)
- **External Bolt**: `bolt://localhost:${NEO4J_BOLT_HOST_PORT}` (host-mapped)
- **Note**: HTTP/HTTPS Browser UI ports (`7474`/`7473`) are commented out by default for security.

## Persistence

- **Data**: `neo4j-volume` → `/bitnami/neo4j`

## Configuration

| Variable / Secret | Description |
| :--- | :--- |
| `NEO4J_USERNAME` | Admin username (default: `neo4j`) |
| `NEO4J_BOLT_HOST_PORT` | Host-mapped Bolt port |
| `neo4j_password` | Secret at `secrets/db/neo4j/neo4j_password.txt` |

## Enabling the Browser UI

To enable web-based access, uncomment the HTTP/HTTPS port mappings in `docker-compose.yml`.

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Single-node Neo4j stack definition. |
| `scripts/` | Helper scripts (if any). |
| `README.md` | Service overview and access notes. |

## Documentation References

- **Neo4j Context Guide**: [docs/guides/04-data/neo4j-context.md](../../../docs/guides/04-data/neo4j-context.md)
