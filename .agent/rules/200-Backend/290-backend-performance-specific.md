---
trigger: always_on
glob: "**/*.{py,js,ts,java,go,rs}"
description: "Backend Performance: Database Indexing, N+1, and Connection Pooling."
---
# Backend Performance Standards

## 1. Database Optimization

- **N+1 Problem**: Number one killer of ORM performance. Use `join`, `prefetch_related` (Django), or `include` (Prisma).
- **Indexing**: Index columns used in `WHERE`, `JOIN`, and `ORDER BY`.

### Example: N+1

**Good**

```python
# Django
users = User.objects.select_related('profile').all()
for u in users:
    print(u.profile.bio) # No extra query
```

**Bad**

```python
users = User.objects.all()
for u in users:
    print(u.profile.bio) # Triggers SQL query per user
```

## 2. Connection Management

- **Pooling**: Use a connection pool (e.g., PgBouncer, HikariCP). Never create a new DB connection per request.
- **Timeouts**: Set strict timeouts on all upstream calls (DB, APIs) to prevent cascading failure (Circuit Breaker).

## 3. Async/Concurrency

- **Non-blocking**: Use Async I/O for network-bound tasks.
- **CPU-bound**: Offload heavy computation (PDF generation, Image resizing) to Worker Queues (Celery, BullMQ).

### Example: Blocking

**Good**

```javascript
await Queue.add('generate-pdf', { id: 1 });
```

**Bad**

```javascript
generatePdfSync(id); // Blocks the Event Loop, server waits
```
