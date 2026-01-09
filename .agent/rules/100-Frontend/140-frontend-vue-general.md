---
trigger: always_on
glob: "**/*.{vue,js,ts}"
description: "Vue.js: Composition API, Reactivity, and Props vs Slots."
---
# Vue.js General Standards

## 1. Composition API (Script Setup)

- **Syntax**: Use `<script setup lang="ts">` for less boilerplate and better TS support.
- **Ref vs Reactive**: Prefer `ref()` for clarity (requires `.value`). Use `reactive()` only for grouped state like forms.

### Example: Script Setup

**Good**

```vue
<script setup lang="ts">
import { ref } from 'vue';
const count = ref(0);
function inc() { count.value++ }
</script>
```

**Bad**

```vue
<script>
export default {
  data() { return { count: 0 } } // Options API (Legacy)
}
</script>
```

## 2. Component Composition

- **Props**: Use `defineProps` for data.
- **Slots**: Use Slots when passing *content* or *layout* (e.g., Button Text, Modal Body).

### Example: Slots

**Good**

```vue
<template>
  <button class="btn">
    <slot /> <!-- Flexible -->
  </button>
</template>
```

**Bad**

```vue
<!-- Restrictive -->
<button :text="label" />
```

## 3. Performance

- **v-if vs v-show**: Use `v-if` for expensive trees (remove from DOM). Use `v-show` for cheap toggles (CSS toggle).
- **Key**: Always use unique `key` in `v-for`.
