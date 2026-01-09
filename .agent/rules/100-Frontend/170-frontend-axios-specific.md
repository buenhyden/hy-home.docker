---
trigger: always_on
glob: "**/*.{ts,js,tsx,jsx}"
description: "Axios: Singleton Instances, Interceptors, and Typing."
---
# Axios Standards

## 1. Singleton Pattern

- **Instance**: Create `src/lib/axios.ts` or `apiClient`. Never use global `axios` directly.
- **Config**: Set `baseURL` and reasonable `timeout`.

### Example: Usage

**Good**

```ts
import { api } from '@/lib/api';
await api.get('/users');
```

**Bad**

```ts
import axios from 'axios';
await axios.get('https://api.myapp.com/users'); // Hardcoded URL
```

## 2. Cancellation

- **AbortController**: Always pass `signal` to requests in effects/components to avoid race conditions.

### Example: Cancellation

**Good**

```ts
useEffect(() => {
  const controller = new AbortController();
  api.get('/data', { signal: controller.signal });
  return () => controller.abort();
}, []);
```

**Bad**

```ts
useEffect(() => {
  api.get('/data'); // Might resolve after component unmount
}, []);
```
