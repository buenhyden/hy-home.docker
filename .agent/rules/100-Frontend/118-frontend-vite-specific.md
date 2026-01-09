---
trigger: always_on
glob: "vite.config.{js,ts},**/*.{js,jsx,ts,tsx}"
description: "Vite: Configuration, Environment Variables, and Performance optimization."
---
# Vite Standards

## 1. Configuration Best Practices

- **Plugins**: Import plugins (e.g., `react()`) explicitly.
- **Environment**: Use `import.meta.env` for environment variables.
- **Base Path**: Set `base` correctly for sub-path deployments.

### Example: Config

**Good**

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: { sourcemap: false }
});
```

**Bad**

```typescript
export default { // No type inference
  plugins: [require('vite-plugin-react')]
}
```

## 2. Environment Variables

- **Prefix**: Variables must start with `VITE_` to be exposed to the client.
- **Access**: Strictly use `import.meta.env`, never `process.env` (unless strictly Node context).

### Example: Variables

**Good**

```typescript
const apiUrl = import.meta.env.VITE_API_URL;
```

**Bad**

```typescript
const apiUrl = process.env.VITE_API_URL; // May be undefined in browser
```

## 3. Performance & Build

- **Code Splitting**: Use `splitVendorChunkPlugin()` or manual `rollupOptions.output.manualChunks` for large apps.
- **Barrel Files**: Avoid importing from `index.ts` files that re-export huge modules. Import leaves directly.

### Example: Imports

**Good**

```typescript
import { Button } from './components/Button/Button';
```

**Bad**

```typescript
import { Button } from './components'; // Might drag in Table, Modal, etc.
```

## 4. Developer Experience

- **Type Checking**: Run `tsc -b` in a separate terminal or `lint-staged`. Vite does NOT check types by default.
- **Preview**: Always run `vite preview` locally to verify the production build before pushing.
