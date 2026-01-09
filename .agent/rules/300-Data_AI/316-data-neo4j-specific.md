---
trigger: always_on
glob: "**/*"
description: "Neo4j: Cypher Queries, Parameters, Constraints, and Performance."
---
# Neo4j Standards

## 1. Naming Conventions

- **Node Labels**: `PascalCase` (e.g., `Person`, `Product`).
- **Relationships**: `UPPER_SNAKE_CASE` (e.g., `FRIEND_OF`, `PURCHASED`).
- **Properties**: `camelCase` (e.g., `firstName`, `createdAt`).

### Example: Naming

**Good**

```cypher
MATCH (p:Person)-[r:FRIEND_OF]->(f:Person)
WHERE p.firstName = 'Alice'
RETURN f.lastName
```

**Bad**

```cypher
MATCH (p:person)-[r:friend_of]->(f:Friend)
WHERE p.first_name = 'Alice'
RETURN f.last_name
```

## 2. Parameterized Queries (Security)

- **Always Use Parameters**: NEVER concatenate strings into Cypher.
- **Injection Prevention**: Parameters prevent Cypher injection.

### Example: Parameters

**Good**

```javascript
const query = `MATCH (u:User {userId: $userId}) RETURN u.name`;
const params = { userId: userInput };
```

**Bad**

```javascript
const query = `MATCH (u:User {userId: '${userInput}'}) RETURN u.name`; // SQLi equivalent
```

## 3. Constraints & Indexes

- **Uniqueness**: Use `CREATE CONSTRAINT` for unique properties.
- **Indexes**: Create indexes on frequently filtered properties.

### Example: Constraint

**Good**

```cypher
CREATE CONSTRAINT FOR (p:Person) REQUIRE p.email IS UNIQUE;
CREATE INDEX FOR (p:Product) ON (p.sku);
```

## 4. Query Optimization

- **Start with Indexed Nodes**: Begin MATCH with labeled, indexed nodes.
- **PROFILE**: Use `PROFILE` to analyze query execution plans.
- **LIMIT Early**: Apply `LIMIT` as early as possible.
