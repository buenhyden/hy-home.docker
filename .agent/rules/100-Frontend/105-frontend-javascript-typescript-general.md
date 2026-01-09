---
trigger: always_on
glob: "**/*.{js,ts,jsx,tsx,mjs,cjs}"
description: "JavaScript & TypeScript Core: Typing, Modules, Async, and Linting."
---
# JavaScript & TypeScript General Standards

## 1. Type System (TypeScript)

- **Strict Mode**: `strict: true` in `tsconfig.json` is mandatory.
- **Avoid `any`**: Use `unknown` and type narrowing if type is truly unknown.
- **Inference**: Let TypeScript infer return types of simple functions.

### Example: Typing

**Good**

```typescript
function add(a: number, b: number): number {
    return a + b;
}

const user = getUserById(1); // TypeScript infers User | undefined
```

**Bad**

```typescript
function add(a: any, b: any): any { return a + b; } // All type safety lost
```

## 2. Modules

- **ES Modules**: Use `import`/`export`. Avoid CommonJS (`require`).
- **Default vs Named**: Prefer named exports for better tree-shaking and IDE auto-import.

### Example: Exports

**Good**

```typescript
// utils.ts
export function formatDate() { ... }
export function parseDate() { ... }

// consumer.ts
import { formatDate } from './utils';
```

**Bad**

```typescript
export default { formatDate, parseDate }; // Hard to tree-shake
```

## 3. Async / Await

- **Always Await Promises**: Never ignore a returned promise.
- **Error Handling**: Use `try/catch` or `.catch()` for every promise chain.

### Example: Unhandled Promise

**Good**

```javascript
await api.createUser(data);
```

**Bad**

```javascript
api.createUser(data); // Unhandled promise, errors disappear silently
```

## 4. Linting & Formatting

- **ESLint + Prettier**: Enforce via pre-commit hooks (Husky/lint-staged).
- **Rules**: No `console.log` in production code.
