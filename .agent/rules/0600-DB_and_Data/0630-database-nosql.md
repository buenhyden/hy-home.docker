---
trigger: model_decision
glob: ["**/*.bson", "**/*.json"]
description: "NoSQL Standards: Guidelines for MongoDB, Redis, and Document stores."
---

# 0630-Database-NoSQL

- **Role**: Backend Engineer
- **Purpose**: Best practices for non-relational data usage.
- **Activates When**: Using MongoDB, Redis, or DynamoDB.

## 1. Standards

### 1.1 Principles

- **[REQ-NOS-GEN-01] Access Patterns**: Schema design MUST follow access patterns (Read-heavy vs Write-heavy).
- **[REQ-NOS-GEN-02] Eventual Consistency**: Application MUST handle eventual consistency.
- **[REQ-NOS-GEN-03] TTL**: Volatile data MUST have Time-To-Live (TTL).

### 1.2 Scope

- **In-Scope**: MongoDB, Redis, DynamoDB.
- **Out-of-Scope**: Relational SQL (see 0600).

### 1.3 Must / Must Not

- **[REQ-NOS-KEY-01] Key Design**: Redis keys MUST be namespaced (e.g., `app:user:123`).
- **[BAN-NOS-SCN-01] No Scans**: `KEYS` or full table scans are BANNED in production.
- **[REQ-NOS-IDX-01] Indexing**: MongoDB queries MUST use covered indexes where possible.

## 2. Procedures

### 2.1 Redis Caching Strategy

1. **Key**: `entity:id`.
2. **Value**: JSON serialized or Protobuf.
3. **TTL**: Set explicit expiration.
4. **Invalidation**: Write-through or Cache-aside pattern.

## 3. Examples

### 3.1 Redis Key Naming

```python
# GOOD
key = f"session:{user_id}"
redis.setex(key, 3600, session_data)

# BAD
key = user_id # No namespace
```

## 4. Validation Criteria

- [ ] **[VAL-NOS-KEY-01]** Redis keys are namespaced.
- [ ] **[VAL-NOS-TTL-01]** Cache entries have TTL.
- [ ] **[VAL-NOS-SCN-01]** Code does not use scan operations.

## 5. References

- Related: [0600-database-general.md](./0600-database-general.md)
