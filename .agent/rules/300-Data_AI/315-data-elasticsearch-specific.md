---
trigger: always_on
glob: "**/*.{json,py,js,ts}"
description: "Elasticsearch: Indexing, Mapping, and Querying Best Practices."
---
# Elasticsearch Standards

## 1. Indexing & Mapping

- **Explicit Mapping**: Never rely on dynamic mapping for production indices. Define types strictly.
- **Keywords vs Text**: Use `keyword` for exact matches/aggregations and `text` for full-text search.
- **Refresh Interval**: Use `refresh_interval` to optimize heavy ingestions.

### Example: Mapping

**Good**

```json
"mappings": {
  "properties": {
    "user_id": { "type": "keyword" },
    "bio": { "type": "text", "analyzer": "standard" },
    "created_at": { "type": "date" }
  }
}
```

**Bad**

```json
// No mapping provided (Dynamic mapping creates 'text' + 'keyword' for everything, wasting space)
```

## 2. Querying

- **Filter Context**: Use `filter` instead of `must` for non-scored constraints (better caching).
- **Pagination**: Use `search_after` for deep paging instead of `from`/`size` (prevents OOM).

### Example: Filter Context

**Good**

```json
"query": {
  "bool": {
    "must": { "match": { "title": "search term" } },
    "filter": { "term": { "status": "active" } }
  }
}
```

**Bad**

```json
"query": {
  "match": { "status": "active" } // Scoring 'active' status is useless and slow
}
```

## 3. Resilience

- **Sharding**: Avoid "over-sharding". Aim for 10GB-50GB shard sizes.
- **Backups**: Use Snapshot/Restore API.
