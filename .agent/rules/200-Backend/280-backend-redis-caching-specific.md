---
trigger: always_on
glob: "**/*.{ts,js,py}"
description: "Redis Caching: Configuration, clients, and advanced patterns (Cache-Aside, Write-Through)."
---
# Redis Caching Standards

## 1. Configuration & Security

- **Persistence**: Enable RDB or AOF for data durability if needed.
- **Eviction**: Set `maxmemory` and `maxmemory-policy` (e.g., `allkeys-lru`).
- **Security**: Require a strong password (`requirepass`). Rename dangerous commands (`FLUSHDB`) in production.
- **Network**: Restrict access to trusted IPs/VPCs. Don't expose publicly.

## 2. Key Design & Structure

- **Hierarchy**: Use colons to create namespaces: `object:id:attribute` (e.g., `user:1001:settings`).
- **Readability**: Keys should be descriptive but concise.
- **No Numbered DBs**: Avoid `SELECT index`. Use namespacing (Redis Cluster doesn't support DBs).
- **Big Keys**: Avoid keys > 1MB. Break them down (e.g., Hash vs String).
- **Commands**: NEVER use `KEYS *` in production (blocks thread). Use `SCAN`.

## 3. Client Best Practices

- **Connection**: Reuse connections (pool). Do not create a new client per request.
- **Error Handling**: Handle connection timeouts and errors gracefully.
- **Serialization**: Use consistent serialization (e.g., JSON) for objects.

## 3. Caching Patterns

- **Cache-Aside (Lazy Loading)**:
  1. App requests data from cache.
  2. If miss, fetch from DB.
  3. Write to cache with TTL.
- **Write-Through**:
  - Update DB and Cache simultaneously (consistency).
- **TTL**: ALWAYS set a Time-To-Live (TTL) to prevent stale data buildup.

### Example: Cache-Aside (TypeScript)

#### Good

```typescript
async function getUser(id: string) {
  const cacheKey = `user:${id}`;
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  const user = await db.user.findUnique({ where: { id } });
  if (user) {
    // Set with TTL (1 hour)
    await redis.setex(cacheKey, 3600, JSON.stringify(user));
  }
  return user;
}
```

#### Bad

```typescript
// No TTL, unlimited growth
await redis.set(key, value);
```
