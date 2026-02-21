---
description: Comprehensive Cypress testing workflow (E2E, API, A11y)
---

1. **Pre-Flight Check**

    Detect TypeScript usage and identify target endpoints.

    - Check `tsconfig.json` for path aliases
    - Identify target URL (e.g., `http://localhost:3000`)

2. **Strategy Selection**

    Choose the right testing strategy for the feature.

    - **E2E**: Critical user journeys (Login -> Checkout)
    - **Integration**: UI state validation
    - **API**: Schema validation
    - **A11y**: Accessibility compliance

3. **Create Test spec**

    Create a new test file in `cypress/e2e`.

    ```bash
    touch cypress/e2e/feature-name.cy.ts
    ```

4. **Implement Test Logic**

    Write the test case using Cypress API.

    ```typescript
    describe('Feature Name', () => {
      beforeEach(() => {
        cy.visit('/page');
        cy.intercept('GET', '/api/data', { fixture: 'data.json' }).as('getData');
      });

      it('should perform expected action', () => {
        cy.getByTestId('submit-btn').click();
        cy.wait('@getData');
        cy.get('.success-message').should('be.visible');
      });

      it('should be accessible', () => {
        cy.injectAxe();
        cy.checkA11y();
      });
    });
    ```

5. **Run Tests Headless**

    Execute tests in headless mode for CI simulation.

    // turbo

    ```bash
    npx cypress run
    ```

6. **Run Tests Interactive (Optional)**

    Open Cypress Test Runner for debugging.

    // turbo

    ```bash
    npx cypress open
    ```

7. **Debugging (If Failed)**

    Analyze failure artifacts.

    - Check `cypress/screenshots`
    - Check `cypress/videos`
    - Use `cy.pause()` or `cy.debug()` in code
