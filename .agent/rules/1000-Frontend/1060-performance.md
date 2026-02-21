---
trigger: always_on
glob: "**/*.{js,ts,jsx,tsx,svelte,vue}"
description: "Frontend Performance Standards: Enforces Core Web Vitals targets, asset optimization, and rendering efficiency."
---

# Frontend Performance Standards

- **Role**: Frontend Performance Engineer
- **Purpose**: Ensure web applications are fast, responsive, and visually stable through data-driven optimization.
- **Activates When**: Writing UI components, configuring build tools, or managing static assets.

**Trigger**: always_on — Apply at all times during the development and build phases.

## 1. Standards

### Principles

- **[REQ-FE_PERF-01] Vitals-First Focus**
  - Performance MUST be measured and optimized against Core Web Vitals (LCP, CLS, INP).
- **[REQ-FE_PERF-02] Main-Thread Respect**
  - Long tasks (>50ms) MUST be avoided or broken up to maintain interaction responsiveness.
- **[REQ-FE_PERF-03] Asset Minimalism**
  - Only the minimum required code and assets for the initial viewport SHOULD be loaded on first paint.

### Target Metrics

| Metric | Threshold | Priority |
| --- | --- | --- |
| LCP | < 2.5s | High |
| CLS | < 0.1 | High |
| INP | < 200ms | High |

### Must

- **[REQ-FE_PERF-04] Hero Preloading**
  - Largest Contentful Paint (LCP) elements (hero images, fonts) MUST be preloaded.
- **[REQ-FE_PERF-05] Layout Stability**
  - Images and dynamic containers MUST have reserved space (width/height) to prevent layout shifts.
- **[REQ-FE_PERF-06] Lazy Loading**
  - Below-the-fold images and non-critical modules MUST be lazily loaded.

### Must Not

- **[BAN-FE_PERF-01] Synchronous Scripts**
  - Non-critical 3rd party scripts MUST NOT be loaded synchronously.
- **[BAN-FE_PERF-02] Recursive Sorting**
  - Expensive logic (like sorting) MUST NOT occur within a component's render loop without memoization.

### Failure Handling

- **Stop Condition**: Stop deployment if Lighthouse performance score falls below the defined threshold (e.g., 90).

## 2. Procedures

- **[PROC-FE_PERF-01] Performance Audit**
  - IF modifying critical path assets THEN MUST run a local Lighthouse or bundle analysis.
- **[PROC-FE_PERF-02] Optimization Hook**
  - Use `useMemo` and `useCallback` in React for expensive calculations that trigger often.

## 3. Examples

### Preloading Hero Image

```html
<link rel="preload" href="/hero.webp" as="image" fetchpriority="high">
```

## 4. Validation Criteria

- **[VAL-FE_PERF-01] Lighthouse Compliance**
  - [ ] Page scores > 90 on Performance in the Lighthouse CI.
- **[VAL-FE_PERF-02] Shift Verification**
  - [ ] No detectable layout shifts occur during initial page hydration.
- **[VAL-FE_PERF-03] Bundle Analysis**
  - [ ] Individual chunks do not exceed 500KB (uncompressed).
