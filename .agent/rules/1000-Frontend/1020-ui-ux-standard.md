---
trigger: always_on
glob: ["**/*.{css,scss,html,jsx,tsx,vue}"]
description: "UI/UX Design Standards: Enforces visual hierarchy, Jobs-to-be-Done (JTBD) alignment, and WCAG accessibility compliance."
---

# UI/UX Design Standards

- **Role**: Senior UI/UX Designer / Design Technologist
- **Purpose**: Define standards for creating user-centered, accessible, and delight-driven interfaces that align with the project's strategic goals and user research.
- **Activates When**: Designing new UI surfaces, implementing interactive flows, or auditing existing user experiences for performance and accessibility.

**Trigger**: always_on — Apply during the design and execution of all user-facing components.

## 1. Standards

### Principles

- **[REQ-UIX-01] Research-Driven Implementation (JTBD)**
  - All UI decisions MUST align with established "Jobs-to-be-Done" (JTBD) analysis and user journey maps.
- **[REQ-UIX-02] Accessibility by Default (WCAG AA)**
  - UI components MUST meet WCAG 2.1 Level AA standards for contrast, focus states, and screen reader compatibility.
- **[REQ-UIX-03] Atomic Hierarchy**
  - Interfaces MUST be constructed using the Atomic Design methodology: Atoms -> Molecules -> Organisms -> Templates -> Pages.

### Design Integrity Matrix

| Attribute | Requirement ID | Baseline |
| --- | --- | --- |
| Contrast | [REQ-UIX-04] | Minimum 4.5:1 for body text |
| Touch Target| [REQ-UIX-05] | Min 44x44px for mobile interaction |
| Whitespace | [REQ-UIX-06] | Generous 8px/16px-grid based spacing |
| Motion | [REQ-UIX-07] | Respect `prefers-reduced-motion` |

### Must

- **[REQ-UIX-08] Semantic Navigability**
  - Use appropriate HTML5 semantic tags (`<nav>`, `<main>`, `<article>`) to ensure structural clarity for assistive technologies.
- **[REQ-UIX-09] Immediate Interaction Feedback**
  - All interactive elements MUST provide immediate visual feedback for `hover`, `active`, and `focus` states.
- **[REQ-UIX-10] Predictive Layout Preservation (CLS)**
  - Reserve space for dynamic content (Images, Ads, Skeletons) to prevent Cumulative Layout Shift (CLS) during load.

### Must Not

- **[BAN-UIX-01] Cognitive Overload**
  - Do NOT present more than 3 primary actions on a single view. Utilize progressive disclosure for complex configuration tasks.
- **[BAN-UIX-02] Color-Only Meaning**
  - Critical information (Errors, Success) MUST NOT be conveyed via color alone; use icons, text labels, or patterns as secondary cues.

### Failure Handling

- **Stop Condition**: Stop feature deployment if an accessibility audit identifies a contrast ratio or focus management violation in the primary user journey.

## 2. Procedures

- **[PROC-UIX-01] Design-to-Code Audit**
  - IF implementing a new Figma-designed view THEN MUST conduct a "Design Sync" to verify token and spacing fidelity.
- **[PROC-UIX-02] Heuristic Review**
  - Conduct a monthly walk-through of the core user journey to identify and resolve usability friction points.

## 3. Examples

### Accessible Button Anatomy (Good)

```jsx
<button
  className="bg-primary text-white p-4 focus:ring-2"
  aria-label="Save current changes"
>
  Save
</button>
```

## 4. Validation Criteria

- **[VAL-UIX-01] WCAG Compliance Pass**
  - [ ] Automated accessibility scanners confirm zero "Critical" violations in the rendered HTML.
- **[VAL-UIX-02] Token Symmetry**
  - [ ] Pixel-level audit confirms that implementation matches the design system's spacing and typography scale.
- **[VAL-UIX-03] Lighthouse A11y Score**
  - [ ] Lighthouse audit achieves a score of > 95 for accessibility on all primary landing pages.
