---
trigger: model_decision
glob: ["**/*.js", "**/*.ts"]
description: "Web Components Standards: Enforces Shadow DOM encapsulation, lifecycle integrity, and declarative templates with Lit/Vanilla."
---

# Web Components Standard

- **Role**: Custom Elements Specialist
- **Purpose**: Define standards for building reusable, encapsulated UI components using the native Web Components specification (Custom Elements, Shadow DOM, Templates).
- **Activates When**: Developing Custom Elements, configuring Shadow DOM isolation, or using declarative libraries like Lit.

**Trigger**: model_decision — Apply during the implementation of native Web Components.

## 1. Standards

### Principles

- **[REQ-WC-01] Total Encapsulation**
  - Components MUST utilize the Shadow DOM (`attachShadow`) to ensure style and DOM isolation, preventing global CSS leakage.
- **[REQ-WC-02] Declarative Template Identity**
  - Leverage `<template>` elements and clonable HTML content for efficient, reusable component markup.
- **[REQ-WC-03] Standardized Lifecycle Integrity**
  - Components MUST correctly implement lifecycle callbacks (`connectedCallback`, `disconnectedCallback`) for cleanup and initialization.

### Component Baseline

| Feature | Requirement ID | Critical Action |
| --- | --- | --- |
| Registration | [REQ-WC-04] | `customElements.define` with kebab-case |
| Isolation | [REQ-WC-05] | `mode: 'open'` for Shadow DOM access |
| Events | [REQ-WC-06] | `composed: true` for event bubbling |
| Props | [REQ-WC-07] | Reflect properties to attributes |

### Must

- **[REQ-WC-08] Kebab-Case Naming**
  - All custom elements MUST be named using kebab-case with at least one hyphen (e.g., `user-profile`) as per the specification.
- **[REQ-WC-09] Explicit Cleanup**
  - Any event listeners or external subscriptions created in `connectedCallback` MUST be removed in `disconnectedCallback`.
- **[REQ-WC-10] Themeable Styling (CSS Parts)**
  - Expose internal elements via `part` attributes to allow external theming without breaking encapsulation.

### Must Not

- **[BAN-WC-01] Global Style Pollution**
  - Do NOT use `<style>` in the light DOM for component-specific logic; keep styles scoped within the Shadow Root.
- **[BAN-WC-02] Manual DOM Manipulation (Sync)**
  - Avoid brute-force innerHTML updates for dynamic content; utilize efficient patching or declarative libraries (e.g., lit-html).

### Failure Handling

- **Stop Condition**: Stop component registration if a naming collision is detected or if `attributeChangedCallback` is used without `observedAttributes`.

## 2. Procedures

- **[PROC-WC-01] A11y Verification**
  - IF a custom element represents an interactive control THEN MUST implement appropriate ARIA roles and keyboard navigation.
- **[PROC-WC-02] Build-Once Audit**
  - Verify that the component's JavaScript bundle remains under the project's atomic component size budget (< 10KB gzipped).

## 3. Examples

### Clean Custom Element (Good)

```javascript
class MyComponent extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: 'open' }).innerHTML = `
      <style>:host { display: block; }</style>
      <slot></slot>
    `;
  }
}
customElements.define('my-component', MyComponent);
```

## 4. Validation Criteria

- **[VAL-WC-01] Encapsulation Pass**
  - [ ] audit confirms that global CSS selectors cannot unintentionally target elements inside the component's Shadow DOM.
- **[VAL-WC-02] Lifecycle Integrity**
  - [ ] Memory analysis confirms zero listener leaks after multiple mount/unmount cycles.
- **[VAL-WC-03] Spec Compliance**
  - [ ] Component functions correctly in environments using strict Shadow DOM boundaries.
