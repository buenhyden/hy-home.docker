---
trigger: always_on
glob: "**/stores/*.{js,ts}"
description: "Vue Pinia: Modular state management and store patterns."
---
# Vue Pinia Specifics

## 1. Store Definition

- **Syntax**: Use "Setup Store" (Function) syntax. It aligns with Composition API.
- **Naming**: `use[Id]Store`.

### Example: Setup Store

**Good**

```ts
export const useUserStore = defineStore('user', () => {
  const user = ref(null);
  const isLoggedIn = computed(() => !!user.value);
  function login() { ... }
  
  return { user, isLoggedIn, login };
});
```

**Bad**

```ts
// Option Store (Legacy)
export const useUserStore = defineStore('user', {
  state: () => ({ user: null }),
  getters: { ... },
  actions: { ... }
});
```

## 2. Usage in Components

- **Destructuring**: MUST use `storeToRefs` for state/getters. Actions can be destructured directly.

### Example: Destructuring

**Good**

```ts
const store = useUserStore();
const { user } = storeToRefs(store); // Reactive
const { login } = store; // Actions are functions, no ref needed
```

**Bad**

```ts
const { user } = useUserStore(); // user is now a plain value, lost connection
```
