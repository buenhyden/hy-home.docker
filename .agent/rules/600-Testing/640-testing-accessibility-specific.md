---
trigger: always_on
glob: "**/*.{test,spec}.{js,ts,tsx,jsx}"
description: "Accessibility Testing: Automated audits, Axe-core, and Manual checks."
---
# Accessibility Testing Standards

## 1. Automated Audits (The Baseline)

- **Axe-core**: Integrate `jest-axe` or `cypress-axe` to catch Low-hanging fruit (missing labels, low contrast).
- **Continuous Integration**: Fail builds if accessibility violations are detected in CI.

### Example: Axe Check

**Good (Cypress)**

```javascript
it('should have no detectable a11y violations on load', () => {
  cy.visit('/');
  cy.injectAxe();
  cy.checkA11y();
});
```

**Bad**
> Relying only on manual spot checks by clicking around the app.

## 2. Keyboard & Focus

- **Tab Flow**: Verify that all interactive elements are reachable via `Tab`.
- **Focus Trap**: For modals/dialogs, focus MUST be trapped within the component.

### Example: Focus Test

**Good**

```javascript
test('modal traps focus', async () => {
  render(<Modal />);
  userEvent.tab();
  expect(document.activeElement).toBe(firstElementInModal);
});
```

## 3. Screen Reader Testing

- **Roles**: Use `getByRole` (React Testing Library) to ensure elements have correct ARIA roles.
- **Manual Verification**: Periodic testing with VoiceOver (macOS) or NVDA/JAWS (Windows).
