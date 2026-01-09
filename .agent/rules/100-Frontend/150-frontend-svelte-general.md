---
trigger: always_on
glob: "**/*.{svelte,js,ts}"
description: "Svelte General: Svelte 5 Runes ($state), Effects, and Props."
---
# Svelte General Standards

## 1. Svelte 5 Runes (Reactivity)

- **State**: Use `$state(val)` instead of `let val`.
- **Derived**: Use `$derived(expr)` instead of `$: val = expr`.
- **Props**: Use `let { prop } = $props();` instead of `export let prop`.

### Example: Counter

**Good (Svelte 5)**

```svelte
<script>
  let count = $state(0);
  let double = $derived(count * 2);
  let { title = 'Counter' } = $props();
</script>
<h1>{title}: {count}</h1>
```

**Bad (Svelte 4 Legacy)**

```svelte
<script>
  export let title = 'Counter';
  let count = 0;
  $: double = count * 2;
</script>
```

## 2. Effects & Lifecycle

- **Side Effects**: Use `$effect` for logging or DOM manipulation.
- **Avoid Loops**: Do NOT create infinite loops by updating state inside an effect that depends on it.

## 3. Stores vs State

- **Global**: Continue using `writable()` stores for global state shared across components.
- **Local**: Use Runes (`$state`) for component-local state.
