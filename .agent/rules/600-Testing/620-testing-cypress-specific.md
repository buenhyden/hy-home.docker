---
trigger: always_on
glob: "**/*.cy.{js,ts}"
description: "Cypress: E2E Best Practices, Waiting, Intercepts, and Custom Commands."
---
# Cypress Standards

## 1. Waiting (No cy.wait(ms))

- **Explicit**: Wait for Aliases (`@apiCall`), not fixed time.
- **Assertions**: `should('be.visible')` retries automatically.

### Example: Wait

**Good**

```ts
cy.intercept('/api/users').as('getUsers');
cy.wait('@getUsers');
```

**Bad**

```ts
cy.wait(5000); // Flaky and slow
```

## 2. Data Attributes (Selectors)

- **Selectors**: Use `[data-testid="submit"]` over CSS classes.

### Example: Selectors

**Good**

```ts
cy.get('[data-testid="login-btn"]').click();
```

**Bad**

```ts
cy.get('.btn-primary').click(); // Brittle, breaks on style change
```

## 3. Custom Commands

- **Pattern**: Add reusable logic to `cypress/support/commands.ts`.
- **Example**: `cy.login(user, password)` wraps the login flow.

### Example: Command

**Good**

```ts
// commands.ts
Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login');
  cy.get('[data-testid="email"]').type(email);
  cy.get('[data-testid="password"]').type(password);
  cy.get('[data-testid="submit"]').click();
  cy.url().should('include', '/dashboard');
});
```

**Bad**

```ts
// Duplicating login steps in every test file
```
