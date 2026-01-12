---
trigger: always_on
glob: "*"
description: "Core Optimization: Big O, I/O Bottlenecks, Caching, and Lazy Loading."
---
# Core Optimization Standards

## 1. Golden Rules

- **Measure First**: Never optimize without profiling. (e.g., `cProfile`, `Chrome DevTools`).
- **Pareto Principle**: 80% of slowness is in 20% of the code (usually Loops or I/O).

## 2. Algorithmic Complexity (Big O)

- **Hot Paths**: In loops/frequent calls, strictly avoid O(N²) or O(N!).
- **Data Structures**: Use Sets/Maps for O(1) checks.

### Example: Lookup Efficiency

**Good**

```python
# O(1) Check
valid_ids = {"a", "b", "c"} 
if user_id in valid_ids: ...
```

**Bad**

```python
# O(N) Check
valid_ids = ["a", "b", "c"]
if user_id in valid_ids: ...
```

## 3. I/O is the Bottleneck

- **Batching**: 1 Query for 100 items is better than 100 Queries (N+1 Problem).
- **Parallelism**: Use `Promise.all` or `asyncio.gather` for independent I/O tasks.

## 4. Caching Strategy

- **TTL**: Cache MUST have an expiration.
- **Layers**: Local Cache (Fastest/Small) -> Distributed (Redis) -> DB (Slowest).

## 5. Lazy Loading (Resource Economy)

- **Deferral**: Don't load heavy modules/components until needed.
- **Pagination**: Never return "all items". Always paginate API lists.

## See Also

- [000-core-general.md](./000-core-general.md) - Core principles including DRY
- [050-core-debugging-specific.md](./050-core-debugging-specific.md) - Profiling and debugging tools
