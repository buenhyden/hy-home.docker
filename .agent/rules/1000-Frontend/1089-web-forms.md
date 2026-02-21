---
trigger: always_on
glob: "**/*.{html,jsx,tsx}"
description: "Web Forms Standards: Enforces accessible labeling, validation UX, and secure submission patterns."
---

# Web Forms Standards

- **Role**: Forms & UX Interaction Specialist
- **Purpose**: Define standards for building accessible, secure, and user-friendly web forms.
- **Activates When**: Creating or modifying input fields, form layouts, or submission logic.

**Trigger**: always_on — Apply when developing form-based interactions.

## 1. Standards

### Principles

- **[REQ-FORMS-01] Accessible Association**
  - Every input MUST be programmatically linked to a label or description.
- **[REQ-FORMS-02] Forgiving UX**
  - Form validation MUST be helpful and clear, avoiding cryptic error codes.
- **[REQ-FORMS-03] Validation Proximity**
  - Error messages MUST be displayed in close proximity to the affected input field.

### Must

- **[REQ-FORMS-04] Explicit Labels**
  - Use `<label>` with the `for` attribute (or `htmlFor` in React) for all inputs.
- **[REQ-FORMS-05] Semantic Grouping**
  - Related inputs (e.g., address fields, radio groups) MUST be grouped using `<fieldset>` and `<legend>`.
- **[REQ-FORMS-06] Auto-Complete compliance**
  - Inputs MUST use appropriate `autocomplete` attributes (e.g., `email`, `tel`, `address-line1`).

### Must Not

- **[BAN-FORMS-01] Placeholder as Label**
  - Placeholders MUST NOT be used as a substitute for labels.
- **[BAN-FORMS-02] Submit Blocking**
  - Form submission MUST NOT be blocked without providing a clear, accessible error summary.

### Failure Handling

- **Stop Condition**: Stop submission if CSRF tokens or required validation logic is missing.

## 2. Procedures

- **[PROC-FORMS-01] Validation Strategy**
  - IF a form has 3+ fields THEN MUST provide an error summary at the top of the form on failure.
- **[PROC-FORMS-02] Accessibility Check**
  - Verify that all error messages are announced to screen readers via `aria-live` or `role="alert"`.

## 3. Examples

### Accessible Fieldset

```html
<fieldset>
  <legend>Shipping Address</legend>
  <label for="city">City</label>
  <input id="city" type="text" autocomplete="address-level2">
</fieldset>
```

## 4. Validation Criteria

- **[VAL-FORMS-01] Keyboard Navigation**
  - [ ] User can traverse all form fields using the Tab key.
- **[VAL-FORMS-02] Error Clarity**
  - [ ] Errors are specific (e.g., "Enter a valid email" vs "Invalid").
- **[VAL-FORMS-03] Mobile Compatibility**
  - [ ] Input types trigger the correct numeric/email virtual keyboards.
