---
description: Workflow for writing and running Vitest unit tests
---

1. **Setup**

    Ensure configuration is correct.

    - Check `vitest.config.ts`
    - Ensure `jsdom` or `happy-dom` installed

2. **Create Test File**

    Create test file co-located with source or in `__tests__`.

    ```bash
    touch src/components/Button.test.tsx
    ```

3. **Write Test**

    Implement test case with mocks if needed.

    ```typescript
    import { describe, it, expect, vi } from 'vitest';
    import { render, screen } from '@testing-library/react';
    import { Button } from './Button';

    describe('Button', () => {
      it('renders correctly', () => {
        render(<Button>Click me</Button>);
        expect(screen.getByText('Click me')).toBeInTheDocument();
      });
    });
    ```

    Mocking example:

    ```typescript
    vi.mock('@/api/user', () => ({
      fetchUser: vi.fn(),
    }));
    ```

4. **Run Tests**

    Execute tests in watch mode (default) or single run.

    // turbo

    ```bash
    npm run test
    ```

5. **Run Coverage**

    Check code coverage.

    // turbo

    ```bash
    npm run test -- --coverage
    ```

6. **Run Type Check**

    Ensure no type errors in tests.

    // turbo

    ```bash
    npx tsc --noEmit
    ```
