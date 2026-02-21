---
trigger: always_on
glob: "**/*.{kt,swift,tsx}"
description: "Mobile Performance Optimization: Enforces 60fps targets, battery efficiency, and memory management best practices."
---

# Mobile Performance Optimization Standards

- **Role**: Mobile Performance Engineer
- **Purpose**: Define standards for ensuring mobile applications are responsive, efficient, and respectful of device resources.
- **Activates When**: Optimizing rendering cycles, managing large data sets, or configuring background synchronization.

**Trigger**: always_on — Apply during the performance-sensitive phases of mobile development.

## 1. Standards

### Principles

- **[REQ-MOBP-01] 60fps Rendering Target**
  - Every UI transition and animation MUST target a consistent 60fps (16ms budget) to prevent visual jank.
- **[REQ-MOBP-02] Resource Stewardship**
  - Applications MUST optimize for battery life and data usage by batching requests and limiting background wake-locks.
- **[REQ-MOBP-03] Startup Latency Cap**
  - Cold startup time MUST remain below 1.5 seconds on mid-range hardware through lazy loading and pre-warmed caches.

### Performance Benchmarks

| Category | Requirement ID | Target Threshold |
| --- | --- | --- |
| App Launch | [REQ-MOBP-04] | < 1.0s (Interactive) |
| Frame Time | [REQ-MOBP-05] | < 16.6ms per frame |
| Memory usage | [REQ-MOBP-06] | Zero growth (Baseline) |
| Data | [REQ-MOBP-07] | Gzip/Brotli compressed |

### Must

- **[REQ-MOBP-08] View Flattening**
  - UI hierarchies MUST be kept shallow to minimize the cost of the measurement and layout passes.
- **[REQ-MOBP-09] Off-Thread Computation**
  - All heavy processing (JSON parsing, crypto, image filtering) MUST occur on background threads/Isolates.
- **[REQ-MOBP-10] Aggressive Caching**
  - Frequently accessed assets and API responses MUST be cached locally using persistent storage (Room/Core Data).

### Must Not

- **[BAN-MOBP-01] Inline Image Resizing**
  - Do NOT resize large images on-the-fly in the UI thread; use pre-scaled thumbnails.
- **[BAN-MOBP-02] Memory Leaks (Retain Cycles)**
  - Applications MUST NOT accumulate memory over time; use weak references for long-lived lambdas/delegates.

### Failure Handling

- **Stop Condition**: Stop execution if the frame rate drops below 30fps during a core user journey (e.g., checkout).

## 2. Procedures

- **[PROC-MOBP-01] Profiling Drill**
  - IF a jank is detected THEN MUST conduct a trace using Android Profiler or Xcode Instruments to locate the bottleneck.
- **[PROC-MOBP-02] Asset Audit**
  - Every quarter, verify that all static assets utilize modern, compressed formats (WebP, VectorDrawables).

## 3. Examples

### Efficient List Recycling

```kotlin
// Good: Using LazyColumn (Compose) or RecyclerView
LazyColumn {
    items(itemsList) { item ->
        ItemRow(item)
    }
}
```

## 4. Validation Criteria

- **[VAL-MOBP-01] Frame-Rate Verification**
  - [ ] Automated profiling confirms 60fps during 100-item scroll test.
- **[VAL-MOBP-02] Memory Stability**
  - [ ] Heap analysis confirms zero increase in baseline memory after 5 cycles of screen navigation.
- **[VAL-MOBP-03] Network Payload Size**
  - [ ] API audit confirms that all payloads are compressed and contain only necessary fields.
