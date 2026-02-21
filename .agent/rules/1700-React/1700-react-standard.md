---
trigger: model_decision
glob: ["**/*.tsx", "**/*.jsx"]
description: "React Standards: Enforces functional components, hooks best practices, and performance-aware state management."
---

# React Development Standards

- **Role**: Frontend React Developer
- **Purpose**: Define standards for building performant, accessible, and maintainable user interfaces using modern React patterns.
- **Activates When**: Developing React components, defining hooks, or managing component-level state.

**Trigger**: model_decision — Apply during the development of React-based UI components.

## 1. Standards

### Principles

- **[REQ-RCT-01] Functional Component Primacy**
  - All new components MUST be Functional Components. The use of Class components is PROHIBITED (Legacy maintenance only).
- **[REQ-RCT-02] Hook-Driven Logic**
  - Business and UI logic MUST be encapsulated in React Hooks (`useState`, `useEffect`, `useMemo`) or custom hooks.
- **[REQ-RCT-03] Strict Prop Typing**
  - Every component MUST have explicit type definitions for its props (using TypeScript interfaces) to ensure contract fidelity.

### Component Lifecycle

| Phase | Requirement ID | Mandatory Action |
| --- | --- | --- |
| Initialization | [REQ-RCT-04] | Lazy load heavy components |
| State Update | [REQ-RCT-05] | Prevent unnecessary re-renders |
| Teardown | [REQ-RCT-06] | Clean up effect subscriptions |
| Validation | [REQ-RCT-07] | Error Boundary at the route level |

### Must

- **[REQ-RCT-08] Hook Rules Compliance**
  - Hooks MUST only be called at the top level of a component or a custom hook. Conditional hook calls are PROHIBITED.
- **[REQ-RCT-09] Exhaustive Effect Dependencies**
  - `useEffect`, `useCallback`, and `useMemo` dependency arrays MUST contain all values from the component scope used in the closure.
- **[REQ-RCT-10] Accessible JSX**
  - All interactive elements MUST include appropriate labels or `aria-` attributes to ensure accessibility (WCAG compliance).

### Must Not

- **[BAN-RCT-01] Prop Drilling**
  - Avoid deeply nesting components where props are passed through multiple layers without being used; utilize `useContext` or a state library.
- **[BAN-RCT-02] Use of index as Key**
  - Do NOT use the array `index` as the `key` prop in mapped lists; use a persistent, unique identifier (e.g., `id`).

### Failure Handling

- **Stop Condition**: Stop feature execution if a component is found to leak memory (e.g., missing `removeEventListener` in a cleanup function).

## 2. Procedures

- **[PROC-RCT-01] Custom Hook Extraction**
  - IF a logic block is repeated across > 2 components THEN MUST extract it into a reusable custom hook.
- **[PROC-RCT-02] Performance Profiling**
  - IF a UI transition feels sluggish THEN MUST use the React DevTools Profiler to identify and resolve redundant re-renders.

## 3. Examples

### Custom Hook (Good)

```tsx
function useWindowSize() {
  const [size, setSize] = useState({ w: 0, h: 0 });
  useEffect(() => {
    const handle = () => setSize({ w: window.innerWidth, h: window.innerHeight });
    window.addEventListener('resize', handle);
    return () => window.removeEventListener('resize', handle);
  }, []);
  return size;
}
```

## 4. Validation Criteria

- **[VAL-RCT-01] Linting Pass**
  - [ ] `eslint-plugin-react-hooks` confirms 100% compliance with hook rules and dependencies.
- **[VAL-RCT-02] Accessibility Audit**
  - [ ] 100% of components pass the automated lighthouse accessibility score of > 90.
- **[VAL-RCT-03] Key Uniqueness**
  - [ ] Runtime logs confirm zero "missing key" or "non-unique key" warnings in dynamic lists.
