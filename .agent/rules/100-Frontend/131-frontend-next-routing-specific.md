---
trigger: always_on
glob: "**/app/**/*.{ts,tsx}"
description: "Next.js App Router: Layouts, Loading, and Error boundaries."
---
# Next.js App Router Patterns

## 1. Route Colocation

- **Private Folders**: Use `_components` to hide folders from routing.
- **Route Groups**: Use `(marketing)` to organize routes without affecting URL.

### Example: Structure

**Good**

```text
app/
  (auth)/
    login/
      page.tsx
    layout.tsx
  _components/
    AuthButton.tsx
```

**Bad**

```text
app/
  components/  # Mixing Routes and Components loosely
    login-form.tsx
  login/
    page.tsx
```

## 2. Data & Layouts

- **Parallel Routes**: Use `@modal` for complex layouts (sidebars, modals).
- **Interception**: Use `(.)photo` to intercept routes for lightboxes.

### Example: Layout Data

**Good**

```tsx
// app/dashboard/layout.tsx
export default function Layout({ children }) {
  return <section><Nav />{children}</section>;
}
```

**Bad**

```tsx
// Fetching data in Layout that blocks the whole page tree unnecessarily
// Use Suspense in Page instead
```
