---
layer: mobile
description: "Rule for mobile UI/UX consistency, interaction quality, and platform-appropriate behavior."
---

# Mobile — UI/UX Rule

## Case
- **[REQ-MOB-01]** Maintain mobile-first usability and interaction clarity.
- **[REQ-MOB-02]** Respect platform conventions for Android/iOS behavior.
- **[REQ-RN-01]** Keep React Native UI patterns predictable and accessible.
- **[REQ-FLT-01]** Keep Flutter UI behavior consistent with design intent.

## Style
- **[PROC-MOB-01]** Validate touch/gesture flows against practical device constraints.
- **[REQ-MOB-LEAK-01]** Keep navigation/state transitions explicit to reduce UX drift.
- **[BAN-MOB-01]** Avoid desktop-first assumptions in mobile flows.

## Validation
- [ ] Core mobile journeys remain consistent across supported platforms.
- [ ] Navigation and interaction patterns are explicit and testable.
- [ ] Accessibility expectations are preserved in key flows.
