---
trigger: always_on
glob: "**/*.{tsx,jsx,vue,svelte,html}"
description: "Frontend Structure: Feature-First Architecture and Shared Components."
---
# Frontend Project Structure Standards

## 1. Feature-First Architecture

- **Vertical Slices**: Group files by *business feature*, not technology.
- **Encapsulation**: Features should not import deeply from other features. Use a public API/Index.

### Example: Feature Hierarchy

**Good**

```text
src/features/
  ├── auth/
  │   ├── components/ (LoginForm, SignupForm)
  │   ├── hooks/      (useAuth)
  │   ├── api/        (authClient)
  │   └── index.ts    (Public Exports)
  └── dashboard/
```

**Bad**

```text
src/
  ├── components/
  │   └── LoginForm.tsx
  ├── hooks/
  │   └── useAuth.tsx
  └── api/
      └── auth.ts
```

## 2. Shared/Core Directory

- **`src/components/ui`**: Dumb, reusable UI primitives (Button, Card, Modal).
- **`src/hooks`**: Global hooks (`useTheme`, `useWindowSize`).
- **`src/utils`**: Pure utility functions (`date-formatter.ts`).

## 3. Assets & Static Files

- **Public**: `favicon.ico`, `robots.txt` go in basic public folder.
- **Images**: If tied to a component, colocate it. `src/features/auth/assets/logo.svg`.
