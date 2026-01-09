---
trigger: always_on
glob: "**/*"
description: "REST Implementation: Pagination, Filtering, and HATEOAS."
---
# REST Implementation Standards

## 1. Pagination

- **Cursor**: Preferred for infinite scroll / large data.
- **Encapsulation**: Envelope response with `data` and `meta`.

### Example: Pagination

**Good**

```json
{
  "data": [...],
  "meta": {
    "next_cursor": "eyJpZCI6MX0=",
    "has_more": true
  }
}
```

**Bad**

```json
[...] // Top level array - hard to add metadata later
```

## 2. Filtering

- **Query Params**: Use `q` for search, `status` for exact match.
- **Operators**: Support `gte`, `lte` via `price[gte]=10`.

### Example: Filter

**Good**

```text
GET /products?category=electronics&price[lte]=500
```

**Bad**

```text
GET /products/electronics/under-500 // Too specific, inflexible path
```
