---
trigger: always_on
glob: "**/*"
description: "Redis: In-memory data structure store for caching and messaging."
---
# Redis Standards

## 1. Key Management

- **Namespacing**: Use colons to separate levels (e.g., `app:user:123:profile`).
- **Length**: Keep keys short but descriptive to save memory.
- **Naming**: Use `snake_case` or `kebab-case` consistently.

## 2. Data Types

- **Strings**: For simple caching and session data.
- **Hashes**: For objects with multiple fields. More memory-efficient than multiple strings.
- **Sets/Sorted Sets**: For unique items, leaderboards, and relationship modeling.
- **Streams**: For high-volume message bus patterns.

## 3. Caching Strategies

- **TTL**: ALWAYS set an expiration time for cache keys to prevent memory exhaustion.
- **Eviction**: Configure an appropriate `maxmemory-policy` (e.g., `allkeys-lru`).

## 4. Performance

- **Pipelining**: Use pipelining to batch multiple commands and reduce round-trip time.
- **Lua Scripts**: Use for atomic multi-key operations.

## 5. Reliability

- **Persistence**: Use RDB for periodic snapshots or AOF for maximum durability.
- **Cluster**: Use Redis Cluster or Sentinel for high availability.
