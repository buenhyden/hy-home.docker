---
description: Workflow for TDD or Unit Testing with Jest
---

1. **Test Scaffolding**

    Create test file next to the source file.

    ```bash
    # Example
    touch src/utils/calculator.test.ts
    ```

    Structure the test file:

    ```typescript
    describe('Calculator', () => {
      // Tests go here
    });
    ```

2. **Mocking Dependencies**

    Setup mocks for external dependencies.

    ```typescript
    import { sendAnalytics } from './analytics';

    jest.mock('./analytics');

    beforeEach(() => {
      jest.clearAllMocks();
    });
    ```

3. **Write Failing Test (Red)**

    Write a test case that describes expected behavior.

    ```typescript
    it('should add two numbers', () => {
      const result = add(2, 3);
      expect(result).toBe(5);
    });
    ```

4. **Run Tests (Fail)**

    Verify that the test fails as expected.

    // turbo

    ```bash
    npm test
    ```

5. **Implement Logic (Green)**

    Write minimal code to pass the test.

    ```typescript
    export function add(a: number, b: number) {
      return a + b;
    }
    ```

6. **Run Tests (Pass)**

    Verify that the test passes.

    // turbo

    ```bash
    npm test
    ```

7. **Refactor**

    Optimize code while keeping tests passing.

    - Improve naming
    - Remove duplication
    - Optimize performance

8. **Final Verification**

    Run all tests including coverage.

    // turbo

    ```bash
    npm test -- --coverage
    ```
