---
layer: infra
---
# Neo4j Graph Database Context

**Overview (KR):** Neo4j 그래프 데이터베이스의 아키텍처와 관계형 데이터 모델링을 위한 컨텍스트 가이드입니다.

> **Component**: `neo4j`
> **Profile**: `standalone` (Optional)
> **Internal Ports**: `7687` (Bolt), `7474` (HTTP Browser)

## 1. System Role

Neo4j is a native graph database designed for highly connected data — social graphs, knowledge graphs, recommendation engines, and dependency analysis. It uses Cypher as its declarative query language.

- **Internal DNS**: `neo4j`
- **Bolt Port**: `${NEO4J_BOLT_HOST_PORT}` → `7687`

## 2. Architecture

The stack runs a single `neo4j` node using the Bitnami image. HTTP/HTTPS browser ports are commented out in the Compose definition for security; access is via the Bolt protocol only.

```text
[Application Driver (bolt://)] --> neo4j:7687 (Bolt)
```

## 3. Secrets & Configuration

| Variable / Secret | Description |
| :--- | :--- |
| `NEO4J_USERNAME` | Admin username (from `.env`, default `neo4j`) |
| `NEO4J_BOLT_HOST_PORT` | Host-mapped Bolt port |
| `neo4j_password` | Docker secret at `secrets/db/neo4j/neo4j_password.txt` |

## 4. Persistence

Data is stored in the named Docker volume `neo4j-volume`, mounted at `/bitnami/neo4j`.

## 5. Common Queries (Cypher)

```cypher
// List all nodes
MATCH (n) RETURN n LIMIT 25;

// Create a relationship
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[:KNOWS]->(b);

// Find shortest path
MATCH p=shortestPath((a:Person)-[*]-(b:Person))
WHERE a.name = 'Alice' AND b.name = 'Charlie'
RETURN p;
```

## 6. Enabling the Browser UI

To access the Neo4j Browser web interface, uncomment the HTTP ports in `infra/04-data/neo4j/docker-compose.yml` and restart the service:

```yaml
ports:
  - "${NEO4J_HTTP_PORT:-7474}:7474"
  - "${NEO4J_HTTPS_PORT:-7473}:7473"
```
