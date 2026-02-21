---
trigger: always_on
glob: "**/*.{ts,tsx}"
description: "Modern React Development: Enforces functional components, server components (RSC), and URL-driven state management."
---

# Modern React Development Standards

- **Role**: Modern React Architect
- **Purpose**: Define standards for building high-performance, accessible, and scalable web applications using React Server Components and modern hooks.
- **Activates When**: Developing React components, configuring Next.js routes, or managing application-level state.

**Trigger**: always_on — Apply during the implementation of modern web application features.

## 1. Standards

### Principles

- **[REQ-REAC-01] Server-First Architecture**
  - Prioritize React Server Components (RSC) to minimize client-side bundle size. Use `'use client'` selectively for interactive leaves.
- **[REQ-REAC-02] URL-Driven State**
  - Prefer managing application state through URL search parameters (using `nuqs`) to ensure bookmarkability and shareability.
- **[REQ-REAC-03] Declarative Interaction**
  - UI logic MUST use functional components and hooks. The use of Class components is PROHIBITED.

### Modern Stack Baseline

| Category | Requirement ID | Recommended Tooling |
| --- | --- | --- |
| State Mgmt | [REQ-REAC-04] | `nuqs` (URL Params) |
| UI | [REQ-REAC-05] | CSS Grid / Flexbox / Tailwind |
| Performance | [REQ-REAC-06] | Next.js SSR / Suspense |
| Type Safety | [REQ-REAC-07] | TypeScript Interfaces |

### Must

- **[REQ-REAC-08] Atomic File Structure**
  - Files MUST be organized hierarchically: Exported component → Private subcomponents → Helpers → Static data → Types.
- **[REQ-REAC-09] Suspense-Aware Loading**
  - Client-side data fetching or heavy components MUST be wrapped in `Suspense` with explicit `fallback` UI.
- **[REQ-REAC-10] Web Vitals Optimization**
  - Implementation MUST prioritize Core Web Vitals (LCP < 2.5s, CLS < 0.1) through lazy loading and pre-defined asset dimensions.

### Must Not

- **[BAN-REAC-01] Overuse of useEffect**
  - Avoid `useEffect` for data synchronization or fetching where Server Components or URL state can suffice.
- **[BAN-REAC-02] Anonymous Function Renders**
  - Do NOT define anonymous functions inside JSX props; use `useCallback` or static helpers to prevent unnecessary re-renders.

### Failure Handling

- **Stop Condition**: Stop execution if a component causes an infinite re-render loop or a Next.js build error related to RSC/Client boundaries.

## 2. Procedures

- **[PROC-REAC-01] Client Boundary Audit**
  - IF adding `'use client'` THEN MUST justify why the component requires browser-side interaction.
- **[PROC-REAC-02] Asset Analysis**
  - Verify every quarter that third-party library imports are optimized for tree-shaking.

## 3. Examples

### URL State with nuqs (Good)

```typescript
import { useQueryState } from 'nuqs';

export function SearchFilter() {
  const [query, setQuery] = useQueryState('q');
  return <input value={query ?? ''} onChange={e => setQuery(e.target.value)} />;
}
```

## 4. Validation Criteria

- **[VAL-REAC-01] Bundle Efficiency**
  - [ ] Client-side JS bundle remains within the project's defined performance budget.
- **[VAL-REAC-02] Accessibility Pass**
  - [ ] 100% of custom components pass the automated lighthouse accessibility audit.
- **[VAL-REAC-03] SEO Integrity**
  - [ ] Every page includes a unique title and meta description relevant to its dynamic content.
