---
description: Incrementally migrate Next.js Pages Router to App Router
---

1. **Enable App Router**:
   - Create `app` directory alongside `pages`.
   - Both routers work simultaneously during migration.

2. **Convert getServerSideProps**:
   - Pages Router:

   ```tsx
   export async function getServerSideProps() {
     const data = await fetchData();
     return { props: { data } };
   }
   ```

   - App Router (Server Component):

   ```tsx
   async function Page() {
     const data = await fetchData();
     return <div>{data}</div>;
   }
   ```

3. **Convert getStaticProps**:
   - Use `generateStaticParams` for dynamic routes.

   ```tsx
   export async function generateStaticParams() {
     const posts = await getPosts();
     return posts.map((post) => ({ slug: post.slug }));
   }
   ```

4. **Migrate API Routes**:
   - Move from `pages/api/*` to `app/api/*/route.ts`.

   ```ts
   // app/api/users/route.ts
   export async function GET() {
     return Response.json({ users: [] });
   }
   ```

5. **Update Middleware**:
   - Middleware works the same, but update imports.

   ```ts
   import { NextResponse } from 'next/server';
   export function middleware(request) {
     return NextResponse.next();
   }
   ```

6. **Pro Tips**:
   - Migrate page by page, not all at once.
   - Use `use client` directive for client components.
   - Test thoroughly - data fetching patterns are different.
   - App Router is the future; prioritize new features there.
