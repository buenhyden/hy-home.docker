---
trigger: always_on
glob: "**/*.sql,**/*.prisma"
description: "PostgreSQL: JSONB, Indexing, and Extensions."
---
# PostgreSQL Standards

## 1. Data Types

- **JSONB**: Use `JSONB` (Binary) over `JSON` (Text).
- **Time**: Always use `TIMESTAMPTZ` (Timestamp with time zone).

### Example: Types

**Good**

```sql
created_at TIMESTAMPTZ DEFAULT NOW(),
meta JSONB
```

**Bad**

```sql
created_at TIMESTAMP, -- Ambiguous timezone
meta JSON -- Slow parsing
```

## 2. Indexing

- **GIN**: Use GIN indexes for JSONB keys or Array containment.
- **Partial**: Index only active rows for queues/flags.

### Example: Partial Index

**Good**

```sql
CREATE INDEX idx_jobs_pending ON jobs(status) WHERE status = 'PENDING';
```

**Bad**

```sql
CREATE INDEX idx_jobs_status ON jobs(status); 
-- Indexes millions of 'COMPLETED' rows unnecessarily
```

## 3. Operations

- **Vacuum**: Set `autovacuum` aggressive for high-churn tables.
- **Explain**: Use `EXPLAIN (ANALYZE, BUFFERS)` to debug IO.
