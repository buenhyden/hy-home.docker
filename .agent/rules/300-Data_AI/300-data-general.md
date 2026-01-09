---
trigger: always_on
glob: "**/*"
description: "Data Core: Modeling, SQL, Migrations, and Transaction Safety."
---
# Data General Standards

## 1. Schema Design

- **Immutability**: Prefer appending new records (Event Sourcing/Audit Logs) over updating existing ones for critical financial/audit data.
- **Naming**: Use singular names for tables (`user` not `users`).
- **Soft Deletes**: Use `deleted_at` timestamps instead of hard deletes for user-generated content.

## 2. Transaction Safety

- **ACID**: Ensure business logic that updates multiple tables is wrapped in a single transaction.
- **Locking**: Avoid long-running transactions to prevent row/table locking issues (deadlocks).

### Example: Transaction

**Good**

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
INSERT INTO transaction_log ...;
COMMIT;
```

**Bad**

```sql
-- Executing queries separately without BEGIN/COMMIT. 
-- If the second fails, the first is still committed.
```

## 3. Migrations

- **Version Control**: All schema changes MUST be in migration files (Flyway, Liquibase, Alembic).
- **Zero Downtime**: Avoid `DROP COLUMN` or `RENAME COLUMN` without a transitional period (deployment compatibility).
- **Data vs Schema**: Separate schema migrations from large data migrations (seeding/backfilling).

## 4. Performance

- **Indices**: Index columns used in `WHERE`, `JOIN`, and `ORDER BY`.
- **N+1 Avoidance**: Use `JOIN` or `IN` queries instead of loop-based queries in application code.
- **EXPLAIN**: Always analyze slow queries using `EXPLAIN ANALYZE`.
