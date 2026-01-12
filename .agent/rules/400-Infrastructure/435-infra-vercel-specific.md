---
trigger: always_on
glob: "**/*.{json,ts,js,yml,yaml}"
description: "Vercel: Serverless, Edge Regions, Caching, and Deployment."
---
# Vercel Standards

## 1. Project Structure

- **api/**: Place serverless functions in `api/` or `app/api/`.
- **Build Output**: Use `output: 'export'` for purely static sites.

## 2. Serverless & Edge

- **Edge Runtime**: Use `export const runtime = 'edge'` for low-latency, light logic.
- **Region**: Set `preferredRegion` close to your database.
- **Fluid Compute**: Enable for automatic scaling and cold start handling.

### Example: Edge Function

**Good**

```typescript
# app/api/hello/route.ts
export const runtime = 'edge';
export const preferredRegion = 'iad1';

export async function GET() {
    return new Response("Hello from Edge");
}
```

## 3. Performance & Caching

- **Headers**: Set `Cache-Control` (`s-maxage`) for CDN caching.
- **Images**: Use `next/image` for optimization.
- **Turborepo**: Use Turborepo for monorepo caching.

### Example: Caching

**Good**

```typescript
res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate');
```

## 4. Deployment

- **Preview**: Use auto-previews for PRs.
- **Env Vars**: Scope vars correctly (Dev/Preview/Prod) in Dashboard.
- **Immutable**: Deployments are immutable. Do not rely on local state.
