---
trigger: always_on
glob: "**/*.ts,**/*.tsx"
description: "TypeScript Expert: Advanced types, Zod validation, and branded types."
---
# TypeScript Expert Standards

## 1. Advanced Type Safety

- **Strict Mode**: `strict: true` is non-negotiable.
- **Branded Types**: Use branded types (tagged unions) for IDs to prevent mixing distinct ID types (e.g., `UserId` vs `OrderId`).
- **Discriminated Unions**: Use a literal `type` or `kind` field for state management (e.g., `{ status: 'loading' } | { status: 'success', data: T }`).

## 2. Runtime Validation

- **Zod/io-ts**: Use Zod for runtime schema validation at API boundaries (Type + Runtime check in one).
- **Type Guards**: Implement manual `isType` predicates ONLY when necessary and test them thoroughly.

## 3. Generics & Utilities

- **Constraints**: Always constrain generics (`<T extends object>`) to avoid `unknown` behavior.
- **Utility Types**: Master `Pick`, `Omit`, `Partial`, `Readonly`, and `ReturnType`.

### Example: Branded Types & Validation

#### Good

```typescript
import { z } from 'zod';

// Branded Type Utility
type Brand<K, T> = K & { __brand: T };
type UserId = Brand<string, 'UserId'>;

// Zod Schema ensuring runtime safety
const UserSchema = z.object({
  id: z.string().uuid().transform(id => id as UserId),
  email: z.string().email(),
});

type User = z.infer<typeof UserSchema>;

function getUser(id: UserId) { 
  // ... 
}

// Compiler error if you pass a raw string or OrderId!
// getUser("123"); 
```
