---
trigger: always_on
glob: "**/*.{sql,db,sqlite,sqlite3}"
description: "SQLite: Schema Design, Performance, WAL Mode, and Best Practices."
---
# SQLite Standards

## 1. Schema Design

- **Types**: Use `INTEGER`, `TEXT`, `REAL`, `BLOB`. No strict types.
- **Primary Key**: Use `INTEGER PRIMARY KEY` for auto-increment rowid.
- **Timestamps**: Use `TEXT` in ISO8601 format or `INTEGER` (Unix epoch).

### Example: Schema

**Good**

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX idx_users_email ON users(email);
```

**Bad**

```sql
CREATE TABLE users (
    id VARCHAR(36),  -- VARCHAR not needed, just use TEXT
    email TEXT       -- No index, no NOT NULL
);
```

## 2. WAL Mode (Performance)

- **Enable WAL**: `PRAGMA journal_mode=WAL;` for concurrent reads.
- **Synchronous**: Use `PRAGMA synchronous=NORMAL;` for balanced safety/speed.

### Example: Pragmas

**Good**

```sql
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA foreign_keys=ON;
```

## 3. Parameterized Queries

- **Always**: Use `?` or `:name` placeholders. NEVER concatenate strings.

### Example: Parameters

**Good**

```python
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

**Bad**

```python
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")  # SQL Injection!
```

## 4. Transactions

- **Explicit**: Use `BEGIN`/`COMMIT` for batch operations.
- **Rollback**: Handle errors with `ROLLBACK`.

## 5. Backup

- **Online Backup**: Use `.backup` command or `sqlite3_backup_*` API.
