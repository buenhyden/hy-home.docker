---
trigger: always_on
glob: ["**/*.{css,scss,js,ts,jsx,tsx,vue,svelte}"]
description: "Frontend Styling Standards: Enforces utility-first (Tailwind), consistent design tokens, and mobile-first responsive design."
---

# Frontend Styling Standards

- **Role**: Senior Design Systems Engineer
- **Purpose**: Define standards for maintaining a consistent, performant, and scalable visual design system across all frontend surfaces.
- **Activates When**: Writing CSS/SCSS, configuring Tailwind CSS, or implementing components with UI libraries (Shadcn, MUI).

**Trigger**: always_on — Apply during the development of all visual styles.

## 1. Standards

### Principles

- **[REQ-STY-01] Utility-First Implementation**
  - Prefer standardized utility classes (e.g., Tailwind) over arbitrary CSS values. Use the `cn()` utility for safe class merging and conditionality.
- **[REQ-STY-02] Token-Based Design**
  - All visual attributes (Colors, Spacing, Typography) MUST be sourced from central design tokens or the `tailwind.config.js`. Hardcoded hex values are PROHIBITED.
- **[REQ-STY-03] Mobile-First Responsiveness**
  - base styles MUST represent the mobile view. Use `min-width` breakpoints (e.g., `md:`, `lg:`) exclusively for desktop enhancements.

### Styling Stack Baseline

| Category | Requirement ID | Authority / Tooling |
| --- | --- | --- |
| Utility CSS | [REQ-STY-04] | Tailwind CSS with `tailwind-merge` |
| Component UI | [REQ-STY-05] | Shadcn UI (Radix + Tailwind) |
| Tokens | [REQ-STY-06] | CSS Variables / Design Tokens |
| Dynamic | [REQ-STY-07] | `clsx` / `tailwind-merge` |

### Must

- **[REQ-STY-08] Explicit Z-Index Scaling**
  - Z-index values MUST utilize a predefined scale (e.g., `z-10`, `z-20`) documented in the technical map to prevent "Z-index wars".
- **[REQ-STY-09] Narrative Class Ordering**
  - Tailwind classes SHOULD follow a logical order: Layout -> Box Model -> Typography -> Visual -> Interaction.
- **[REQ-STY-10] Transient Prop Prefixing**
  - In CSS-in-JS libraries (e.g., Styled Components), MUST use the `$` prefix for internal props to prevent unwanted attribute leakage to the DOM.

### Must Not

- **[BAN-STY-01] Indiscriminate Global Styling**
  - Avoid using the `*` selector or global tag overrides except within a controlled CSS Reset or Normalize file.
- **[BAN-STY-02] Use of !important**
  - The use of `!important` is STRICTLY PROHIBITED. Resolve specificity issues through proper selector nesting or utility adjustments.

### Failure Handling

- **Stop Condition**: Stop feature deployment if a component is found to contain more than 10% arbitrary (non-tokenized) color or spacing values.

## 2. Procedures

- **[PROC-STY-01] Theme Extension Workflow**
  - IF a new design token is required THEN MUST update `tailwind.config.js` or the global CSS variable manifest before implementation.
- **[PROC-STY-02] Visual Regression Check**
  - Perform a manual visual audit on high-DPI and mobile-sized viewports for all major UI component changes.

## 3. Examples

### Clean Tailwind Component (Good)

```tsx
const Button = ({ className, ...props }) => (
  <button className={cn("px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700", className)} {...props} />
);
```

## 4. Validation Criteria

- **[VAL-STY-01] Token Alignment Audit**
  - [ ] Static analysis confirms that 100% of colors used in the project are defined in the approved design system.
- **[VAL-STY-02] Responsive Fidelity**
  - [ ] Cross-device tests confirm that layouts do not break or overflow at the defined breakpoints (320px, 768px, 1024px).
- **[VAL-STY-03] Formatting Pass**
  - [ ] `Prettier` and Tailwind-Lint confirm that class ordering and formatting meet project standards.
