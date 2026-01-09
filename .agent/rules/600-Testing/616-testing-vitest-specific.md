---
trigger: always_on
glob: "**/*.{test,spec}.{ts,js}"
description: "Vitest: Vite-native testing, Workers, Coverage, and Snapshots."
---
# Vitest Standards

## 1. Compatibility & Configuration

- **Jest-like**: API is compatible (`describe`, `it`, `expect`).
- **Imports**: `import { describe, it, expect } from 'vitest';` (No globals by default).
- **Config**: Use `vitest.config.ts` for project-specific settings.

### Example: Import

**Good**

```ts
import { expect, test } from 'vitest';
test('foo', () => expect(1).toBe(1));
```

**Bad**

```ts
test('foo', () => expect(1).toBe(1)); // 'test' is undefined
```

## 2. Coverage

- **Provider**: Use `c8` or `@vitest/coverage-v8`.
- **Thresholds**: Enforce thresholds in `vitest.config.ts`.

### Example: Config

**Good**

```ts
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      thresholds: { lines: 80 }
    }
  }
});
```

## 3. Features

- **In-Source Testing**: Allowed for small utils. `if (import.meta.vitest) { ... }`.
- **Threads**: Vitest uses Worker Threads. Ensure tests are isolated.
- **Snapshots**: Use `toMatchInlineSnapshot()` for simple snapshots.
