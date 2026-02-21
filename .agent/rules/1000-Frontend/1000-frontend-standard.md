---
trigger: always_on
glob: ["**/*.{html,css,scss,js,ts,jsx,tsx,vue,svelte}"]
description: "Frontend General Standards: Enforces semantic HTML, accessibility (WCAG), core component principles, and unified state management."
---

# Frontend General Standards

- **Role**: Frontend Governance Architect
- **Purpose**: Define standards for building high-quality, accessible, and maintainable user interfaces across the entire frontend ecosystem.
- **Activates When**: Initializing new frontend surfaces, creating shared components, or defining core state and styling architecture.

**Trigger**: always_on — Apply as the primary authority for all frontend engineering activities.

## 1. Standards

### Principles

- **[REQ-FND-01] Semantic Primacy**
  - All web interfaces MUST utilize semantic HTML5 elements (`<main>`, `<nav>`, `<article>`) to ensure structural clarity and SEO integrity.
- **[REQ-FND-02] Accessibility as Foundation**
  - Accessibility MUST be integrated at the component design phase. Components MUST be focusable, operable via keyboard, and compatible with screen readers.
- **[REQ-FND-03] Uni-directional Data Flow**
  - Frontend architecture MUST favor one-way data flow (Data down, Events up) to maintain predictable component states.

### Frontend Governance Matrix

| Attribute | Requirement ID | Authority / Standard |
| --- | --- | --- |
| Structure | [REQ-FND-04] | Feature-First (vertical slices) |
| Styling | [REQ-FND-05] | Tailwind / Design Tokens |
| Performance | [REQ-FND-06] | Core Web Vitals (LCP < 2.5s) |
| A11y | [REQ-FND-07] | WCAG 2.1 Level AA |

### Must

- **[REQ-FND-08] Explicit Prop Validation**
  - Every component MUST have explicit prop definitions (TypeScript interfaces) describing all mandatory and optional inputs.
- **[REQ-FND-09] Modular Hook Extraction**
  - UI logic that persists beyond a single render or is used across multiple components MUST be extracted into a reusable Custom Hook.
- **[REQ-FND-10] Standardized State Partitioning**
  - Application state MUST be explicitly partitioned into "Server State" (API data) and "Client State" (UI toggles/local data).

### Must Not

- **[BAN-FND-01] Non-Semantic Action Divs**
  - Do NOT use `<div>` or `<span>` for primary interactive actions; utilize `<button>` or `<a>` to ensure native focus and accessibility.
- **[BAN-FND-02] Deep Component Prop Drilling**
  - Avoid passing props through more than 3 layers of components without usage; utilize Context API or a dedicated state library.

### Failure Handling

- **Stop Condition**: Stop feature execution if a primary navigation or action element is identified as being inaccessible to keyboard users.

## 2. Procedures

- **[PROC-FND-01] Component Complexity Check**
  - IF a single component file exceeds 200 lines THEN MUST evaluate it for decomposition into smaller, atomic feature components.
- **[PROC-FND-02] Cross-Browser Audit**
  - Regularly verify core user flows against the project's supported browser matrix (Chrome, Firefox, Safari, Edge).

## 3. Examples

### Semantic Action Pattern (Good)

```tsx
const SaveButton = ({ onSave }) => (
  <button
    className="p-2 bg-blue-500 text-white rounded"
    onClick={onSave}
    aria-label="Save current progress"
  >
    Save
  </button>
);
```

## 4. Validation Criteria

- **[VAL-FND-01] Accessibility Score**
  - [ ] Lighthouse audit confirms an accessibility score of > 90 for all production routes.
- **[VAL-FND-02] Semantic Tag Usage**
  - [ ] audit confirms that 100% of major page sections are wrapped in appropriate HTML5 landmark elements.
- **[VAL-FND-03] Hook Logic Ratio**
  - [ ] Manual review confirms that complex state logic is correctly extracted from UI-only components.
