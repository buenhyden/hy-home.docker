---
description: Workflow for End-to-End Testing with Playwright
---

1. **Test Planning**

    Identify critical user flows and scenarios.

    - **Scope**: "Checkout", "Login", "Profile Update"
    - **Strategy**: Happy path + Key error states

2. **Create Test Spec**

    Create test file in `tests/e2e`.

    ```bash
    touch tests/e2e/login.spec.ts
    ```

3. **Implement Test Logic**

    Write test using Playwright test runner.

    ```typescript
    import { test, expect } from '@playwright/test';

    test.describe('Login Feature', () => {
      test.beforeEach(async ({ page }) => {
        await page.goto('/login');
      });

      test('should login successfully', async ({ page }) => {
        // Arrange
        await page.getByLabel('Email').fill('user@example.com');
        await page.getByLabel('Password').fill('password');

        // Act
        await page.getByRole('button', { name: 'Sign in' }).click();

        // Assert
        await expect(page).toHaveURL('/dashboard');
        await expect(page.getByText('Welcome')).toBeVisible();
      });
    });
    ```

4. **Run Tests**

    Execute Playwright tests.

    // turbo

    ```bash
    npx playwright test
    ```

5. **Run Tests with UI (Optional)**

    Open interactive UI mode for debugging.

    // turbo

    ```bash
    npx playwright test --ui
    ```

6. **Accessibility Check**

    Verify accessibility compliance.

    ```typescript
    import { injectAxe, checkA11y } from 'axe-playwright';

    test('should be accessible', async ({ page }) => {
      await injectAxe(page);
      await checkA11y(page);
    });
    ```

7. **Analyze Results**

    Check reports and traces if failed.

    ```bash
    npx playwright show-report
    ```
