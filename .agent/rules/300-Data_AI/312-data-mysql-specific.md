---
trigger: always_on
glob: "**/*.sql"
description: "MySQL: Popular open-source relational database best practices."
---
# MySQL Standards

## 1. Engine & Configuration

- **Storage Engine**: Always use `InnoDB` for ACID compliance and row-level locking.
- **Charset**: Use `utf8mb4` with `utf8mb4_unicode_ci` for full Unicode support.

## 2. Schema Best Practices

- **Naming**: Use `snake_case` for all tables and columns.
- **Primary Keys**: Prefer `BIGINT UNSIGNED AUTO_INCREMENT` or binary UUIDs for performance.
- **Booleans**: Use `TINYINT(1)` for boolean flags.

## 3. Performance

- **Indexing**: Avoid over-indexing. Use Covering Indexes to reduce disk I/O.
- **Query Cache**: Note that Query Cache is removed in 8.0; focus on query optimization and buffer pool sizing.
- **JOINs**: Ensure joined columns have identical types and are indexed.

## 4. Operations

- **Slow Query Log**: Enable and monitor the slow query log to identify bottlenecks.
- **Backups**: Use `mysqldump` or `mysqlpump` for logical backups. Use Percona XtraBackup for physical backups.
