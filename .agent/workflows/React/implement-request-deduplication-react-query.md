---
description: Prevent duplicate API calls in React components
---

1. **Next.js 15 Fetch Caching**:
   - **Change:** `fetch` requests are no longer cached by default in `GET` handlers or Server Components unless configured.
   - **Fix:** Explicitly set `cache: 'force-cache'` if you want caching.

   ```ts
   fetch('https://...', { cache: 'force-cache' }); // Cached forever
   fetch('https://...', { next: { revalidate: 3600 } }); // Cached for 1 hour
   ```

2. **React Query (Client-Side)**:
   - Best for client-side deduplication and state management.
   // turbo
   - Run `npm install @tanstack/react-query`

   ```tsx
   const { data } = useQuery({
     queryKey: ['user', id],
     queryFn: () => fetch(`/api/user/${id}`).then(r => r.json()),
     staleTime: 60 * 1000, // Deduplicates requests for 1 minute
   });
   ```

3. **Request Memoization (Server-Side)**:
   - React `cache` function deduplicates requests *within a single render pass*.

   ```tsx
   import { cache } from 'react';

   export const getUser = cache(async (id) => {
     return db.user.findUnique({ where: { id } });
   });
   // Calling getUser(1) multiple times in one request only hits DB once.
   ```

4. **Pro Tips**:
   - Use `react.cache` for DB calls in Server Components.
   - Use React Query for Client Components.
   - Next.js `fetch` deduplication happens automatically for the same URL+options.
