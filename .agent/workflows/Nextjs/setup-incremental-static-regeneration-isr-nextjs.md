---
description: Serve static pages with auto-updates
---

1. **Enable ISR**:

   ```tsx
   export const revalidate = 60; // seconds

   export default async function Page() {
     const data = await fetchData();
     return <div>{data}</div>;
   }
   ```

2. **On-Demand Revalidation**:

   ```ts
   import { revalidatePath } from 'next/cache';

   export async function POST(request: Request) {
     const { path } = await request.json();
     revalidatePath(path);
     return Response.json({ revalidated: true });
   }
   ```

3. **Pro Tips**:
   - Use tags for bulk revalidation.
   - Perfect for blogs and e-commerce.
