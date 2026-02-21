---
trigger: model_decision
glob: ["**/*"]
description: "Performance Pillar: Enforces latency budgets, load testing (k6), and data-driven optimization standards across frontend and backend."
---

# Performance Pillar

- **Role**: Performance Systems Engineer
- **Purpose**: Ensure application responsiveness, scalability, and visual stability through rigorous measurement and optimization.
- **Activates When**: Developing high-scale code, configuring load tests, or optimizing frontend assets.

**Trigger**: model_decision — Apply during architectural design and performance-sensitive implementation.

## 1. Standards

### Principles

- **[REQ-PERF-01] Budget-Driven Development**
  - Every critical service path MUST have a defined latency budget (e.g., P99 < 200ms) within its SLO.
- **[REQ-PERF-02] Evidence-First Optimization**
  - Optimization MUST NOT be performed without profiling data (Flamegraphs, APM) and a clear hypothesis.
- **[REQ-PERF-03] Visual Stability (LCP/CLS)**
  - Frontend assets MUST be optimized to meet Core Web Vitals targets for Largest Contentful Paint and Layout Shift.

### Core Metrics (SLOs)

| Metric | Threshold | Scope |
| --- | --- | --- |
| P99 Latency | < 300ms | Backend API |
| LCP | < 2.5s | Frontend |
| CLS | < 0.1 | Frontend |
| INP | < 200ms | Interactive Elements |

### Must

- **[REQ-PERF-04] Mandatory Profiling**
  - Bottlenecks MUST be identified using profiling tools (e.g., pprof, Chrome DevTools) before patching.
- **[REQ-PERF-05] Load Testing Gate**
  - Critical user journeys MUST be load-tested using k6 or Gatling before production deployment.
- **[REQ-PERF-06] Lazy Asset Delivery**
  - Images MUST use modern formats (WebP/AVIF) and utilize lazy loading for below-fold content.

### Must Not

- **[BAN-PERF-01] Blind Refactoring**
  - Logic MUST NOT be refactored for "speed" without a before-and-after benchmark report.
- **[BAN-PERF-02] Main-Thread Blocking**
  - Computationally heavy tasks MUST NOT block requested UI interactions (use Workers/Background jobs).

### Failure Handling

- **Stop Condition**: Stop deployment if Lighthouse scores or P99 latencies fail to meet the project's performance budget.

## 2. Procedures

- **[PROC-PERF-01] Bottleneck Identification**
  - IF a performance regression is detected THEN MUST conduct a flamegraph analysis to locate the hot path.
- **[PROC-PERF-02] Asset Optimization Audit**
  - Every quarter, audit frontend assets for unused JS/CSS to minimize the critical rendering path.

## 3. Examples

### Benchmarking Hypothesis

```javascript
// Good: Simple benchmark to verify optimization
console.time('optimization-test');
runTargetFunction();
console.timeEnd('optimization-test');
```

## 4. Validation Criteria

- **[VAL-PERF-01] Lighthouse Compliance**
  - [ ] Production frontend score > 90 in the accessibility and performance categories.
- **[VAL-PERF-02] Latency Verification**
  - [ ] Load tests confirm that P99 latency remains within budget under 2x expected peak load.
- **[VAL-PERF-03] Resource Density**
  - [ ] JavaScript bundle size for initial paint is < 200KB (gzipped).
