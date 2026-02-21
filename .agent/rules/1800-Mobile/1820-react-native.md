---
trigger: always_on
glob: "**/*.{ts,tsx,js,jsx,json}"
description: "React Native Development Standards: Enforces Expo best practices, safe area management, and mobile-specific performance patterns."
---

# React Native Development Standards

- **Role**: React Native Mobile Architect
- **Purpose**: Define technical standards for building high-performance, maintainable mobile apps using React Native and the Expo ecosystem.
- **Activates When**: Developing mobile components, configuring navigation, or managing device-specific state.

**Trigger**: always_on — Apply during the implementation of React Native application features.

## 1. Standards

### Principles

- **[REQ-RN-01] Functional Declarativity**
  - UI logic MUST use functional components and hooks. Class-based components are deprecated and PROHIBITED.
- **[REQ-RN-02] Safe Boundary Awareness**
  - Layouts MUST explicitly account for device safe areas (notches, status bars) using `react-native-safe-area-context`.
- **[REQ-RN-03] Platform-Adaptive Logic**
  - Platform-specific code MUST be handled using `Platform.select()` or `.ios.tsx` / `.android.tsx` file extensions.

### Ecosystem Baseline

| Category | Requirement ID | Recommended Tooling |
| --- | --- | --- |
| Framework | [REQ-RN-04] | Expo (Managed Workflow) |
| Navigation | [REQ-RN-05] | React Navigation / Expo Router |
| Styling | [REQ-RN-06] | NativeWind / styled-components |
| Performance | [REQ-RN-07] | Reanimated 3 / FlashList |

### Must

- **[REQ-RN-08] Strict Type Interfaces**
  - Every component and navigation route MUST have a defined TypeScript interface.
- **[REQ-RN-09] List Virtualization**
  - Long lists MUST use `FlatList`, `SectionList`, or `FlashList` to ensure memory efficiency.
- **[REQ-RN-10] Encrypted Persistence**
  - Sensitive data (tokens, PII) MUST be stored using `react-native-encrypted-storage` or Expo SecureStore.

### Must Not

- **[BAN-RN-01] Absolute Dimensions**
  - Fixed width/height values (px) MUST NOT be used for layout; use Flexbox or percent-based scaling.
- **[BAN-RN-02] Sync Blocking States**
  - Heavy computation MUST NOT occur within the render cycle (use `useMemo` or Web Workers).

### Failure Handling

- **Stop Condition**: Stop deployment if the Android/iOS build fails its respective platform-specific lint or type-check.

## 2. Procedures

- **[PROC-RN-01] Performance Profiling**
  - IF a screen drops below 60FPS THEN MUST use the Flashlight or React DevTools profile to locate the leak.
- **[PROC-RN-02] Assets Optimization**
  - Optimize all images using WebP format and defined dimensions before adding to the `assets/` directory.

## 3. Examples

### Safe Area Wrapper

```tsx
import { SafeAreaView } from 'react-native-safe-area-context';

export function ScreenWrapper({ children }) {
  return <SafeAreaView style={{ flex: 1 }}>{children}</SafeAreaView>;
}
```

## 4. Validation Criteria

- **[VAL-RN-01] Frame Rate Audit**
  - [ ] Core navigations maintain inconsistent 60FPS during transition testing.
- **[VAL-RN-02] Safe Area Integrity**
  - [ ] No UI overlaps occur on notched devices (e.g., iPhone 15, Pixel 8).
- **[VAL-RN-03] Bundle Hygiene**
  - [ ] App bundle size is monitored and remains within defined multi-platform thresholds.
