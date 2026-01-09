---
trigger: always_on
glob: "**/*.{js,ts,jsx,tsx,svelte,vue}"
description: "Frontend Performance: Rendering, Bundle Splitting, and Web Vitals."
---
# Frontend Performance Standards

## 1. Web Vitals & Rendering

- **LCP (Largest Contentful Paint)**: Preload hero images.
- **CLS (Shift)**: Reserve space for ads/images/embeds.
- **INP (Interaction)**: Break up long tasks (>50ms) using `setTimeout` or Workers.

## 2. Framework Optimization

- **React**: Use `React.memo` for components that re-render often with same props.
- **Vue**: Use `v-once` for static content.
- **Memoization**: Cache expensive calculations (`useMemo`, `computed`).

### Example: Memoization

**Good**

```tsx
const sorted = useMemo(() => items.sort(), [items]);
```

**Bad**

```tsx
const sorted = items.sort(); // Re-sorts on every render!
```

## 3. Bundle Hygiene

- **Imports**: Avoid `import * as _`. Import specific functions.
- **Splitting**: Lazy load routes and heavy 3rd party libs (Charts, Maps).
- **Analysis**: Run `webpack-bundle-analyzer` or `vite-bundle-visualizer` monthly.
- **Tree Shaking**: Ensure unused code is eliminated. Use ES Modules.
- **Minification**: Minify CSS/JS in production.
- **Compression**: Enable Gzip/Brotli on the server/CDN.

### Example: Splitting

**Good**

```tsx
const Chart = lazy(() => import('./HeavyChart'));
```

**Bad**

```tsx
import Chart from './HeavyChart'; // Loads instantly, blocks TTI
```
