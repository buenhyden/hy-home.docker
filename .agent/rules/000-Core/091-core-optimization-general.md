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

### Example: Parallel I/O

**Good**

```javascript
const [user, posts] = await Promise.all([
  api.getUser(id),
  api.getPosts(id)
]);
```

**Bad**

```javascript
const user = await api.getUser(id);
const posts = await api.getPosts(id); // Waits unnecessarily
```

## 4. Caching Strategy

- **TTL**: Cache MUST have an expiration.
- **Layers**: Local Cache (Fastest/Small) -> Distributed (Redis) -> DB (Slowest).

## 5. Lazy Loading (Resource Economy)

- **Deferral**: Don't load heavy modules/components until needed.
- **Pagination**: Never return "all items". Always paginate API lists.

### Example: Import

**Good**

```javascript
// Dynamic import on button click
const heavyModule = await import('./heavy-chart');
```

**Bad**

```javascript
import HeavyChart from './heavy-chart'; // Loads on page load
```
