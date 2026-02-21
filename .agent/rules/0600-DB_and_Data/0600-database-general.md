---
trigger: model_decision
glob: ["**/*.sql", "**/*.schema", "**/migrations/**"]
description: "Database General: SQL standards, Migration governance, and Normalization."
---

# 0600-Database-General

- **Role**: Backend Engineer / DBA
- **Purpose**: Ensure data integrity, performance, and maintainability of relational databases.
- **Activates When**: Designing schemas, writing SQL, or creating migrations.

## 1. Standards

### 1.1 Principles

- **[REQ-DB-GEN-01] ACID**: Transactions MUST preserve Atomicity, Consistency, Isolation, Durability.
- **[REQ-DB-GEN-02] Normalization**: Schemas MUST be 3NF by default (denormalize only for proven performance).
- **[REQ-DB-GEN-03] Indexing**: Foreign keys and query predicates MUST be indexed.

### 1.2 Scope

- **In-Scope**: PostgreSQL, MySQL, SQL standards.
- **Out-of-Scope**: NoSQL (see 0630).

### 1.3 Must / Must Not

- **[REQ-DB-NAM-01] Naming**: Tables MUST use `snake_case` (e.g., `user_profiles`).
- **[REQ-DB-MIG-01] Migrations**: All schema changes MUST be versioned migrations.
- **[BAN-DB-LOG-01] Logic**: Business logic MUST NOT reside in Stored Procedures (triggers/functions) unless critical for integrity.

## 2. Procedures

### 2.1 Schema Design

1. **Primary Key**: UUIDv4 or BIGINT.
2. **Foreign Key**: Explicit constraints with `ON UPDATE/DELETE` rules.
3. **Timestamps**: `created_at` and `updated_at` (with triggers) on all entities.

### 2.2 Migration Workflow

1. **Create**: Generate migration file (timestamped).
2. **Up**: SQL to apply change.
3. **Down**: SQL to revert change (MANDATORY).
4. **Test**: Run Up -> Down -> Up chain.

## 3. Examples

### 3.1 Standard Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

## 4. Validation Criteria

- [ ] **[VAL-DB-NAM-01]** Table names are snake_case.
- [ ] **[VAL-DB-MIG-01]** Migration includes Down script.
- [ ] **[VAL-DB-IDX-01]** Indexes exist for search fields.

## 5. References

- Related: [0630-database-nosql.md](./0630-database-nosql.md)
