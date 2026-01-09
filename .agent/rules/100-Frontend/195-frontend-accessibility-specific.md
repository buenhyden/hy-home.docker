---
trigger: always_on
glob: "**/*.{tsx,jsx,vue,html}"
description: "Accessibility (A11y): ARIA, Focus Management, and Screen Readers."
---
# Accessibility Standards

## 1. Interaction & Focus

- **Outline**: NEVER remove `:focus` outline without replacing it.
- **Trap**: Modals MUST trap focus inside them until closed.
- **Skip Links**: Add "Skip to Content" for keyboard users.

## 2. ARIA Usage (Last Resort)

- **Rule**: If a semantic HTML tag exists (`<button>`, `<nav>`), use it. Do NOT use `role="button"`.
- **Labels**: `aria-label` is required if no visible text exists (e.g., Icon Buttons).

### Example: Icon Button

**Good**

```jsx
<button aria-label="Close Menu" onClick={close}>
  <Icon name="x" />
</button>
```

**Bad**

```jsx
<button onClick={close}>
  <Icon name="x" /> <!-- Screen reader says nothing -->
</button>
```

## 3. Color & Contrast

- **Ratio**: Ensure 4.5:1 contrast ratio for text.
- **Reliance**: Don't use color alone to convey meaning (e.g., Error state needs text/icon, not just red border).
