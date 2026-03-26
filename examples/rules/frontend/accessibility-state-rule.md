---
layer: frontend
description: "Rule for accessibility behavior and state-management predictability in frontend flows."
---

# Frontend — Accessibility & State Rule

## Case
- **[REQ-FND-02]** Build accessibility into component behavior from the start.
- **[REQ-A11Y-01]** Ensure keyboard/screen-reader compatibility on critical interactions.
- **[REQ-FND-10]** Separate server and client state responsibilities clearly.

## Style
- **[REQ-FND-03]** Prefer predictable one-way data flow.
- **[PROC-FND-01]** Decompose over-complex components into testable units.
- **[BAN-FND-01]** Do not use non-semantic interactive primitives.
- **[BAN-FND-02]** Avoid deep prop drilling when shared state patterns are appropriate.

## Validation
- [ ] Accessibility checks pass for core interaction flows.
- [ ] State update paths are explicit and non-mutative.
- [ ] Component complexity remains within maintainable boundaries.
