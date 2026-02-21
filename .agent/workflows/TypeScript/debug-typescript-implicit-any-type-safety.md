---
description: Find and eliminate implicit 'any' types for better type safety
---

1. **Enable Strict Mode**:
   - Update `tsconfig.json` to catch implicit any.

   ```json
   {
     "compilerOptions": {
       "strict": true,
       "noImplicitAny": true,
       "strictNullChecks": true
     }
   }
   ```

2. **Find All 'any' Usages**:
   - Use ESLint rule.

   ```json
   // .eslintrc.json
   {
     "rules": {
       "@typescript-eslint/no-explicit-any": "error"
     }
   }
   ```

3. **Common Fixes**:
   - **Event Handlers**:

     ```tsx
     // ❌ Bad
     const handleClick = (e: any) => {};
     // ✅ Good
     const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {};
     ```

   - **API Responses**:

     ```tsx
     // ❌ Bad
     const data: any = await fetch('/api/user').then(r => r.json());
     // ✅ Good
     interface User { id: string; name: string; }
     const data: User = await fetch('/api/user').then(r => r.json());
     ```

   - **Third-Party Libraries**:

     ```tsx
     // ❌ Bad
     import someLib from 'some-lib'; // Module has no types
     // ✅ Good
     npm install --save-dev @types/some-lib
     ```

4. **Use 'unknown' Instead of 'any'**:
   - Forces type checking before use.

   ```tsx
   function handleData(data: unknown) {
     if (typeof data === 'string') {
       console.log(data.toUpperCase()); // ✅ Type-safe
     }
   }
   ```

5. **Generate Types for External APIs**:
   - See "Generate TypeScript Types from API" workflow.

6. **Pro Tips**:
   - Enable `noUncheckedIndexedAccess` to catch array/object access bugs.
   - Use type assertions sparingly: `as Type`.
   - Prefer type inference over explicit types when obvious.
