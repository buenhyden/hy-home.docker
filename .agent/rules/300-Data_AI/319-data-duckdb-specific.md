---
trigger: always_on
glob: "**/*.sql"
description: "DuckDB: Analytical SQL, Performance Tuning, and Data Loading specific rules."
---
# DuckDB Specific Rules

## 1. Project Structure & Configuration

- **Pragmas**: Explicitly set session pragmas (`threads`, `memory_limit`) at the start of scripts.
- **Extensions**: Explicitly `INSTALL` and `LOAD` extensions (e.g., `httpfs`, `spatial`).

### Example: Script Header

```sql
PRAGMA threads=4;
PRAGMA memory_limit='8GB';
INSTALL httpfs;
LOAD httpfs;
```

## 2. Performance & Data Loading

- **Data Loading**: Use `COPY ... FROM` or `read_parquet` for bulk loading. Avoid row-by-row `INSERT`.
- **CTEs**: Use Common Table Expressions (CTEs) for complex logic instead of nested subqueries.
- **Window Functions**: Use `QUALIFY` to filter window function results efficiently.

### Example: Efficient Loading

**Good**

```sql
CREATE TABLE users (id INT, name VARCHAR);
COPY users FROM 'users.csv' (HEADER true);
```

### Example: Time Series

**Good**

```sql
-- Use time_bucket for arbitrary intervals
SELECT time_bucket(INTERVAL 15 MINUTE, ev_time) AS bucket, count(*)
FROM events
GROUP BY 1;
```

## 3. Query Guidelines

- **Explicit Columns**: Avoid `SELECT *` in production/persistent queries.
- **Types**: Define explicit types in `CREATE TABLE`. Do not rely solely on inference for production schemas.
- **Testing**: Use `sqllogictest` or similar for critical transformation logic.
