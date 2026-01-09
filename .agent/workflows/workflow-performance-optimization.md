---
description: Standard workflow for performance optimization
---

# Performance Optimization Workflow

Based on `091-core-optimization-general.md` and `290-backend-performance-specific.md`.

1. **Measure First**
   - Profile the code (cProfile, Chrome DevTools).
   - Identify the bottleneck (CPU, I/O, DB).

2. **Hypothesis**
   - Formulate a hypothesis (e.g., "N+1 query in user loop").

3. **Optimization**
   - **DB**: Add indexes, use `select_related`/`include`.
   - **Algo**: Reduce complexity (O(N^2) -> O(N)).
   - **I/O**: Batch requests or use Parallelism.

4. **Verify**
   - Re-run profiler.
   - Ensure functionality is unchanged (Tests pass).
