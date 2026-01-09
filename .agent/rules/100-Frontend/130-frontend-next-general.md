---
trigger: always_on
glob: "**/*.{jsx,tsx,js,ts}"
description: "Next.js: App Router, Server Actions, and Optimization."
---
# Next.js General Standards

## 1. App Router Strategy

- **Server First**: Default to Server Components. Only add `'use client'` when you need:
  - Event listeners (`onClick`).
  - React Hooks (`useState`, `useEffect`).
  - Browser API access.
- **Async Components**: `await` data fetches directly in the component body.

### Example: Async Component

**Good**

```tsx
export default async function Dashboard() {
  const data = await db.query();
  return <Chart data={data} />;
}
```

**Bad**

```tsx
'use client'
export default function Dashboard() {
  const [data, setData] = useState();
  // Waterfalls, client bundle bloat
}
```

## 2. Server Actions

- **Mutations**: Use Server Actions for Form submissions to utilize Progressive Enhancement.
- **Validation**: ALWAYS validate `FormData` with Zod/Valibot on the server side.

## 3. Optimization

- **Images**: Use `<Image />` component. MUST define `width`/`height` or `fill`.
- **Fonts**: Use `next/font` to prevent Layout Shift (CLS).

### Example: Images

**Good**

```tsx
<Image src="/hero.png" width={800} height={400} alt="Hero" priority />
```

**Bad**

```tsx
<img src="/hero.png" /> // No lazy loading, layout shift
```
