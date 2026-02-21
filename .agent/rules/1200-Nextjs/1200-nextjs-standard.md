---
trigger: model_decision
glob: ["app/**/*.{ts,tsx}", "pages/**/*.{ts,tsx}"]
description: "Next.js Standards: Enforces App Router usage, React Server Components (RSC), and secure server-action patterns."
---

# Next.js Development Standards

- **Role**: Fullstack Next.js Engineer
- **Purpose**: Define standards for building high-performance, SEO-optimized applications using the Next.js App Router and Server Components architecture.
- **Activates When**: Developing Next.js applications, configuring routing, or managing server-side data fetching.

**Trigger**: model_decision — Apply during the design and implementation of Next.js based fullstack features.

## 1. Standards

### Principles

- **[REQ-NXT-01] App Router Primacy**
  - All new projects or major features MUST utilize the App Router (`app/` directory). The Pages Router is reserved for legacy maintenance only.
- **[REQ-NXT-02] Server-Component by Default**
  - All components MUST be React Server Components (RSC) by default to minimize client-side bundle size. Use `'use client'` selectively for interactivity.
- **[REQ-NXT-03] Native Data Fetching**
  - Leverage native `fetch()` with Next.js caching and revalidation options instead of external client-side fetching libraries where possible.

### Framework Stack

| Category | Requirement ID | Critical Action |
| --- | --- | --- |
| Routing | [REQ-NXT-04] | Use File-based routing in `app/` |
| Interaction | [REQ-NXT-05] | `'use client'` at the component leaf |
| Optimization | [REQ-NXT-06] | Use `next/image` and `next/font` |
| Actions | [REQ-NXT-07] | Use `'use server'` for mutations |

### Must

- **[REQ-NXT-08] Explicit Client Boundaries**
  - Components requiring browser APIs (hooks, event listeners) MUST explicitly declare the `'use client'` directive at the top of the file.
- **[REQ-NXT-09] Image Optimization**
  - All images MUST be rendered using the `next/image` component to ensure automatic resizing, lazy loading, and format conversion.
- **[REQ-NXT-10] Metadata Engagement**
  - Every page/layout SHOULD export a `metadata` object or `generateMetadata` function for SEO and social sharing integrity.

### Must Not

- **[BAN-NXT-01] Secrets in Client Bundles**
  - Sensitive API keys or environment variables MUST NOT be prefixed with `NEXT_PUBLIC_` unless they are explicitly intended for client-side exposure.
- **[BAN-NXT-02] Native <img> Tags**
  - Avoid using standard `<img>` tags for internal assets; utilize `next/image` to prevent performance regressions.

### Failure Handling

- **Stop Condition**: Stop deployment if a Server Component is found to be importing a client-only library without a proper `'use client'` boundary.

## 2. Procedures

- **[PROC-NXT-01] Cache Investigation**
  - IF a page displays stale data THEN MUST verify the `revalidate` settings in the `fetch` options or `export const revalidate` tag.
- **[PROC-NXT-02] Bundle Analysis**
  - Run `next build` and analyze the route-level bundle sizes monthly to identify oversized client-side components.

## 3. Examples

### Server Action (Good)

```typescript
async function updateData() {
  'use server';
  // ... database logic
}
```

## 4. Validation Criteria

- **[VAL-NXT-01] RSC/Client Ratio**
  - [ ] build audit confirms that the majority of static logic resides in Server Components.
- **[VAL-NXT-02] SEO Presence**
  - [ ] Every active route generates valid Meta tags for Title and Description.
- **[VAL-NXT-03] LCP Performance**
  - [ ] Lighthouse audit confirms Largest Contentful Paint (LCP) < 2.5s for core routes.
