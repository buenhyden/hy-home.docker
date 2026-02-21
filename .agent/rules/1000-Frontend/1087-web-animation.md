---
trigger: always_on
glob: "**/*.{css,js,tsx}"
description: "Web Animation & Motion Design Standards: Enforces performance-optimized animations and motion reduction accessibility."
---

# Web Animation Standards

- **Role**: Motion Design Engineer
- **Purpose**: Define standards for performant, accessible, and purposeful web animations.
- **Activates When**: Creating CSS animations, JS-based transitions, or motion-heavy UI interactions.

**Trigger**: always_on — Apply during the design and implementation of web animations.

## 1. Standards

### Principles

- **[REQ-ANIM-01] Purposeful Motion**
  - Animations MUST serve a functional purpose (e.g., feedback, state changes) rather than decorative excess.
- **[REQ-ANIM-02] Interaction Responsiveness**
  - Animations SHOULD NOT block user interactions or increase perceived latency.
- **[REQ-ANIM-03] Motion Economy**
  - Use GPU-accelerated properties (`transform`, `opacity`) to maintain 60fps and minimize layout reflows.

### Property Performance

| Property | Performance | Recommendation |
| --- | --- | --- |
| `transform` | Composite | Preferred for movement/scale |
| `opacity` | Composite | Preferred for fades |
| `left`/`top` | Layout | AVOID for animations (triggers reflow) |
| `width`/`height` | Layout | AVOID for frequent animations |

### Must

- **[REQ-ANIM-04] Accessibility Overrides**
  - Every animation MUST respect the `prefers-reduced-motion` media query.
- **[REQ-ANIM-05] Timing Constraints**
  - UI transitions SHOULD generally be between 150ms and 300ms for optimal feel.
- **[REQ-ANIM-06] Layer Handoff**
  - Use `will-change` sparingly on elements that animate frequently to promote GPU layering.

### Must Not

- **[BAN-ANIM-01] Autoplay Motion**
  - Motion sequences longer than 5 seconds MUST NOT autoplay without a pause/stop control.
- **[BAN-ANIM-02] Layout-Thrashing Transitions**
  - Transitions MUST NOT target layout-inducing properties like `flex-basis` or `margin` in production.

### Failure Handling

- **Stop Condition**: Stop implementation if an animation triggers significant Layout Shift (CLS > 0.1).

## 2. Procedures

- **[PROC-ANIM-01] Motion Audit**
  - IF adding complex animations THEN MUST test with "Reduced Motion" setting enabled on the OS.
- **[PROC-ANIM-02] Performance Check**
  - Verify that animations do not drop below 60fps on low-end mobile devices.

## 3. Examples

### Reduced Motion Support

```css
@media (prefers-reduced-motion: reduce) {
  .animated-element {
    animation: none !important;
    transition: none !important;
  }
}
```

## 4. Validation Criteria

- **[VAL-ANIM-01] GPU Acceleration**
  - [ ] Animations use `transform` and `opacity` exclusively for movement.
- **[VAL-ANIM-02] User Control**
  - [ ] Large animations have a pause/stop toggle.
- **[VAL-ANIM-03] Timing Quality**
  - [ ] Transitions feel snappy and do not delay user task completion.
