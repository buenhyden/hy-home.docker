---
description: Workflow for developing a feature in Next.js (App Router)
---

# Next.js Feature Workflow

Based on `136-frontend-next15-react19.md` and `130-frontend-next-specific.md`.

1. **Architecture Design**
    - **Route Structure**: Define `app/[route]/page.tsx`.
    - **Layout**: Do I need a `layout.tsx` for shared UI/Context?
    - **Data Strategy**: Server Component fetch vs Client Component hook?
      - *Default*: Fetch in Server Component.

2. **Implementation**
    - **Server Component**:
      - Fetch data.
      - Pass data to client components as props.
    - **Client Component** (`'use client'`):
      - Implement interactivity (listeners, state).
      - Use `useActionState` for form submissions (Mutations).
    - **Server Actions**:
      - Define `actions.ts` (`'use server'`).
      - Implement mutation logic (DB calls).

3. **UI Construction**
    - Use Tailwind classes.
    - Build responsive layout.
    - Use `next/image` for media.

4. **Verification**
    - Build project (`npm run build`) to check types and strict mode errors.
    - Verify loading states and error boundaries.
