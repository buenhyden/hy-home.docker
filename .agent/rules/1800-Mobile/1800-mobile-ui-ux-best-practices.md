---
trigger: always_on
glob: ["**/*.{tsx,jsx,swift,kt}"]
description: "Mobile UI/UX Standards: Enforces touch-first design, accessibility, and platform-specific interaction patterns (iOS/Android)."
---

# Mobile UI/UX Standards

- **Role**: Mobile Experience Designer
- **Purpose**: Define standards for building highly-accessible, performant, and platform-adaptive mobile user interfaces.
- **Activates When**: Designing or implementing mobile views, navigation flows, or touch interaction targets.

**Trigger**: always_on — Apply during the development of mobile-first application interfaces.

## 1. Standards

### Principles

- **[REQ-MOB-01] Touch-First Ergonomics**
  - Interactive elements MUST prioritize large hit areas (min 44x44pt) and reachability within the "Thumb Zone".
- **[REQ-MOB-02] Native Parity**
  - Applications SHOULD adhere to platform-specific HIG (Human Interface Guidelines) for iOS and Material Design for Android.
- **[REQ-MOB-03] Visual Confirmation**
  - Every touch interaction MUST provide immediate visual or haptic feedback to signal system acknowledgement.

### Adaptive Targets

| Platform | Min Touch Target | Key Navigator |
| --- | --- | --- |
| iOS | 44 x 44 pt | Tab Bar (Bottom) |
| Android | 48 x 48 dp | Navigation Rail / Drawer |
| Universal | 44 pt minimum | Floating Action Button |

### Must

- **[REQ-MOB-04] Semantic Accessibility**
  - Every interactive element MUST have an associated `accessibilityLabel` or equivalent native description.
- **[REQ-MOB-05] Feedback Continuity**
  - Transitions and animations MUST maintain spatial consistency to minimize user disorientation.
- **[REQ-MOB-06] Dynamic Sizing**
  - Typography and layouts MUST adapt to user-defined "Dynamic Type" and high-contrast accessibility settings.

### Must Not

- **[BAN-MOB-01] Fixed Precise Targets**
  - UI targets MUST NOT rely on mouse-like precision or hover states for critical path functionality.
- **[BAN-MOB-02] Blocking Loaders**
  - Long load operations MUST NOT block UI interaction without providing a "Skeleton" or "Spinner" fallback.

### Failure Handling

- **Stop Condition**: Stop feature release if touch targets fail the minimum size audit on a small physical device (e.g., iPhone SE size).

## 2. Procedures

- **[PROC-MOB-01] Accessibility Audit**
  - IF creating a new screen THEN MUST verify it with TalkBack (Android) or VoiceOver (iOS).
- **[PROC-MOB-02] Reachability Check**
  - Perform a "Thumb Zone" audit to ensure primary actions are reachable with one-handed use.

## 3. Examples

### Accessible Button (React Native)

```tsx
<TouchableOpacity
  accessible={true}
  accessibilityLabel="Submit Profile"
  onPress={handlePress}>
  <Text>Submit</Text>
</TouchableOpacity>
```

## 4. Validation Criteria

- **[VAL-MOB-01] Touch Accuracy**
  - [ ] 100% of interactive elements meet the 44x44pt minimum size requirement.
- **[VAL-MOB-02] Reachability Pass**
  - [ ] Primary CTAs are placed within the lower 1/3 of the screen for one-handed reach.
- **[VAL-MOB-03] A11y Verification**
  - [ ] The screen is fully traversable using only native gesture navigation for screen readers.
