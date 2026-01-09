---
trigger: always_on
glob: "src/routes/**/*"
description: "SvelteKit: Routing, Server-side rendering (SSR), and Load functions."
---
# SvelteKit Specifics

## 1. Data Loading

- **Load Functions**: Use `+page.server.ts` for sensitive data (DB). Use `+page.ts` for public data.
- **Return**: Return a simple JSON object.

### Example: Load Function

**Good**

```ts
// +page.server.ts
export async function load({ fetch }) {
  const user = await db.getUser();
  return { user }; 
}
```

**Bad**

```ts
// Fetching in component
<script>
  onMount(async () => {
    data = await fetch('/api/user'); // Waterfalls
  });
</script>
```

## 2. Form Actions

- **Mutations**: ALWAYS use Form Actions (`export const actions`) over API routes for form submissions. It handles no-JS progressively.

### Example: Actions

**Good**

```html
<form method="POST" action="?/login">
```

**Bad**

```html
<button onclick={login}>Login</button> <!-- Requires JS -->
```
