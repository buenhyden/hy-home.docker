---
trigger: always_on
glob: "**/*.{ts,tsx}"
description: "tRPC: Modular Routers, Zod Validation, Middleware, and Type Safety."
---
# tRPC Standards

## 1. Modular Routers

- **Feature-Based**: Split routers by feature (`userRouter`, `postRouter`).
- **Merge**: Combine in `appRouter` for a clean API surface.

### Example: Modular

**Good**

```typescript
// routers/user.ts
export const userRouter = t.router({
  getUser: publicProcedure.query(() => { /* ... */ }),
});

// root.ts
export const appRouter = t.router({
  user: userRouter,
  post: postRouter,
});
```

**Bad**

```typescript
// All 50 procedures in a single monolithic router
```

## 2. Input Validation (Zod)

- **Always Validate**: Use Zod schemas for ALL procedure inputs.
- **No z.any()**: Never use `z.any()` or `z.unknown()`.

### Example: Zod

**Good**

```typescript
createPost: protectedProcedure
  .input(z.object({
    title: z.string().min(3),
    content: z.string().optional(),
  }))
  .mutation(async ({ ctx, input }) => { /* ... */ })
```

**Bad**

```typescript
createPost: protectedProcedure
  .input(z.any())
  .mutation(async ({ ctx, input }) => { /* ... */ })
```

## 3. Middleware for Auth

- **Reusable**: Create `protectedProcedure` and `adminProcedure`.
- **Context Extension**: Narrow ctx types in middleware.

## 4. Client-Side

- **Superjson**: Use as transformer for Date/Map serialization.
- **Invalidation**: Call `utils.router.invalidate()` after mutations.
