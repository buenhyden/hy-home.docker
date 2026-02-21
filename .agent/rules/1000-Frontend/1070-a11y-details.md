---
trigger: always_on
glob: "**/*.{tsx,jsx,vue,html}"
description: "Accessibility (A11y) Standards: Master authority for WCAG 2.1/2.2 compliance, keyboard navigation, and aria implementation."
---

# Accessibility Standards (WCAG 2.1/2.2)

- **Role**: Accessibility Conformance Lead
- **Purpose**: Ensure products are inclusive, usable, and aligned with WCAG 2.1/2.2 across A/AA/AAA levels.
- **Activates When**: Writing UI code, designing interactions, or configuring media assets.

**Trigger**: always_on — Apply at all times during the frontend development lifecycle.

## 1. Standards

### Principles

- **[REQ-A11Y-01] Semantic-First Design**
  - Native HTML elements MUST be preferred over ARIA roles whenever possible.
- **[REQ-A11Y-02] Input Independence**
  - All functionality MUST be usable via keyboard alone without requiring a mouse or gestural precision.
- **[REQ-A11Y-03] Visual Adaptability**
  - Content MUST be readable at 400% zoom and maintain a 4.5:1 minimum contrast ratio for text.

### Compliance Matrix

| Feature | WCAG Success Criterion | Target Level |
| --- | --- | --- |
| Visual Contrast | 1.4.3 | AA |
| Keyboard Access | 2.1.1 | A |
| Focus Visible | 2.4.7 | AA |
| Alt Text | 1.1.1 | A |

### Must

- **[REQ-A11Y-04] Explicit Labeling**
  - Every form input MUST be associated with a programmatically-linked `<label>`.
- **[REQ-A11Y-05] Focus Management**
  - Focus MUST be trapped within active modals and restored to the trigger upon closing.
- **[REQ-A11Y-06] Secretive Decimals**
  - Decorative images MUST be hidden from assistive technologies using `alt=""` or `aria-hidden="true"`.

### Must Not

- **[BAN-A11Y-01] Focus Hiding**
  - Focus indicators MUST NOT be removed unless a visible, accessible alternative is provided.
- **[BAN-A11Y-02] Color-Only Meaning**
  - Meaning or status MUST NOT be communicated through color alone (use icons or text tags).

### Failure Handling

- **Stop Condition**: Stop deployment if a critical path fails keyboard-only navigation testing.

## 2. Procedures

- **[PROC-A11Y-01] Component Audit**
  - IF creating a interactive component THEN MUST verify ARIA role/name/state using a screen reader.
- **[PROC-A11Y-02] Testing Routine**
  - Run automated checks (Axe/Lighthouse) AND manual keyboard smoke tests on every PR.

## 3. Examples

### Accessible Form Field

```jsx
<label htmlFor="email">Email Address</label>
<input id="email" type="email" aria-describedby="email-error" aria-invalid={hasError} />
{hasError && <div id="email-error" role="alert">Invalid email</div>}
```

## 4. Validation Criteria

- **[VAL-A11Y-01] Keyboard Tab-ability**
  - [ ] All interactive elements are reachable and operable via the Tab/Enter/Space keys.
- **[VAL-A11Y-02] Screen Reader Logic**
  - [ ] Dynamic updates are announced via `aria-live` regions where appropriate.
- **[VAL-A11Y-03] Heading Hierarchy**
  - [ ] Page structure follows a logical H1-H6 nesting without skipping levels.
