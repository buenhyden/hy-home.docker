---
trigger: always_on
glob: "**/*.{js,jsx,ts,tsx,mts,cts}"
description: "ESLint: Definitive flat config, type-aware linting, and Prettier integration."
---
# ESLint Best Practices

## 1. Core Configuration (Flat Config)

- **Mandatory**: Use `eslint.config.js` (Flat Config). Legacy `.eslintrc` is deprecated.
- **Base**: `eslint.configs.recommended` + `eslint.configs.strict`.

## 2. TypeScript Integration

- **Type-Awareness**: Enable strict type-checked rules.
- **Performance**: Use specific service configuration for performance.

### Example: eslint.config.ts

#### Good

```typescript
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import prettierConfig from 'eslint-config-prettier';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  ...tseslint.configs.stylisticTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
  prettierConfig, // Must be last
);
```

## 3. Critical Rules

- **`no-console`**: Error in production, allow specific levels if needed.
- **`eqeqeq`**: Always use `===`.
- **`no-unused-vars`**: Fail on unused variables (cruft).
- **`prefer-const`**: Immutable variables by default.

## 4. Anti-Patterns

- **`eslint-disable`**: Avoid suppression comments. Fix the root cause.
- **Mixed Configs**: Do not mix Flat Config and `.eslintrc`.
